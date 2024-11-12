from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.crud.charity_project import charity_project_crud
from app.crud.donation import donation_crud
from app.models import User
from app.schemas.donation import (DonationCreate, ForDonationList,
                                  ForUserDonation)
from app.services.investment_service import process_investment

router = APIRouter()


@router.post(
    '/',
    response_model=ForUserDonation,
    response_model_exclude_none=True,
)
async def create_donation(
    donation: DonationCreate,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
):
    new_donation = await donation_crud.create(
        obj_in=donation,
        session=session,
        user=user,
    )

    interaction_objects = await charity_project_crud.get_open_objects(session)
    if interaction_objects:
        update_objects = process_investment(
            target=new_donation,
            sources=interaction_objects
        )
        for obj in update_objects:
            session.add(obj)

    await session.commit()
    await session.refresh(new_donation)
    return new_donation


@router.get(
    '/',
    response_model=list[ForDonationList],
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def get_all_donation(
    session: AsyncSession = Depends(get_async_session)
):
    results = await donation_crud.get_all_obj(session)
    return results


@router.get(
    '/my',
    response_model=list[ForUserDonation],
    response_model_exclude_none=True,
)
async def get_my_donation(
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
):
    results = await donation_crud.get_my_donation(session, user)
    return results