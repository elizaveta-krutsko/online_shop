from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sql_online_shop.database import Base

class Category(Base):
    """"Category info"""
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True)
    name = Column(String(90), unique=True)
    parent_category_id = Column(Integer, ForeignKey("categories.id", ondelete='RESTRICT'))

    # self_referential_one_to_many
    # parent_category = relationship("Category")




