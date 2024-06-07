from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from api.db import db
from api.models import Users as Model
from api.crud.tokens import validate_token
import api.schemas.users as schema
import api.crud.users as crud

router = APIRouter()

@router.get("/api/read_users", response_model=List[schema.Users])
async def read_users(db: AsyncSession = Depends(db)):
    return await crud.read_users(db)

@router.put("/api/update_user", response_model=schema.UserUpdateResponse)
async def update_user(id: int, body: schema.UserUpdate, db: AsyncSession = Depends(db)):
    await validate_token(db, body.access_token)
    model = await read_user_with_errorcheck(id, db)
    return await crud.update_user(db, body, original=model)

@router.delete("/api/delete_user", response_model=None)
async def delete_user(id: int, body: schema.UserDelete, db: AsyncSession = Depends(db)):
    await validate_token(db, body.access_token)
    model = await read_user_with_errorcheck(id, db)
    await crud.delete_user(db, original=model)

@router.post("/api/signup", response_model=None)
async def signup(body: schema.UserSignin, db: AsyncSession = Depends(db)):
    await crud.signup(db, body)

@router.post("/api/signin", response_model=schema.UserSigninResponse)
async def signin(body: schema.UserSignin, db: AsyncSession = Depends(db)):
    return await crud.signin(db, body)

async def read_user_with_errorcheck(id: int, db: AsyncSession = Depends(db)) -> Model:
    model = await crud.read_user(db, id)
    if model is None:
        raise HTTPException(status_code=404, detail=f"Not found id({id}) in users")
    return model
