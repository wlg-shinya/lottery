from fastapi import APIRouter, Depends
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from core.db import db
import api.schemas.lotteries as schema
import api.crud.lotteries as crud
import api.crud.access_tokens as access_tokens

router = APIRouter()

@router.post("/api/create_lottery", response_model=schema.LotteryCreateResponse)
async def create_lottery(body: schema.LotteryCreate, db: AsyncSession = Depends(db)):
    await access_tokens.validate_token(db=db, token=body.access_token)
    return await crud.create_lottery(db=db, body=body)

@router.get("/api/read_lotteries", response_model=List[schema.Lotteries])
async def read_lotteries(db: AsyncSession = Depends(db)):
    return await crud.read_lotteries(db=db)

@router.get("/api/read_my_lotteries", response_model=List[schema.Lotteries])
async def read_my_lotteries(access_token: str, db: AsyncSession = Depends(db)):
    await access_tokens.validate_token(db=db, token=access_token)
    return await crud.read_my_lotteries(db=db, access_token=access_token)

@router.get("/api/read_lottery", response_model=schema.Lotteries)
async def read_lottery(id: int, db: AsyncSession = Depends(db)):
    return await crud.read_lottery(db=db, id=id)

@router.put("/api/update_lottery", response_model=schema.LotteryCreateResponse)
async def update_lottery(id: int, body: schema.LotteryCreate, db: AsyncSession = Depends(db)):
    await access_tokens.validate_token(db=db, token=body.access_token)
    model = await crud.read_my_lottery(db=db, id=id, access_token=body.access_token)
    return await crud.update_lottery(db=db, body=body, original=model)

@router.delete("/api/delete_lottery", response_model=None)
async def delete_lottery(id: int, body: schema.LotteryDelete, db: AsyncSession = Depends(db)):
    await access_tokens.validate_token(db=db, token=body.access_token)
    model = await crud.read_my_lottery(db=db, id=id, access_token=body.access_token)
    await crud.delete_lottery(db=db, original=model)

@router.get("/api/is_lottery_id_mine", response_model=bool)
async def is_lottery_id_mine(id: int, access_token: str, db: AsyncSession = Depends(db)):
    await access_tokens.validate_token(db=db, token=access_token)
    return await crud.is_lottery_id_mine(db=db, id=id, access_token=access_token)

@router.post("/api/increment_lottery_used_count", response_model=schema.LotteryCreateResponse)
async def increment_lottery_used_count(id: int, access_token: str, db: AsyncSession = Depends(db)):
    await access_tokens.validate_token(db=db, token=access_token)
    return await crud.increment_lottery_used_count(db=db, id=id)

@router.delete("/api/admin/delete_lottery", response_model=None)
async def delete_lottery(id: int, db: AsyncSession = Depends(db)):
    model = await crud.read_lottery(db=db, id=id)
    await crud.delete_lottery(db=db, original=model)
