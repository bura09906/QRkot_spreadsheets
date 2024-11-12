from sqlalchemy import Column, ForeignKey, Integer, Text

from .base import BaseFundModel


class Donation(BaseFundModel):
    user_id = Column(Integer, ForeignKey('user.id'))
    comment = Column(Text)
