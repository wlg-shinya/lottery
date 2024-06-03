from fastapi import FastAPI
from api.routers import users, lotteries

app = FastAPI()
app.include_router(users.router)
app.include_router(lotteries.router)
