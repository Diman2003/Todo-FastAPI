from typing import Optional
from pydantic import BaseModel,EmailStr
from datetime import datetime


class TodoCreate(BaseModel):
    title: str
    description: str
    completed: bool = False



class TodoList(BaseModel):
    id: Optional[int] = None
    title:str
    completed:bool
    class Config:
        orm_mode = True

class TodoDetail(BaseModel):
    id: Optional[int] = None
    title:str
    description: str
    completed:bool
    class Config:
        orm_mode = True



class UserCreate(BaseModel):
    email:EmailStr
    password:str

    
class BlacklistToken(BaseModel):
    token: str
    expires_at: datetime

