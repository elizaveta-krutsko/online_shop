from pydantic import BaseModel, EmailStr
from typing import Optional
from fastapi_users import schemas


class CategoryBase(BaseModel):
    name: str


class CategoryCreate(CategoryBase):
    parent_category_id: Optional[int]


class Category(CategoryBase):
    id: int
    parent_category_id: Optional[int]
    child_categories: Optional[list] = []

    class Config:
        orm_mode = True


class CategoryUpdate(CategoryBase):
    parent_category_id: Optional[int]
    name: Optional[str]

    class Config:
        orm_mode = True


class ItemBase(BaseModel):
    name: str
    unit_price: float
    amount: int
    item_category_id: int

    class Config:
        orm_mode = True


class Item(ItemBase):
    id: int

    class Config:
        orm_mode = True


class ItemUpdate(BaseModel):
    name: Optional[str]
    unit_price: Optional[float]
    amount: Optional[int]
    item_category_id: Optional[int]


############### USERS ################
class UserRead(schemas.BaseUser[int]):
    id: int
    email: EmailStr
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False

    class Config:
        orm_mode = True


class UserCreate(schemas.BaseUserCreate):
    email: EmailStr
    user_name: str
    first_name: Optional[str]
    last_name: Optional[str]
    password: str
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False


class UserUpdate(schemas.BaseUserUpdate):
    user_name: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    password: Optional[str]
    email: Optional[EmailStr]
    is_active: Optional[bool]
    is_superuser: Optional[bool]
    is_verified: Optional[bool]
