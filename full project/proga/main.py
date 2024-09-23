from database import engine, Base
from database import SessionLocal as session_maker
from fastapi import FastAPI, Request, HTTPException, Depends
import database, schemas, crud, models
from starlette import status
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated, List
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import OAuth2PasswordBearer
from crud import get_password_hash


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




@app.post("/create", response_model=schemas.PUser, status_code=status.HTTP_201_CREATED)
async def create_user(user:schemas.PUser,session: Annotated[AsyncSession, Depends(crud.get_session)]):
        create = await crud.create_user(session, user)
        return create
    

@app.get("/user/{username}", response_model=schemas.AUser)
async def get_user(request:Request, username:str):
    async with request.app.state.session_maker() as session:
        get = await crud.get_user(session, username=username)
        if not get:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail='Client not found')
        return get


@app.delete("/user/{username}",status_code=status.HTTP_202_ACCEPTED)
async def delete_user(request:Request, username:str):
    db = request.app.state.session_maker
    async with db.begin() as session:
        user = await crud.get_user(session, username)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        delete = await crud.delete_user(session, username)


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@app.post("/token")
async def login(request:Request,form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    async with request.app.state.session_maker() as session:
        user = await crud.get_user(session,form_data.username)
        if not user:
            raise HTTPException(status_code=400, detail="Incorrect username or password")
        hashed_password = get_password_hash(form_data.password)
        if not hashed_password == user.hashed_password:
            raise HTTPException(status_code=400, detail="Incorrect username or password")
        return {"access_token": user.username, "token_type": "bearer"}



@app.get("/users", response_model=List[schemas.IUser])
async def get_users(request:Request, offset:int=None, limit:int=None)->List[models.User]:
    async with request.app.state.session_maker() as session:
        users = await crud.get_users(session, offset=offset, limit=limit)
        return users
    

@app.patch("/user/{username}",response_model=schemas.AUser, status_code=status.HTTP_202_ACCEPTED)
async def update_user(request:Request, username:str,data:schemas.AUser):
    db = request.app.state.session_maker
    async with db.begin() as session:
        user = await crud.get_user(session, username)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        mydata=data.dict(exclude_unset=True)
        update=await crud.update_user(session, username, mydata)
        return update

    

