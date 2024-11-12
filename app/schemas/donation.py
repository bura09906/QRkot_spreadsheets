from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra, PositiveInt


class BaseDonation(BaseModel):
    full_amount: PositiveInt
    comment: Optional[str]


class DonationCreate(BaseDonation):
    pass

    class Config:
        extra = Extra.forbid


class ForDonationList(BaseDonation):
    id: int
    create_date: datetime
    user_id: int
    invested_amount: int
    fully_invested: bool
    close_date: Optional[datetime]

    class Config:
        orm_mode = True


class ForUserDonation(BaseDonation):
    id: int
    create_date: datetime

    class Config:
        orm_mode = True