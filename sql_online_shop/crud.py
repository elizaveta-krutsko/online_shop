from sqlalchemy.orm import Session

from . import models, schemas


def get_category(db: Session, category_id: int):
    return db.query(models.Category).filter(models.Category.id == category_id).first()

def get_category_by_name(db: Session, name: str):
    return db.query(models.Category).filter(models.Category.name == name).first()

def create_category(db: Session, category: schemas.CategoryCreate):
    db_user = models.Category(name=Category.name, parent_category=Category.parent_category_id)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_category
