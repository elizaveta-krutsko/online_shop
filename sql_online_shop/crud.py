from sqlalchemy.orm import Session
from . import models, schemas
from typing import Union
import utils
from datetime import datetime, timedelta
from sqlalchemy.orm import joinedload


def get_category(db: Session, category_id: int):
    return db.query(models.Category).filter(models.Category.id == category_id).first()


def get_category_child_list(db: Session, category_id: int):
    db_category = db.query(models.Category).filter(models.Category.id == category_id).first()
    db_category.child_categories = list(db.query(models.Category).with_entities(
        models.Category.id, models.Category.name).filter(models.Category.parent_category_id == category_id))
    return db_category


def get_categories(db: Session, skip: int = 0, limit: int = 100):
    db_categories = db.query(models.Category).offset(skip).limit(limit).all()
    return db_categories


def create_category(db: Session, category: schemas.CategoryCreate):
    db_category = models.Category(name=category.name, parent_category_id=category.parent_category_id)
    db.add(db_category)
    db.commit()
    return db_category


def delete_category(db: Session, category_id: int):
    db_category = db.query(models.Category).filter(models.Category.id == category_id).delete()
    db.commit()
    return db_category


def update_category(db: Session, category_id: int, category: schemas.CategoryUpdate):
    db_category = db.query(models.Category).filter(models.Category.id == category_id)
    if db_category.first():
        if category.name:
            db_category.update({models.Category.name: category.name}, synchronize_session=False)
        if category.parent_category_id:
            db_category.update({models.Category.parent_category_id: category.parent_category_id}, synchronize_session=False)
        db.commit()
        return db_category


# crud for items
def create_category_item(db: Session, item: schemas.ItemBase):
    db_item = models.Item(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def delete_category_item(db: Session, item_id: int):
    db_item = db.query(models.Item).filter(models.Item.id == item_id).delete()
    db.commit()
    return db_item


def update_item(db: Session, item_id: int, item: schemas.ItemUpdate):
    item_dict = item.dict(exclude_unset=True)
    db_item_query = db.query(models.Item).filter(models.Item.id == item_id)
    db_item = db_item_query.first()
    if db_item:
        db_item_query.filter(models.Item.id == item_id).update(item_dict,synchronize_session=False)
        db.commit()
        db.refresh(db_item)
        return db_item


def get_item(db: Session, item_id: int):
    return db.query(models.Item).filter(models.Item.id == item_id).first()


def get_items(db: Session, item_category_id: Union[list, None], skip: int = 0, limit: int = 100):
    if item_category_id:
        item_category_id_list = item_category_id[0].split(',')
        return db.query(models.Item).filter(models.Item.item_category_id.in_(item_category_id_list)).offset(skip).limit(
                limit).all()
    else:
        return db.query(models.Item).offset(skip).limit(limit).all()


# USERS
def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = utils.get_password_hash(user.password)
    user_data = user.dict()
    del user_data["password"]
    user_data["hashed_password"] = hashed_password
    db_user = models.User(**user_data)
    db.add(db_user)
    db.commit()
    return db_user


def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def delete_user(db: Session, user_id: int):
    db_user = db.query(models.User).filter(models.User.id == user_id).delete()
    db.commit()
    return db_user


def update_user(db: Session, user_id: int, user: schemas.UserUpdate):
    print(type(user))
    user_dict = user.dict(exclude_unset=True)
    db_user_query = db.query(models.User).filter(models.User.id == user_id)
    db_user = db_user_query.first()
    if db_user:
        db_user_query.filter(models.User.id == user_id).update(user_dict, synchronize_session=False)
        db.commit()
        db.refresh(db_user)
        return db_user


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    db_users = db.query(models.User).offset(skip).limit(limit).all()
    return db_users


#ORDERS
def create_order(db: Session, is_been_paid_flag: schemas.OrderIsBeenPaid, username: str, cart_items: list):
    # ищем id юзера
    id_user = db.query(models.User).filter(models.User.username == username).first().__dict__['id']

    # проверяем наличие указанного кол-ва товара для заказа на складе
    for item in cart_items:
        db_item = db.query(models.Item).filter(models.Item.id == item['id']).first()
        if int(item['ordered_quantity']) > db_item.amount:
            item['ordered_quantity'] = str(db_item.amount)

    # считаем стоимость каждого товара в корзине
    for item in cart_items:
        item['total_item_cost'] = float(item['unit_price']) * int(item['ordered_quantity'])

    # считаем итоговую стоимость заказа
    total_order_cost = 0
    for item in cart_items:
        total_order_cost += item['total_item_cost']

    # берем флаг оплаты заказа с Body запроса
    is_been_paid_dict = is_been_paid_flag.dict(exclude_unset=True)

    #создаем заказ
    db_order = models.Order(
        user_id=id_user,
        expired_at=(datetime.utcnow() + timedelta(minutes=30)),
        total_order_cost=total_order_cost,
        is_been_paid=is_been_paid_dict['is_been_paid']
    )
    db.add(db_order)
    db.flush()

    # создаем связи
    for item in cart_items:
        db_item_order = models.OrderItem(
            order_id=db_order.id,
            item_id=item['id'],
            ordered_quantity=item['ordered_quantity'],
            total_item_cost=item['total_item_cost']
        )
        db.add(db_item_order)

    db.commit()
    return db_order.id


def get_order_info(db: Session, order_id: int):
    db_order = db.query(models.Order).options(
        joinedload(models.Order.all_items).options(
            joinedload(models.OrderItem.my_item)
        )
    ).where(models.Order.id == order_id).one()
    return db_order


def get_all_user_orders(db: Session, username: str):
    id_user = db.query(models.User).filter(models.User.username == username).first().__dict__['id']
    db_orders = db.query(models.Order).options(
        joinedload(models.Order.all_items).options(
            joinedload(models.OrderItem.my_item)
        )
    ).where(models.Order.user_id == id_user).all()
    return db_orders


def delete_order(db: Session, order_id: int):
    db_order = db.query(models.Order).filter(models.Order.id == order_id).delete()
    db.commit()
    return db_order


def remove_ordered_quantity(db: Session, order_id: int):
    db_order_items = db.query(models.OrderItem).filter(models.OrderItem.order_id == order_id).all()
    for item in db_order_items:
        db_item = db.query(models.Item).filter(models.Item.id == item.item_id).first()
        db_item.amount -= item.ordered_quantity
        db.commit()


def add_ordered_quantity(db: Session, order_id: int):
    db_order_items = db.query(models.OrderItem).filter(models.OrderItem.order_id == order_id).all()
    for item in db_order_items:
        db_item = db.query(models.Item).filter(models.Item.id == item.item_id).first()
        db_item.amount += item.ordered_quantity
        db.commit()


def remove_expired_orders(db: Session):
    db_expired_orders = db.query(models.Order).filter(models.Order.expired_at < datetime.utcnow()).all()
    for order in db_expired_orders:
        db.query(models.Order).filter(models.Order.id == order.id).delete()
    db.commit()
    return f'function completed'
