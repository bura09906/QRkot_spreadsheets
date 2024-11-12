from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra, Field, PositiveInt

from app.constants import MAX_LENGH_FIELD_NAME, MIN_LENGH_STR_FIELD


class BaseCharityProject(BaseModel):
    name: str = Field(
        min_length=MIN_LENGH_STR_FIELD, max_length=MAX_LENGH_FIELD_NAME
    )
    description: str = Field(min_length=MIN_LENGH_STR_FIELD)
    full_amount: PositiveInt


class CharityProjectCreate(BaseCharityProject):
    pass

    class Config:
        extra = Extra.forbid


class CharityProjectUpdate(CharityProjectCreate):
    name: Optional[str] = Field(max_length=MAX_LENGH_FIELD_NAME)
    description: Optional[str]
    full_amount: Optional[PositiveInt]

    class Config:
        extra = Extra.forbid
        min_anystr_length = MIN_LENGH_STR_FIELD


class CharityProjectDB(BaseCharityProject):
    id: int
    invested_amount: int
    fully_invested: bool
    create_date: datetime
    close_date: Optional[datetime]

    class Config:
        orm_mode = True
