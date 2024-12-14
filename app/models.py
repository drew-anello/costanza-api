from sqlalchemy import Column, Integer, String
from app.db import Base


class Quote(Base):
    __tablename__ = "quotes"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    quote = Column(String, nullable=False, unique=True)
    season = Column(Integer, nullable=False)
    episode = Column(Integer, nullable=False)
    character = Column(String, nullable=False)
