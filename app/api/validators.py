from fastapi.exceptions import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.constants import DEFAULT_INVESTED_AMOUNT
from app.crud.charity_project import charity_project_crud
from app.models import CharityProject
from app.schemas.charity_project import CharityProjectUpdate


async def check_charity_project_exists(
    charity_project_id: int,
    session: AsyncSession,
):
    charity_project = await charity_project_crud.get(
        charity_project_id, session
    )
    if charity_project is None:
        raise HTTPException(
            status_code=404,
            detail='Проект не найден!'
        )
    return charity_project


async def validate_field_name(
    field_name: str,
    session: AsyncSession,
):
    obj_db = await charity_project_crud.get_by_filed_name(
        field_name, session
    )
    if obj_db:
        raise HTTPException(
            status_code=400,
            detail='Проект с таким именем уже существует!',
        )


async def validate_update_charity_project(
    charity_project: CharityProject,
    update_data: CharityProjectUpdate,
    session: AsyncSession,
):
    if charity_project.fully_invested:
        raise HTTPException(
            status_code=400,
            detail='Нельзя обновить закрытый проект'
        )
    if update_data.name:
        await validate_field_name(update_data.name, session)
    if (
        update_data.full_amount is not None and
        charity_project.invested_amount > update_data.full_amount
    ):
        raise HTTPException(
            status_code=422,
            detail=('Поле full_amount не может быть установленно '
                    'меньше текущего значения поля invested_amount')
        )


def validate_remove_charity_project(
    charity_project: CharityProject,
):
    if (
        charity_project.invested_amount > DEFAULT_INVESTED_AMOUNT or
        charity_project.fully_invested
    ):
        raise HTTPException(
            status_code=400,
            detail="В проект были внесены средства, не подлежит удалению!"
        )