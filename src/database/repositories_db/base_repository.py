from uuid import UUID

from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.expression import delete, insert, select


class BaseRepository:
    model = None
    mapper = None

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def add(self, **kwargs):

        smt = insert(self.model).values(**kwargs).returning(self.model)

        add_obj = await self.session.execute(smt)

        await self.session.commit()

        return self.mapper.model_validate(add_obj.scalar_one())

    async def get_all(self):
        objects = await self.session.execute(select(self.model))

        await self.session.commit()

        return [self.mapper.model_validate(data) for data in objects.scalars()]

    async def get_id(self, id: str | UUID | int):

        object = await self.session.get(self.model, id)

        if not object:
            return None

        return self.mapper.model_validate(object)

    async def get_filter(
        self,
        **kwargs,
    ):
        smt = select(self.model).filter_by(**kwargs)
        objects = await self.session.execute(smt)
        return [self.mapper.model_validate(object) for object in objects.scalars()]

    async def delete(self, **kwargs):

        smt = delete(self.model).filter_by(**kwargs).returning(self.model)

        objects = await self.session.execute(smt)

        await self.session.commit()

        return [self.mapper.model_validate(data) for data in objects.scalars().all()]

    async def update(self, model_id: int | str | UUID, **kwargs):

        smt = (
            update(self.model)
            .values(**kwargs)
            .returning(self.model)
            .where(self.model.id == model_id)
        )

        confirm = await self.session.execute(smt)

        await self.session.commit()

        return self.mapper.model_validate(confirm.scalar_one())
