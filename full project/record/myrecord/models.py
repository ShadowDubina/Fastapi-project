from sqlalchemy import Column, Integer, String

from .database import Base

class Record(Base):
    __tablename__ = "records"

    id = Column(Integer, primary_key=True)
    username = Column(String)
    body = Column(String)