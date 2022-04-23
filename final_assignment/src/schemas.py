from typing import Optional

from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = True
    full_name: Optional[str] = None


class UserCreate(UserBase):
    email: EmailStr
    password: str


class UserInDBBase(UserBase):
    id: Optional[str] = None

    class Config:
        orm_mode = True


class BookBase(BaseModel):
    title: str
    author: str
    published: int


class BookCreate(BookBase):
    is_active: Optional[bool] = True


class BookInDBBase(BookBase):
    id: str

    class Config:
        orm_mode = True


class AddToFavourite(BaseModel):
    user_id: str
    book_id: str
    like: bool = True


class UserFavouriteCount(BaseModel):
    user_id: str
    count: int

    class Config:
        orm_mode = True
