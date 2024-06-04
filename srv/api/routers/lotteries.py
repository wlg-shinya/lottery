from fastapi import APIRouter, Depends
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
import api.schemas.lotteries as schema
import api.crud.lotteries as crud
from api.db import db

router = APIRouter()

@router.get("/api/read_lotteries", response_model=List[schema.Lotteries])
async def read_lotteries():
    return [schema.Lotteries(id=1, user_id=1, text="FOO")]

@router.post("/api/create_lottery", response_model=schema.LotteryCreateResponse)
async def create_lottery(body: schema.LotteryCreate, db: AsyncSession = Depends(db)):
    return await crud.create_lottery(db, body)
