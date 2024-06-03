from fastapi import APIRouter
from typing import List
import api.schemas.lotteries as schema

router = APIRouter()

@router.get("/api/read_lotteries", response_model=List[schema.Lotteries])
async def read_lotteries():
    return [schema.Lotteries(id=1, user_id=1, text="FOO")]

@router.post("/api/create_lottery", response_model=schema.LotteryCreateResponse)
async def create_lottery(body: schema.LotteryCreate):
    return schema.LotteryCreateResponse(id=1, **body.model_dump())
