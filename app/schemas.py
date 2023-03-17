from pydantic import BaseModel, EmailStr
from datetime import date
from typing import List, Union


class PeopleMain(BaseModel):
    id: int
    full_name: Union[str, None] = None
    photo_title: str

    class Config:
        orm_mode = True


class PhotoMain(BaseModel):
    id: int
    title: str
    location: Union[str, None] = None
    creating_date: date
    owner_id: int
    people: List[PeopleMain] = []

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    username: str
    email: EmailStr
    full_name: str


class UserCreate(UserBase):
    password: str


class UserMain(UserBase):
    id: int
    photos: List[PhotoMain] = []
    hashed_password: str

    class Config:
        orm_mode = True


class TokenData(BaseModel):
    username: str

