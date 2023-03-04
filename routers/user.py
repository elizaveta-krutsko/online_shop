from fastapi import APIRouter, Query, Depends, HTTPException
from sqlalchemy.orm import Session
from sql_online_shop import crud, schemas
from dependencies import get_db
from sqlalchemy import exc
from typing import Union


router = APIRouter(
    prefix="/api/v1/users",
    tags=["users"],
)


@router.get("/", response_model=schemas.UserCreate)
def create_category_item(item: schemas.ItemBase, db: Session = Depends(get_db)):
    try:
        return crud.create_category_item(db=db, item=item)
    except exc.IntegrityError as err:
        err_msg = str(err.orig).split(':')[-1].replace('\n', '').strip()
        raise HTTPException(status_code=400, detail=err_msg)
