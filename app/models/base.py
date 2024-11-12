from datetime import datetime as dt

from sqlalchemy import Boolean, Column, DateTime, Integer
from sqlalchemy.schema import CheckConstraint

from app.constants import DEFAULT_INVESTED_AMOUNT, THRESHOLD_FULL_AMOUNT
from app.core.db import Base


class BaseFundModel(Base):
    __abstract__ = True

    full_amount = Column(Integer, nullable=False)
    invested_amount = Column(
        Integer, nullable=False, default=DEFAULT_INVESTED_AMOUNT
    )
    fully_invested = Column(Boolean, default=False)
    create_date = Column(DateTime, index=True, default=dt.utcnow)
    close_date = Column(DateTime, index=True,)

    __table_args__ = (
        CheckConstraint(
            sqltext=(f'full_amount > {THRESHOLD_FULL_AMOUNT} AND '
                     f'invested_amount >= {DEFAULT_INVESTED_AMOUNT}'),
            name='Проверка целочисленных полей',
        ),
    )

    @property
    def available_funds(self):
        return self.full_amount - self.invested_amount

    def to_close(self):
        self.fully_invested = True
        self.close_date = dt.utcnow()