from typing import Union
from pydantic import BaseModel


class User(BaseModel):
    username: str

    class Config:
        orm_mode=True


class PUser(User):
    hashed_password: str 



class AUser(User):
    email: Union[str, None] = None
    country: Union[str, None] = None


class IUser(AUser):
    id:int


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None