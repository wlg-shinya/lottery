from fastapi import APIRouter, Depends
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from api.db import db
import api.schemas.users as schema
import api.crud.users as crud
import api.crud.tokens as tokens

router = APIRouter()

@router.get("/api/read_users", response_model=List[schema.Users])
async def read_users(db: AsyncSession = Depends(db)):
    return await crud.read_users(db=db)

@router.get("/api/read_user", response_model=schema.Users)
async def read_user(id: int, db: AsyncSession = Depends(db)):
    return await crud.read_user(db=db, id=id)

@router.get("/api/read_user_by_access_token", response_model=schema.Users)
async def read_user_by_access_token(access_token: str, db: AsyncSession = Depends(db)):
    return await crud.read_user_by_access_token(db=db, access_token=access_token)

@router.put("/api/update_user", response_model=schema.UserUpdateResponse)
async def update_user(body: schema.UserUpdate, db: AsyncSession = Depends(db)):
    await tokens.validate_token(db=db, access_token=body.access_token)
    model = await crud.read_user_by_access_token(db=db, access_token=body.access_token)
    return await crud.update_user(db=db, body=body, original=model)

@router.delete("/api/delete_user", response_model=None)
async def delete_user(body: schema.UserDelete, db: AsyncSession = Depends(db)):
    await tokens.validate_token(db, body.access_token)
    model = await crud.read_user_by_access_token(db=db, access_token=body.access_token)
    await crud.delete_user(db=db, original=model)

@router.post("/api/signup", response_model=None)
async def signup(body: schema.UserSignin, db: AsyncSession = Depends(db)):
    await crud.signup(db=db, body=body)

@router.post("/api/signin", response_model=schema.UserSigninResponse)
async def signin(body: schema.UserSignin, db: AsyncSession = Depends(db)):
    return await crud.signin(db=db, body=body)

@router.delete("/api/admin/delete_user", response_model=None)
async def delete_user(id: int, db: AsyncSession = Depends(db)):
    model = await crud.read_user(db=db, id=id)
    await crud.delete_user(db=db, original=model)