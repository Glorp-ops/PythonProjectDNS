from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi_cache.decorator import cache
from sqlalchemy.ext.asyncio import AsyncSession

from ..data_mappers.data_mappers_get import GetProductsMapper
from ..data_mappers.data_mappers_repository import ProductsMapper
from ..database.repositories_db import ProductsRepository
from ..database.sqlalchemy_connect import get_session
from ..dependencies import (
    validate_product_get_id_with_join_and_description,
)
from ..schemes import pagination

router = APIRouter(prefix="/api/v1/products", tags=["products"])


@cache(1800)
@router.get(
    "",
    response_model=list[GetProductsMapper],
)
# 1800
@cache(expire=10)
async def get_products(
    session: Annotated[AsyncSession, Depends(get_session)],
    pagination: pagination,
):
    return await ProductsRepository(session).get_all_with_join_no_description(
        page=pagination.page, size=pagination.size
    )


@router.get(
    "/{product_id}",
    response_model=ProductsMapper,
)
# 30
@cache(expire=10)
async def get_product(product_id: int, session: Annotated[AsyncSession, Depends(get_session)]):
    return await validate_product_get_id_with_join_and_description(session, product_id)
