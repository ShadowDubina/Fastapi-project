from sqlalchemy import Column, Integer, String

from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    email = Column(String, unique=True, index=True, default=None)
    country = Column(String, default=None)
    hashed_password = Column(String)