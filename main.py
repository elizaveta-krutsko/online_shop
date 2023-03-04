from fastapi import Depends, FastAPI
from fastapi_users import FastAPIUsers
from auth import auth_backend, get_user_manager
from routers import category, item, user
from dependencies import get_db, get_user_db
from sql_online_shop.models import User
from sql_online_shop.schemas import UserRead, UserCreate, UserUpdate

app = FastAPI(dependencies=[Depends(get_db), Depends(get_user_db)])


fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)


app.include_router(category.router)
app.include_router(item.router)
app.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["users"],
)
app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)
