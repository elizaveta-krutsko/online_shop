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


def create_category_item(db: Session,
                         item: schemas.ItemCreate,
                         category_id: int):
    db_item = models.Item(**item.dict(), item_category_id=category_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Item).offset(skip).limit(limit).all()


def delete_category_item(db: Session, item_id: int):
    db_item = db.query(models.Item).filter(models.Item.id == item_id).delete()
    db.commit()
    return db_item
