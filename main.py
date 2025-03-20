from fastapi import FastAPI
from database import create_db_and_tables
from routes.users import router as user_router
from routes.account import router as account_router

app = FastAPI()

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

app.include_router(user_router, prefix="/users", tags=["Users"])
app.include_router(account_router, prefix="/account", tags=["Account"])
