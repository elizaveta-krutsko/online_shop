from sqlalchemy.orm import Session
from . import models, schemas


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
    db_item = db.query(models.Item).filter(models.Item.id == item_id)
    if db_item.first():
        if item.name:
            db_item.update({models.Item.name: item.name}, synchronize_session=False)
        if item.unit_price:
            db_item.update({models.Item.unit_price: item.unit_price}, synchronize_session=False)
        if item.amount:
            db_item.update({models.Item.amount: item.amount}, synchronize_session=False)
        if item.item_category_id:
            db_item.update({models.Item.item_category_id: item.item_category_id}, synchronize_session=False)
        db.commit()
        return db_item


def get_item(db: Session, item_id: int):
    return db.query(models.Item).filter(models.Item.id == item_id).first()


def get_items(db: Session, item_category_id: int, skip: int = 0, limit: int = 100):
    if item_category_id:
        return db.query(models.Item).filter(models.Item.item_category_id == item_category_id).offset(skip).limit(limit).all()
    else:
        return db.query(models.Item).offset(skip).limit(limit).all()
