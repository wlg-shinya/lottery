from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from core.config import env
from api.routers import users, lotteries

app = FastAPI(
    openapi_url=env().openapi_url,
    docs_url=env().docs_url,
    redoc_url=env().redoc_url,
)
app.include_router(users.router)
app.include_router(lotteries.router)

# CORS対応
origins = [env().frontend_url]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)