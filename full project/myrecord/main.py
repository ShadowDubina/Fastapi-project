from database import engine, Base
from database import SessionLocal as session_maker
import requests, httpx
from fastapi import FastAPI, Request, HTTPException, Depends
import database, schemas, crud, models
from starlette import status
from typing import Annotated, List
from sqlalchemy.ext.asyncio import AsyncSession


app = FastAPI()
app.state.engine = engine
app.state.session_maker = session_maker



@app.on_event("startup")
async def on_startup():
    async with app.state.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.on_event("shutdown")
async def on_shutdown():
    # async with app.state.engine.begin() as conn:
    #     await conn.run_sync(Base.metadata.drop_all)
    await app.state.engine.dispose()


# @app.get('/get_firstuser')
# def first_user():
#     api_url = "https://jsonplaceholder.typicode.com/users"
#     all_users = requests.get(api_url).json()
#     user1 = all_users[0]
#     name = user1["name"]
#     email = user1["email"]
#     return {'name': name, "email": email}


@app.post("/create", response_model=schemas.URecord, status_code=status.HTTP_201_CREATED)
async def create_record(record:schemas.Record,session: Annotated[AsyncSession, Depends(crud.get_session)]):
        create = await crud.create_record(session,record)
        return create
    

@app.get("/record/{username}", response_model=schemas.URecord)
async def get_record(request:Request, username:str):
    async with request.app.state.session_maker() as session:
        get = await crud.get_record(session, username=username)
        if not get:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail='Client not found')
        return get


@app.delete("/record/{username}",status_code=status.HTTP_202_ACCEPTED)
async def delete_record(request:Request, username:str):
    db = request.app.state.session_maker
    async with db.begin() as session:
        user = await crud.get_record(session, username)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        delete = await crud.delete_record(session, username)

