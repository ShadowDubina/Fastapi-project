from sqlalchemy.ext.asyncio import AsyncSession
from passlib.context import CryptContext
import models, schemas
from sqlalchemy import delete, select, update
from typing import  List
from fastapi import Request


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password:str):
    return "fake" + password


async def create_user(db:AsyncSession, user:schemas.PUser):
    password = get_password_hash(user.hashed_password)
    db_user = models.User(username = user.username, hashed_password = password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user



async def get_user(db:AsyncSession, username: str):
    return await db.scalar(select(models.User).where(models.User.username == username))



async def delete_user(db:AsyncSession, username: str):
   return await db.execute(delete(models.User).where(models.User.username==username))



async def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


async def get_session(request: Request):
    db = request.app.state.session_maker
    async with db.begin() as session:
        yield session


async def get_users(db:AsyncSession, offset:int = 0, limit:int = 100)->List[models.User]:
    where = list()
    return await db.scalars(
        select(models.User).where(*where).limit(limit).offset(offset)
        )


async def update_user(db:AsyncSession, username:str, data:dict)->None:
    await db.execute(
        update(models.User).where(models.User.username == username).values(data)
    )