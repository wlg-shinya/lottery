from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from api.db import db
from api.models import Lotteries as Model
from api.crud.tokens import validate_token
import api.schemas.lotteries as schema
import api.crud.lotteries as crud

router = APIRouter()

@router.post("/api/create_lottery", response_model=schema.LotteryCreateResponse)
async def create_lottery(body: schema.LotteryCreate, db: AsyncSession = Depends(db)):
    await validate_token(db, body.access_token)
    return await crud.create_lottery(db, body)

@router.get("/api/read_lotteries", response_model=List[schema.Lotteries])
async def read_lotteries(db: AsyncSession = Depends(db)):
    return await crud.read_lotteries(db)

@router.get("/api/read_my_lotteries", response_model=List[schema.Lotteries])
async def read_my_lotteries(access_token: str, db: AsyncSession = Depends(db)):
    await validate_token(db, access_token)
    return await crud.read_my_lotteries(db, access_token)

@router.put("/api/update_lottery", response_model=schema.LotteryCreateResponse)
async def update_lottery(id: int, body: schema.LotteryCreate, db: AsyncSession = Depends(db)):
    await validate_token(db, body.access_token)
    model = await read_lottery_with_errorcheck(id, db)
    return await crud.update_lottery(db, body, original=model)

@router.delete("/api/delete_lottery", response_model=None)
async def delete_lottery(id: int, body: schema.LotteryDelete, db: AsyncSession = Depends(db)):
    await validate_token(db, body.access_token)
    model = await read_lottery_with_errorcheck(id, db)
    await crud.delete_lottery(db, original=model)

async def read_lottery_with_errorcheck(id: int, db: AsyncSession = Depends(db)) -> Model:
    model = await crud.read_lottery(db, id)
    if model is None:
        raise HTTPException(status_code=404, detail=f"Not found id({id}) in {Model.__tablename__}")
    return model
