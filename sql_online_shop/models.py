from sqlalchemy import Column, ForeignKey, Integer, String, FLOAT, Boolean, DateTime, func
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

    #many to many with Orders
    all_orders = relationship("OrderItem", back_populates="my_item", passive_deletes=True)


class User(Base):
    """User account"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String(90), unique=True)
    username = Column(String(90), unique=True, nullable=False)
    first_name = Column(String(90))
    last_name = Column(String(90))
    registered_at = Column(DateTime(), nullable=False, server_default=func.now())
    hashed_password = Column(String(length=1024), nullable=False)
    is_superuser = Column(Boolean, default=False, nullable=False)

    # one to many with Order
    user_order = relationship("Order", back_populates="order_user", cascade='save-update, merge, delete', passive_deletes=True)


class Order(Base):
    """"Order details"""
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(DateTime(), nullable=False, server_default=func.now())
    is_been_paid = Column(Boolean, nullable=False)
    expired_at = Column(DateTime())
    total_order_cost = Column(FLOAT(8))

    # one to many with User
    order_user = relationship("User", back_populates="user_order")

    #many to many with Item
    all_items = relationship("OrderItem", back_populates="my_order", cascade="all, delete")


class OrderItem(Base):
    """"Association table"""
    __tablename__ = "order_item"

    order_id = Column(ForeignKey('orders.id', ondelete="CASCADE"), primary_key=True)
    item_id = Column(ForeignKey('items.id', ondelete="CASCADE"), primary_key=True)
    ordered_quantity = Column(Integer, nullable=False)
    total_item_cost = Column(FLOAT(8))

    # many to many with Item and Order
    my_item = relationship("Item", back_populates="all_orders")
    my_order = relationship("Order", back_populates="all_items")
