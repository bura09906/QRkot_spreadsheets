from typing import Optional, Union

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import CharityProject, Donation, User


class CRUDBase:

    def __init__(self, model):
        self.model = model

    async def get(
        self,
        obj_id: int,
        session: AsyncSession,
    ):
        db_obj = await session.execute(
            select(self.model).where(
                self.model.id == obj_id
            )
        )
        return db_obj.scalars().first()

    async def get_all_obj(
        self,
        session: AsyncSession
    ):
        db_objs = await session.execute(select(self.model))
        return db_objs.scalars().all()

    async def get_by_filed_name(
        self,
        field_name: str,
        session: AsyncSession,
    ):
        obj_db = await session.execute(
            select(self.model).where(
                self.model.name == field_name
            )
        )
        return obj_db.scalars().first()

    async def get_my_donation(
        self,
        session: AsyncSession,
        user: User,
    ):
        my_donation = await session.execute(
            select(self.model).where(
                self.model.user_id == user.id
            )
        )
        return my_donation.scalars().all()

    async def create(
        self,
        obj_in: Union[CharityProject, Donation],
        session: AsyncSession,
        user: Optional[User] = None,
    ):
        obj_in_data = obj_in.dict()
        if user is not None:
            obj_in_data['user_id'] = user.id
        db_obj = self.model(**obj_in_data)
        session.add(db_obj)
        await session.flush()
        return db_obj

    async def remove(
            self,
            db_obj,
            session: AsyncSession,
    ):
        await session.delete(db_obj)
        await session.commit()
        return db_obj

    async def get_open_objects(
        self,
        session: AsyncSession,
    ):
        selection = await session.execute(
            select(self.model)
            .where(self.model.fully_invested.is_(False))
            .order_by(self.model.create_date)
        )
        return selection.scalars().all()
