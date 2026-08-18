from datetime import UTC, datetime
from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy import desc, func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from ...data_mappers.data_mappers_get import (
    GetReviewItemMapper,
    GetReviewPaginationMapper,
    GetReviewUserMapper,
)
from ...database.db_models import Like
from ...database.repositories_db import (
    OrderItemRepository,
    ProductsRepository,
    ReviewsRepository,
)
from ...schemes import UpdateReviewsScheme


class ReviewService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.product_repo = ProductsRepository(session=session)
        self.review_repo = ReviewsRepository(session=session)
        self.order_items_repo = OrderItemRepository(session=session)

    async def create_review(
        self, user_id: UUID, product_id: int, rating: float, title: str, content: str
    ):
        orders_items = await self.order_items_repo.get_filter(product_id=product_id)

        if not orders_items:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You cannot leave a review for a product you did not order.",
            )
        try:
            review = await self.review_repo.add(
                user_id=user_id,
                product_id=product_id,
                rating=rating,
                title=title,
                content=content,
            )
        except IntegrityError as e:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail="That's review already exists."
            ) from e

        product = await self.session.get(self.product_repo.model, product_id)

        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
            )
        rating_review_db = await self.session.scalars(
            select(self.review_repo.model.rating).where(
                self.review_repo.model.product_id == product_id
            )
        )
        sum_review_rating = 0
        product.review_count += 1

        for rating in rating_review_db:
            sum_review_rating += rating

        product.rating = sum_review_rating / product.review_count

        await self.session.commit()
        await self.session.refresh(product)

        return review, product.rating, product.review_count

    async def delete_review(self, review_id: int, user_id: UUID):
        review = await self.review_repo.delete(id=review_id, user_id=user_id)

        try:
            review_count_rating_db = await self.session.execute(
                select(
                    func.avg(ReviewsRepository.model.rating).label("rating"),
                    func.count(ReviewsRepository.model.id).label("review_count"),
                ).where(ReviewsRepository.model.product_id == review[0].product_id)
            )
            review_count_rating = review_count_rating_db.first()

            product = await self.session.get(self.product_repo.model, review[0].product_id)
        except IndexError as e:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Review not found"
            ) from e

        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
            )

        product.review_count -= 1
        try:
            product.rating = review_count_rating.rating / review_count_rating.review_count
        except ZeroDivisionError:
            product.rating = 0

        await self.session.commit()
        await self.session.refresh(product)

        return review, product.rating, product.review_count

    async def update_review(self, review_update: UpdateReviewsScheme):

        review = await self.session.get(self.review_repo.model, review_update.review_id)

        if not review:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Review not found"
            )

        if review_update.content:
            review.content = f"{review.content}\nДополнение: {review_update.content}"  # noqa: RUF001

        if review_update.rating:
            product = await self.session.get(self.product_repo.model, review.product_id)

            if not product:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
                )

            review.rating = review_update.rating

            try:
                product.rating = review.rating / product.review_count
            except ZeroDivisionError:
                product.rating = 0

        review.updated_at = datetime.now(UTC)

        if review_update.title:
            review.title = review_update.title

        await self.session.commit()
        await self.session.refresh(review)

        return review

    async def get_reviews_product(
        self, product_id: int, page: int, size: int, new: bool, more_like: bool
    ):
        count_reviews = await self.session.scalar(
            select(func.count()).select_from(ReviewsRepository.model)
        )

        stmt = (
            select(
                self.review_repo.model,
                func.count(Like.review_id).label("likes_count"),
            )
            .join(Like, Like.review_id == self.review_repo.model.id, isouter=True)
            .options(
                selectinload(self.review_repo.model.products),
                selectinload(self.review_repo.model.users),
            )
            .where(self.review_repo.model.product_id == product_id)
            .group_by(self.review_repo.model.id)
            .offset(size * (page - 1))
            .limit(size)
        )
        order_cond = []

        if new:
            order_cond.append(self.review_repo.model.created_at.desc())
        if more_like:
            order_cond.append(desc("likes_count"))
        if order_cond:
            stmt = stmt.order_by(*order_cond)

        reviews_data = await self.session.execute(stmt)
        reviews_data_validate = []

        for data in reviews_data.unique().all():
            reviews_data_validate.append(
                GetReviewItemMapper(
                    id=data[0].id,
                    product_id=data[0].products[0].id,
                    rating=data[0].rating,
                    content=data[0].content,
                    created_at=data[0].created_at,
                    likes_count=data.likes_count,
                    user=GetReviewUserMapper(
                        id=data[0].users.id, nickname=data[0].users.nickname
                    ),
                )
            )

        return reviews_data_validate, GetReviewPaginationMapper(
            page=page, size=size, pages_all=(count_reviews // size)
        )

    async def get_review_product(self, review_id: int):
        reviews_data_db = await self.session.execute(
            select(self.review_repo.model, func.count(Like.review_id).label("likes_count"))
            .join(Like, Like.review_id == self.review_repo.model.id, isouter=True)
            .options(
                selectinload(self.review_repo.model.products),
                selectinload(self.review_repo.model.users),
            )
            .group_by(self.review_repo.model.id)
            .where(self.review_repo.model.id == review_id)
        )

        review_data = reviews_data_db.one()

        return (
            GetReviewItemMapper(
                id=review_data[0].id,
                product_id=review_data[0].products[0].id,
                rating=review_data[0].rating,
                content=review_data[0].content,
                created_at=review_data[0].created_at,
                likes_count=review_data.likes_count,
                user=GetReviewUserMapper(
                    id=review_data[0].users.id, nickname=review_data[0].users.nickname
                ),
            ),
        )
