from fastapi import Depends, FastAPI
from routers import category, item, user, cart
from dependencies import get_db
import uvicorn


app = FastAPI(dependencies=[Depends(get_db)])


app.include_router(category.router)
app.include_router(item.router)
app.include_router(user.router)
app.include_router(cart.router)

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
