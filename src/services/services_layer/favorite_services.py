from uuid import UUID

from fastapi import HTTPException
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload
from starlette import status

from ...data_mappers.data_mappers_get import (
    GetFavoriteMapper,
    GetFavoritesMapper,
    GetProductsMapper,
)
from ...data_mappers.data_mappers_repository import ProductsMapper
from ...database.repositories_db import FavoriteRepository, ProductsRepository


class FavoriteServices:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.favorite_repo = FavoriteRepository(session)
        self.products_repo = ProductsRepository(session)

    async def get_favorites(self, user_id: UUID, page: int, size: int):
        count_fovourite = await self.session.scalar(
            select(func.count()).select_from(self.favorite_repo.model)
        )

        favorite_data_db = await self.session.execute(
            select(self.favorite_repo.model)
            .where(self.favorite_repo.model.user_id == user_id)
            .offset(size * (page - 1))
            .limit(size)
            .options(
                joinedload(self.favorite_repo.model.products).selectinload(
                    self.products_repo.model.images
                )
            )
        )
        favorite_data = []

        for data in favorite_data_db.scalars().unique().all():
            favorite_data.append(
                GetFavoritesMapper(
                    favorite_id=data.id,
                    added_at=data.created_at,
                    products=GetProductsMapper(
                        id=data.products[0].id,
                        name=data.products[0].name,
                        price=data.products[0].price,
                        review_count=data.products[0].review_count,
                        rating=data.products[0].rating,
                        image_url=data.products[0].images[0].image_url,
                    ),
                )
            )

        return (
            favorite_data,
            len(favorite_data),
            {"page": page, "size": size, "all_pages": count_fovourite // size},
        )

    async def get_favorite(self, product_id: int, user_id: UUID):
        favorite_data_db = await self.session.execute(
            select(self.favorite_repo.model)
            .where(
                self.favorite_repo.model.product_id == product_id,
                self.favorite_repo.model.user_id == user_id,
            )
            .options(
                joinedload(self.favorite_repo.model.products).options(
                    selectinload(self.products_repo.model.images),
                    selectinload(self.products_repo.model.products_categories),
                )
            )
        )

        favorite_data = favorite_data_db.scalars().unique().all()

        if not favorite_data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Don't found product_id",
            )

        return GetFavoriteMapper(
            favorite_id=favorite_data[0].id,
            product=ProductsMapper(
                id=favorite_data[0].products[0].id,
                name=favorite_data[0].products[0].name,
                price=favorite_data[0].products[0].price,
                description=favorite_data[0].products[0].description,
                sku=favorite_data[0].products[0].sku,
                quantity=favorite_data[0].products[0].quantity,
                rating=favorite_data[0].products[0].rating,
                review_count=favorite_data[0].products[0].review_count,
                is_deleted=favorite_data[0].products[0].is_deleted,
                images_url=[data.image_url for data in favorite_data[0].products[0].images],
                created_at=favorite_data[0].products[0].created_at,
                active_at=favorite_data[0].products[0].active_at,
                categories=[
                    data.category_id
                    for data in favorite_data[0].products[0].products_categories
                ],
            ),
        )
