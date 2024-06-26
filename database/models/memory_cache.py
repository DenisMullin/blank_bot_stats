from sqlalchemy import Column, TEXT, JSON
from .mics import Base


class MemoryCache(Base):
    __tablename__ = 'memory_cache'

    key = Column(TEXT, primary_key=True)
    state = Column(TEXT)
    data = Column(JSON)