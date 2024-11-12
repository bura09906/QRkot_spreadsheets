from sqlalchemy import Column, String, Text
from sqlalchemy.schema import CheckConstraint

from app.constants import MAX_LENGH_FIELD_NAME, MIN_LENGH_STR_FIELD

from .base import BaseFundModel


class CharityProject(BaseFundModel):
    name = Column(String(MAX_LENGH_FIELD_NAME), unique=True, nullable=False)
    description = Column(Text, nullable=False)

    __table_args__ = (
        CheckConstraint(
            sqltext=(f'length(name) >= {MIN_LENGH_STR_FIELD} '
                     f'AND length(description) >= {MIN_LENGH_STR_FIELD}'),
            name='Проверка минимального значения полей name и description'
        ),
    )

    @property
    def сlosing_time(self):
        if self.close_date is not None:
            return str(self.close_date - self.create_date)
