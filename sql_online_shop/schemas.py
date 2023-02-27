from pydantic import BaseModel
from typing import Optional


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


class ItemCreate(ItemBase):
    pass


class Item(ItemBase):
    id: int
    category_id: int

    class Config:
        orm_mode = True
