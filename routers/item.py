from fastapi import APIRouter
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from sql_online_shop import crud, schemas
from dependencies import get_db
from sqlalchemy import exc


router = APIRouter(
    prefix="/api/v1/categories",
    tags=["items"],
)


@router.post("/{category_id}/items/", response_model=schemas.Item)
def create_category_item(category_id: int, item: schemas.ItemCreate,
                         db: Session = Depends(get_db)):
    try:
        return crud.create_category_item(db=db, item=item, category_id=category_id)
    except exc.IntegrityError as err:
        err_msg = str(err.orig).split(':')[-1].replace('\n', '').strip()
        raise HTTPException(status_code=400, detail=err_msg)


@router.get("/items/", response_model=list[schemas.Item])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_items(db, skip=skip, limit=limit)