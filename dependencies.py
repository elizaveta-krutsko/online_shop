from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase

from sql_online_shop.database import SessionLocal
from fastapi import Depends
from sql_online_shop.models import User


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_user_db(session: SessionLocal = Depends(get_db)):
    yield SQLAlchemyUserDatabase(session, User)
