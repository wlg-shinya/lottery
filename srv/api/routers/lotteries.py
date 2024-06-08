from fastapi import APIRouter, Depends
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from api.db import db
import api.schemas.lotteries as schema
import api.crud.lotteries as crud
import api.crud.tokens as tokens

router = APIRouter()

@router.post("/api/create_lottery", response_model=schema.LotteryCreateResponse)
async def create_lottery(body: schema.LotteryCreate, db: AsyncSession = Depends(db)):
    await tokens.validate_token(db=db, access_token=body.access_token)
    return await crud.create_lottery(db=db, body=body)

@router.get("/api/read_lotteries", response_model=List[schema.Lotteries])
async def read_lotteries(db: AsyncSession = Depends(db)):
    return await crud.read_lotteries(db=db)

@router.get("/api/read_my_lotteries", response_model=List[schema.Lotteries])
async def read_my_lotteries(access_token: str, db: AsyncSession = Depends(db)):
    await tokens.validate_token(db=db, access_token=access_token)
    return await crud.read_my_lotteries(db=db, access_token=access_token)

@router.put("/api/update_lottery", response_model=schema.LotteryCreateResponse)
async def update_lottery(id: int, body: schema.LotteryCreate, db: AsyncSession = Depends(db)):
    await tokens.validate_token(db=db, access_token=body.access_token)
    model = await crud.read_lottery_with_errorcheck(db=db, id=id, access_token=body.access_token)
    return await crud.update_lottery(db=db, body=body, original=model)

@router.delete("/api/delete_lottery", response_model=None)
async def delete_lottery(id: int, body: schema.LotteryDelete, db: AsyncSession = Depends(db)):
    await tokens.validate_token(db=db, access_token=body.access_token)
    model = await crud.read_lottery_with_errorcheck(db=db, id=id, access_token=body.access_token)
    await crud.delete_lottery(db=db, original=model)

@router.get("/api/is_lottery_id_mine", response_model=bool)
async def is_lottery_id_mine(id: int, access_token: str, db: AsyncSession = Depends(db)):
    await tokens.validate_token(db=db, access_token=access_token)
    return await crud.is_lottery_id_mine(db=db, id=id, access_token=access_token)

@router.delete("/api/admin/delete_lottery", response_model=None)
async def delete_lottery(id: int, db: AsyncSession = Depends(db)):
    model = await crud.read_lottery(db=db, id=id)
    await crud.delete_lottery(db=db, original=model)
