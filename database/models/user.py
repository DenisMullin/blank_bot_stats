from sqlalchemy import Column, String, BigInteger, DateTime, text

from .mics import Base


class User(Base):
    __tablename__ = 'user'

    first_name = Column(String(255))
    last_name = Column(String(255))
    id = Column(BigInteger, primary_key=True)
    username = Column(String(32))
    registration_date = Column(
        DateTime, server_default=text("timezone('utc', now())")
    )