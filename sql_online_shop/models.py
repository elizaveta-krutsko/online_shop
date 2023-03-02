from sqlalchemy import Column, ForeignKey, Integer, String, FLOAT
from sqlalchemy.orm import relationship
from sql_online_shop.database import Base


class Category(Base):
    """Category info"""
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True)
    name = Column(String(90), unique=True)
    parent_category_id = Column(Integer, ForeignKey("categories.id", ondelete='RESTRICT'))


class Item(Base):
    """Item info"""
    __tablename__ = "items"

    id = Column(Integer, primary_key=True)
    name = Column(String(90), unique=True)
    unit_price = Column(FLOAT(8))
    amount = Column(Integer)
    item_category_id = Column(Integer, ForeignKey("categories.id", ondelete='RESTRICT'))

    related_category = relationship("Category", backref="items", passive_deletes=True)
