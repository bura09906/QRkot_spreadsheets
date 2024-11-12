from datetime import timedelta
from typing import Union

from fastapi.encoders import jsonable_encoder
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.charity_project import CharityProject


class CRUDCharityProject(CRUDBase):
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


charity_project_crud = CRUDCharityProject(CharityProject)
