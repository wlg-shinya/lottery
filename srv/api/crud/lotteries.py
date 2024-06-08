from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from api.models import Lotteries as Model, Tokens as TokensModel
import api.schemas.lotteries as schema
import api.crud.tokens as tokens

async def create_lottery(
    db: AsyncSession, body: schema.LotteryCreate
) -> Model:
    tokens_model = await tokens.read_token(db, body.access_token)
    model = Model(user_id=tokens_model.user_id, text=body.text, title=body.title)
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

async def read_lottery_with_errorcheck(
    db: AsyncSession, id: int, access_token: str
) -> Model:
    model = await read_lottery(db, id)
    _read_lottery_not_found(model)
    tokens_model = await tokens.read_token(db, access_token)
    _read_lottery_not_match_user_id(model, tokens_model)
    return model

def _read_lottery_not_found(model: Model | None):
    # データが見つからない
    if model is None:
        raise HTTPException(status_code=404, detail=f"Not found id({id}) in {Model.__tablename__}")

def _read_lottery_not_match_user_id(model: Model, tokens_model: TokensModel):
    # アクセストークンと今回扱うデータの所有者が一致しない
    if tokens_model.user_id != model.user_id:
        raise HTTPException(status_code=400, detail=f"Bad Request not match user_id in {Model.__tablename__}")

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

async def is_lottery_id_mine(
    db: AsyncSession, id: int, access_token: str
) -> bool:
    model = await read_lottery(db, id)
    _read_lottery_not_found(model)
    tokens_model = await tokens.read_token(db, access_token)
    return tokens_model.user_id == model.user_id