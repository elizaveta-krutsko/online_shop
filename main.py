from fastapi import Depends, FastAPI
from routers import category, item
from dependencies import get_db


app = FastAPI(dependencies=[Depends(get_db)])

app.include_router(category.router)
app.include_router(item.router)
