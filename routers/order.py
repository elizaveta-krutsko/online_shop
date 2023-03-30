from fastapi import APIRouter
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from sql_online_shop import crud, schemas
from sqlalchemy import exc
from dependencies import get_db, get_current_user, get_redis

router = APIRouter(
    prefix="/api/v1/order",
    tags=["order"],
)


@router.post("/", response_model=schemas.Order)
def create_order(
        db: Session = Depends(get_db),
        current_user: schemas.UserRead = Depends(get_current_user),
        redis=Depends(get_redis),
        is_been_paid: bool = Body(...)
        ):

    # берем юзера с токена
    username = current_user.__dict__["username"]

# по username вытаскиваем товары из корзины
    cart_items = []
    redis_cart_items = redis.hgetall(username)
    if redis_cart_items:
        for item_id in redis_cart_items.keys():
            db_item = crud.get_item(db, item_id).__dict__
            db_item["ordered_quantity"] = redis_cart_items[item_id]
            cart_items.append(db_item)
    else:
        raise HTTPException(status_code=404, detail="Cart is empty")

# создаем заказ
    try:
        return crud.create_order(db, is_been_paid, username, cart_items)

        # чистим корзину этого юзера
        redis.delete(username)

    except exc.IntegrityError as err:
        err_msg = str(err.orig).split(':')[-1].replace('\n', '').strip()
        raise HTTPException(status_code=400, detail=err_msg)