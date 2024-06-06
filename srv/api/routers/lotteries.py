from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from api.db import db
from api.models import Lotteries as Model
import api.schemas.lotteries as schema
import api.crud.lotteries as crud

router = APIRouter()

@router.post("/api/create_lottery", response_model=schema.LotteryCreateResponse)
async def create_lottery(body: schema.LotteryCreate, db: AsyncSession = Depends(db)):
    return await crud.create_lottery(db, body)

@router.get("/api/read_lotteries", response_model=List[schema.Lotteries])
async def read_lotteries(db: AsyncSession = Depends(db)):
    return await crud.read_lotteries(db)

@router.get("/api/read_lotteries_by_user_id", response_model=List[schema.Lotteries])
async def read_lotteries_by_user_id(user_id: int, db: AsyncSession = Depends(db)):
    return await crud.read_lotteries_by_user_id(db, user_id=user_id)

@router.put("/api/update_lottery", response_model=schema.LotteryCreateResponse)
async def update_lottery(id: int, body: schema.LotteryCreate, db: AsyncSession = Depends(db)):
    model = await read_lottery_with_errorcheck(id, db)
    return await crud.update_lottery(db, body, original=model)

@router.delete("/api/delete_lottery", response_model=None)
async def delete_lottery(id: int, db: AsyncSession = Depends(db)):
    model = await read_lottery_with_errorcheck(id, db)
    await crud.delete_lottery(db, original=model)

async def read_lottery_with_errorcheck(id: int, db: AsyncSession = Depends(db)) -> Model:
    model = await crud.read_lottery(db, id=id)
    if model is None:
        raise HTTPException(status_code=404, detail=f"Not found id({id}) in lotteries")
    return model
