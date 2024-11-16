from datetime import timedelta
from typing import Optional, Union

from fastapi.encoders import jsonable_encoder
from sqlalchemy import func, select
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

    async def update(
        self,
        db_obj,
        obj_in,
        session: AsyncSession,
    ):
        obj_data = jsonable_encoder(db_obj)
        update_data = obj_in.dict(exclude_unset=True)

        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])

        if db_obj.full_amount == db_obj.invested_amount:
            db_obj.to_close()

        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
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

    async def get_projects_by_completion_rate(
            self, session: AsyncSession
    ) -> list[dict[str, Union[str, timedelta]]]:
        results = await session.execute(
            select(self.model)
            .where(self.model.fully_invested.is_(True))
            .order_by(
                func.extract('epoch', self.model.close_date) -
                func.extract('epoch', self.model.create_date)
            )
        )
        results = results.scalars().all()

        closed_projects_by_closing_time = []

        for project in results:
            closed_projects_by_closing_time.append(
                {
                    'name': project.name,
                    'closing_time': project.сlosing_time,
                    'description': project.description,
                }
            )

        return closed_projects_by_closing_time
