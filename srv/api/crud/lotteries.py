from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from api.models import Lotteries as Model
import api.schemas.lotteries as schema

async def create_lottery(
    db: AsyncSession, body: schema.LotteryCreate
) -> Model:
    model = Model(**body.model_dump())
    db.add(model)
    await db.commit()
    await db.refresh(model)
    return model

async def read_lotteries(
    db: AsyncSession
) -> List[schema.Lotteries]:
    result = await db.execute(select(Model.id, Model.user_id, Model.text, Model.title))
    return result.all()

async def read_lottery(
    db: AsyncSession, id: int
) -> Model | None:
    return await db.get(Model, id)

async def update_lottery(
    db: AsyncSession, body: schema.LotteryCreate, original: Model
) -> Model:
    original.user_id = body.user_id
    original.text = body.text
    original.title = body.title
    db.add(original)
    await db.commit()
    await db.refresh(original)
    return original

async def delete_lottery(
    db: AsyncSession, original: Model
) -> None:
    await db.delete(original)
    await db.commit()