from typing import Union
from pydantic import BaseModel

class Record(BaseModel):
    body: str

    class Config:
        orm_mode=True

class URecord(Record):
    username:str