from typing import List
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


@router.post("/")
def create_order(
        is_been_paid_flag: schemas.OrderIsBeenPaid,
        db: Session = Depends(get_db),
        current_user: schemas.UserRead = Depends(get_current_user),
        redis=Depends(get_redis)
        ):

    # берем юзера с токена
    username = current_user.username

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
        db_order_id = crud.create_order(db=db, is_been_paid_flag=is_been_paid_flag, username=username, cart_items=cart_items)
    except exc.IntegrityError as err:
        err_msg = str(err.orig).split(':')[-1].replace('\n', '').strip()
        raise HTTPException(status_code=400, detail=err_msg)

    # чистим корзину этого юзера
    redis.delete(username)

    #отнимаем заказанное кол-во из бд при первом post (без оплаты), чтобы не было дубрирования
    if is_been_paid_flag.is_been_paid == False:
        crud.remove_ordered_quantity(db=db, order_id=db_order_id)

    return f'The order has been placed'


@router.get("/{order_id}", response_model=schemas.Order)
def get_order(order_id: int, db: Session = Depends(get_db), current_user: schemas.UserRead = Depends(get_current_user)):
    if not (db_order := crud.get_order_info(db=db, order_id=order_id)):
        raise HTTPException(status_code=404, detail="Order not found")
    return db_order


@router.get("/", response_model=List[schemas.Order])
def get_user_orders(db: Session = Depends(get_db), current_user: schemas.UserRead = Depends(get_current_user)):
    username = current_user.username
    if not (db_orders := crud.get_all_user_orders(db=db, username=username)):
        raise HTTPException(status_code=404, detail="Orders not found")
    return db_orders


@router.delete("/{order_id}")
def delete_order(order_id: int, db: Session = Depends(get_db), current_user: schemas.UserRead = Depends(get_current_user)):
    if crud.delete_order(db, order_id=order_id):
        return f'Order with id = {order_id} was successfully deleted'
    else:
        raise HTTPException(status_code=404, detail="Order not found")
