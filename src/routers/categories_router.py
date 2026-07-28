from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi_cache.decorator import cache
from sqlalchemy.ext.asyncio import AsyncSession

from ..data_mappers.data_mappers_repository import CategoriesMapper
from ..database.repositories_db import CategoriesRepository
from ..database.sqlalchemy_connect import get_session
from ..dependencies import build_tree

router = APIRouter(prefix="/api/v1/categories", tags=["categories"])


@router.get("/categories", response_model=list[CategoriesMapper])
@cache(3600)
async def get_categories(session: Annotated[AsyncSession, Depends(get_session)]):
    return await CategoriesRepository(session).get_all()


@router.get("/tree-categories")
@cache(3600)
async def get_tree_categories(session: Annotated[AsyncSession, Depends(get_session)]):
    return build_tree(await CategoriesRepository(session).get_all())
