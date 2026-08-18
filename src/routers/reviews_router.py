from typing import Annotated

from fastapi import APIRouter, Depends, Path, Request
from fastapi_cache.decorator import cache
from sqlalchemy.ext.asyncio import AsyncSession

from ..database.repositories_db import LikeRepository
from ..database.sqlalchemy_connect import get_session
from ..dependencies import validate_create_like_review
from ..schemes import (
    LikeReviewScheme,
    ReviewsProductDep,
    ReviewsScheme,
    UpdateReviewsScheme,
)
from ..services import check_users_sessions
from ..services.services_layer import ReviewService

router = APIRouter(
    prefix="/api/v1/reviews",
    tags=["reviews"],
)


@cache(60 * 15)
@router.get("")
async def get_reviews(
    session: Annotated[AsyncSession, Depends(get_session)],
    request: Request,
    reviews_product: ReviewsProductDep,
):

    await check_users_sessions(session, request=request, permission="review:view")

    reviews_data, pagination = await ReviewService(session).get_reviews_product(
        product_id=reviews_product.product_id,
        page=reviews_product.pagination.page,
        size=reviews_product.pagination.size,
        new=reviews_product.new,
        more_like=reviews_product.more_likes,
    )

    return {"result": True, "reviews_data": reviews_data, "pagination": pagination}


@router.get("/{review_id}")
async def get_review(
    session: Annotated[AsyncSession, Depends(get_session)],
    request: Request,
    review_id: Annotated[int, Path(gt=0)],
):

    await check_users_sessions(session, request=request, permission="review:view")

    reviews_data = await ReviewService(session).get_review_product(review_id)

    return {"result": True, "reviews_data": reviews_data}


@router.post("", status_code=201)
async def create_review(
    review: ReviewsScheme,
    session: Annotated[AsyncSession, Depends(get_session)],
    request: Request,
):

    payload_validate, _ = await check_users_sessions(
        session, request=request, permission="review:create"
    )

    review, rating, review_count = await ReviewService(session).create_review(
        user_id=payload_validate.userId,
        product_id=review.product_id,
        rating=review.rating,
        content=review.content,
        title=review.title,
    )

    return {
        "result": True,
        "review": review,
        "updated_product": {"rating": rating, "review_count": review_count},
    }


@router.post("/like", status_code=201)
async def like_review(
    session: Annotated[AsyncSession, Depends(get_session)],
    request: Request,
    like: LikeReviewScheme,
):
    payload_validate, _ = await check_users_sessions(
        session, request=request, permission="review:like"
    )

    like_data, like_count = await validate_create_like_review(
        session=session, user_id=payload_validate.userId, review_id=like.review_id
    )

    return {"result": True, "like_data": like_data, "like_count": like_count}


@router.delete("/like/{review_id}")
async def delete_like_review(
    review_id: Annotated[int, Path(gt=0)],
    session: Annotated[AsyncSession, Depends(get_session)],
    request: Request,
):
    payload_validate, _ = await check_users_sessions(
        session, request=request, permission="review:like"
    )

    delete_like = await LikeRepository(session).delete(
        review_id=review_id, user_id=payload_validate.userId
    )

    return {"result": True, "delete_like": delete_like}


@router.delete("/{review_id}")
async def delete_review(
    review_id: Annotated[int, Path(gt=0)],
    session: Annotated[AsyncSession, Depends(get_session)],
    request: Request,
):
    payload_validate, _ = await check_users_sessions(
        session, request=request, permission="review:delete"
    )

    review, rating, review_count = await ReviewService(session).delete_review(
        review_id=review_id, user_id=payload_validate.userId
    )

    return {
        "result": True,
        "deleted_review": review,
        "updated_product": {"rating": rating, "review_count": review_count},
    }


@router.patch("")
async def update_review(
    review_update: UpdateReviewsScheme,
    session: Annotated[AsyncSession, Depends(get_session)],
    request: Request,
):
    await check_users_sessions(session, request=request, permission="review:edit")

    review = await ReviewService(session).update_review(review_update=review_update)

    return {
        "result": True,
        "updated_review": review,
    }
