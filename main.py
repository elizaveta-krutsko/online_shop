from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session
from sql_online_shop import crud, models, schemas
from sql_online_shop.database import SessionLocal, engine
from sqlalchemy.dialects import postgresql
from routers import category
from dependencies import get_db


app = FastAPI(dependencies=[Depends(get_db)])

app.include_router(category.router)

