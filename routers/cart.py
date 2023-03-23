from fastapi import APIRouter
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from sql_online_shop import crud, schemas
from dependencies import get_db, get_current_user, get_redis

router = APIRouter(
    prefix="/api/v1/cart",
    tags=["cart"],
)


@router.get("/", response_model=list[schemas.CartItemResponse])
def get_cart(current_user: schemas.UserRead = Depends(get_current_user),
             db: Session = Depends(get_db),
             redis=Depends(get_redis)
             ):
    username = current_user.__dict__["username"]
    cart_items = []
    redis_cart_items = redis.hgetall(username)
    for item_id in redis_cart_items.keys():
        db_item = crud.get_item(db, item_id).__dict__
        db_item["ordered_quantity"] = redis_cart_items[item_id]
        cart_items.append(db_item)

    return cart_items


@router.post("/", response_model=schemas.CartItemResponse)
def add_to_cart(
        item: schemas.CartItemCreate,
        db: Session = Depends(get_db),
        current_user: schemas.UserRead = Depends(get_current_user),
        redis=Depends(get_redis)
        ):
    db_item = crud.get_item(db, item_id=item.id)
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")

    db_item_dict = db_item.__dict__
    if item.ordered_quantity > db_item_dict["amount"]:
        raise HTTPException(status_code=404, detail=f'Max amount exceeded. Available amount: {db_item_dict["amount"]}')

    username = current_user.__dict__["username"]
    redis.hset(username, item.id, item.ordered_quantity)
    redis.expire(username, 3 * 24 * 3600)
    db_item_dict["ordered_quantity"] = item.ordered_quantity

    return db_item_dict


@router.delete("/")
def remove_from_cart(
        item: schemas.CartItemCreate,
        db: Session = Depends(get_db),
        current_user: schemas.UserRead = Depends(get_current_user),
        redis=Depends(get_redis)
        ):
    db_item = crud.get_item(db, item_id=item.id)
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")

    db_item_dict = db_item.__dict__
    username = current_user.__dict__["username"]
    redis.hdel(username, item.id)
    return f'{db_item_dict["name"]} was removed from cart.'


@router.delete("/all")
def clear_cart(
        current_user: schemas.UserRead = Depends(get_current_user),
        redis=Depends(get_redis)
        ):

    username = current_user.__dict__["username"]
    redis.delete(username)
    return f'Cart was cleared.'
