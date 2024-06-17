from fastapi import APIRouter, Depends
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from core.db import db
import api.schemas.users as schema
import api.crud.users as crud
import api.crud.access_tokens as access_tokens
import api.crud.signup_tokens as signup_tokens

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

@router.post("/api/update_user", response_model=schema.UserUpdateResponse)
async def update_user(body: schema.UserUpdate, db: AsyncSession = Depends(db)):
    await access_tokens.validate_token(db=db, token=body.access_token)
    model = await crud.read_user_by_access_token(db=db, access_token=body.access_token)
    return await crud.update_user(db=db, body=body, original=model)

@router.put("/api/update_user_account_name", response_model=schema.UserUpdateResponse)
async def update_user_account_name(access_token: str, account_name: str, db: AsyncSession = Depends(db)):
    await access_tokens.validate_token(db=db, token=access_token)
    model = await crud.read_user_by_access_token(db=db, access_token=access_token)
    return await crud.update_user_account_name(db=db, account_name=account_name, original=model)

@router.put("/api/update_user_pull_lottery_ids", response_model=schema.UserUpdateResponse)
async def update_user_pull_lottery_ids(access_token: str, pull_lottery_ids: list[int], db: AsyncSession = Depends(db)):
    await access_tokens.validate_token(db=db, token=access_token)
    model = await crud.read_user_by_access_token(db=db, access_token=access_token)
    return await crud.update_user_pull_lottery_ids(db=db, pull_lottery_ids=pull_lottery_ids, original=model)

@router.delete("/api/delete_user", response_model=None)
async def delete_user(body: schema.UserDelete, db: AsyncSession = Depends(db)):
    await access_tokens.validate_token(db=db, token=body.access_token)
    model = await crud.read_user_by_access_token(db=db, access_token=body.access_token)
    await crud.delete_user(db=db, original=model)

@router.post("/api/signup_step1", response_model=None)
async def signup_step1(body: schema.UserSignupStep1, db: AsyncSession = Depends(db)):
    response = await crud.signup_step1(db=db, body=body)
    crud.send_signup_gmail(to_email=body.email, signup_token=response.signup_token)

@router.post("/api/signup_step2", response_model=None)
async def signup_step2(body: schema.UserSignupStep2, db: AsyncSession = Depends(db)):
    await signup_tokens.validate_token(db=db, token=body.signup_token)
    await crud.signup_step2(db=db, body=body)

@router.post("/api/signin", response_model=schema.UserSigninResponse)
async def signin(body: schema.UserSignin, db: AsyncSession = Depends(db)):
    return await crud.signin(db=db, body=body)

@router.post("/api/change_password", response_model=schema.UserUpdateResponse)
async def change_password(body: schema.UserChangePassword, db: AsyncSession = Depends(db)):
    return await crud.change_password(db=db, body=body)

@router.post("/api/admin/signup_step1", response_model=schema.UserSignupStep2)
async def signup_step1(body: schema.UserSignupStep1, db: AsyncSession = Depends(db)):
    return await crud.signup_step1(db=db, body=body)

@router.delete("/api/admin/delete_user", response_model=None)
async def delete_user(id: int, db: AsyncSession = Depends(db)):
    model = await crud.read_user(db=db, id=id)
    await crud.delete_user(db=db, original=model)
