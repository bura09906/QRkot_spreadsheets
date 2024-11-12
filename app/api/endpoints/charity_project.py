from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (check_charity_project_exists,
                                validate_field_name,
                                validate_remove_charity_project,
                                validate_update_charity_project)
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.charity_project import charity_project_crud
from app.crud.donation import donation_crud
from app.schemas.charity_project import (CharityProjectCreate,
                                         CharityProjectDB,
                                         CharityProjectUpdate)
from app.services.investment_service import process_investment

router = APIRouter()


@router.post(
    '/',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def create_charity_project(
    charity_project: CharityProjectCreate,
    session: AsyncSession = Depends(get_async_session)
):
    await validate_field_name(charity_project.name, session)

    new_charity_project = await charity_project_crud.create(
        charity_project, session
    )

    interaction_objects = await donation_crud.get_open_objects(session)
    if interaction_objects:
        update_objects = process_investment(
            target=new_charity_project,
            sources=interaction_objects,
        )
        for obj in update_objects:
            session.add(obj)

    await session.commit()
    await session.refresh(new_charity_project)
    return new_charity_project


@router.get(
    '/',
    response_model=list[CharityProjectDB],
    response_model_exclude_none=True,
)
async def get_all_charity_projetc(
    session: AsyncSession = Depends(get_async_session)
) -> list[CharityProjectDB]:
    results = await charity_project_crud.get_all_obj(session)
    return results


@router.patch(
    '/{project_id}',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def partially_update_charity_project(
    project_id: int,
    update_data: CharityProjectUpdate,
    session: AsyncSession = Depends(get_async_session)
):
    charity_project = await check_charity_project_exists(
        project_id, session
    )
    await validate_update_charity_project(
        charity_project, update_data, session
    )

    charity_project = await charity_project_crud.update(
        charity_project, update_data, session
    )
    return charity_project


@router.delete(
    '/{project_id}',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def remove_charity_project(
    project_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    charity_project = await check_charity_project_exists(
        project_id, session
    )
    validate_remove_charity_project(charity_project)

    charity_project = await charity_project_crud.remove(
        charity_project, session
    )
    return charity_project