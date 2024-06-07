from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from api.models import Lotteries as Model
import api.schemas.lotteries as schema
import api.crud.tokens as tokens

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
    result = await db.execute(select(Model.id, Model.user_id, Model.text, Model.title, Model.created_at, Model.updated_at))
    return result.all()

async def read_my_lotteries(
    db: AsyncSession, access_token: str
) -> List[schema.Lotteries]:
    # トークンからユーザIDを取得して自分が所有しているくじ引きデータをすべて返す
    tokens_model = await tokens.read_token(db, access_token)
    result = await db.execute(
        select(Model.id, Model.user_id, Model.text, Model.title, Model.created_at, Model.updated_at)
        .filter(Model.user_id == tokens_model.user_id)
        )
    return result.all()

async def read_lottery(
    db: AsyncSession, id: int
) -> Model | None:
    return await db.get(Model, id)

async def update_lottery(
    db: AsyncSession, body: schema.LotteryCreate, original: Model
) -> Model:
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