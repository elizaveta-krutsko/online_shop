from pydantic import BaseModel

class CategoryBase(BaseModel):
    name: str

class CategoryCreate(CategoryBase):
    pass

class Cetegory(CategoryBase):
    id: int
    parent_category_id: int

    class Config:
        orm_mode = True
