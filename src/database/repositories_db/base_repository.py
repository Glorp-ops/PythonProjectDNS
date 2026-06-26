import logging

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.expression import insert, select


class BaseRepository:
    model = None
    mapper = None

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def add(self, **kwargs):

        smt = insert(self.model).values(**kwargs).returning(self.model)

        add_obj = await self.session.scalars(smt)

        await self.session.commit()

        return [self.mapper.model_validate(object) for object in add_obj.all()]

    async def get_all(self):
        objects = await self.session.execute(select(self.model))

        await self.session.commit()

        return [self.mapper.model_validate(object) for object in objects]

    async def get_one_or_none(self, id: int):

        object = await self.session.get(self.model, id)

        if not object:
            return None

        await self.session.commit()

        return self.mapper.model_validate(object)

    async def get_filter(self, **kwargs):
        smt = select(self.model).filter_by(**kwargs)
        objects = await self.session.scalars(smt)

        await self.session.commit()

        return [self.mapper.model_validate(object) for object in objects.all()]

    async def delete(self, id: int):

        object = await self.session.get(self.model, id)

        await self.session.delete(object)

        await self.session.commit()
