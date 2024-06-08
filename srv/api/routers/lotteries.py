from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from api.db import db
from api.models import Lotteries as Model
import api.schemas.lotteries as schema
import api.crud.lotteries as crud
import api.crud.tokens as tokens

router = APIRouter()

@router.post("/api/create_lottery", response_model=schema.LotteryCreateResponse)
async def create_lottery(body: schema.LotteryCreate, db: AsyncSession = Depends(db)):
    await tokens.validate_token(db, body.access_token)
    return await crud.create_lottery(db, body)

@router.get("/api/read_lotteries", response_model=List[schema.Lotteries])
async def read_lotteries(db: AsyncSession = Depends(db)):
    return await crud.read_lotteries(db)

@router.get("/api/read_my_lotteries", response_model=List[schema.Lotteries])
async def read_my_lotteries(access_token: str, db: AsyncSession = Depends(db)):
    await tokens.validate_token(db, access_token)
    return await crud.read_my_lotteries(db, access_token)

@router.put("/api/update_lottery", response_model=schema.LotteryCreateResponse)
async def update_lottery(id: int, body: schema.LotteryCreate, db: AsyncSession = Depends(db)):
    await tokens.validate_token(db, body.access_token)
    model = await read_lottery_with_errorcheck(id, body.access_token, db)
    return await crud.update_lottery(db, body, original=model)

@router.delete("/api/delete_lottery", response_model=None)
async def delete_lottery(id: int, body: schema.LotteryDelete, db: AsyncSession = Depends(db)):
    await tokens.validate_token(db, body.access_token)
    model = await read_lottery_with_errorcheck(id, body.access_token, db)
    await crud.delete_lottery(db, original=model)

async def read_lottery_with_errorcheck(id: int, access_token: str, db: AsyncSession = Depends(db)) -> Model:
    model = await crud.read_lottery(db, id)
    # データが見つからない
    if model is None:
        raise HTTPException(status_code=404, detail=f"Not found id({id}) in {Model.__tablename__}")
    # アクセストークンと今回扱うデータの所有者が一致しない
    tokens_model = await tokens.read_token(db, access_token)
    if tokens_model.user_id != model.user_id:
        raise HTTPException(status_code=400, detail=f"Bad Request not match user_id in {Model.__tablename__}")
    return model

@router.delete("/api/admin/delete_lottery", response_model=None)
async def delete_lottery(id: int, db: AsyncSession = Depends(db)):
    model = await read_lottery_with_errorcheck(id, db)
    await crud.delete_lottery(db, original=model)
