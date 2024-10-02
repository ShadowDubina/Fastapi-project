from sqlalchemy.ext.asyncio import AsyncSession
from . import models, schemas
from sqlalchemy import delete, select, update
from starlette import status
from fastapi import Request
import httpx
from typing import  List


async def create_record(db:AsyncSession,record:schemas.Record):
    username = await second_user()
    db_user = models.Record(username = username, body=record.body)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


async def get_record(db:AsyncSession, username: str):
    return await db.scalar(select(models.Record).where(models.Record.username == username))



async def delete_record(db:AsyncSession, username: str):
   return await db.execute(delete(models.Record).where(models.Record.username==username))



async def get_session(request: Request):
    db = request.app.state.session_maker
    async with db.begin() as session:
        yield session


async def second_user():
    api_url = "http://127.0.0.1:8000/users"
    async with httpx.AsyncClient() as client:
        response = await client.get(api_url)
        user = response.json()
        user2 = user[0]
        name = user2["username"]
        return name
    

async def get_records(db:AsyncSession, offset:int = 0, limit:int = 100)->List[models.Record]:
    where = list()
    return await db.scalars(
        select(models.Record).where(*where).limit(limit).offset(offset)
        )