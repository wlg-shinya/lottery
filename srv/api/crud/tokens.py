from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from api.models import Tokens as Model
from datetime import datetime
from zoneinfo import ZoneInfo
from api.schemas.tokens import default_timezone
import api.schemas.tokens as schema

async def create_token(
    db: AsyncSession, body: schema.TokenCreate
) -> Model:
    model = Model(**body.model_dump())
    db.add(model)
    await db.commit()
    await db.refresh(model)
    return model

async def read_token(
    db: AsyncSession, access_token: str
) -> Model | None:
    row = (await db.execute(select(Model).filter(Model.access_token == access_token))).first()
    if row is None or len(row) == 0:
        return None
    else:
        return row.tuple()[0]

async def validate_token(
    db: AsyncSession, access_token: str
) -> None:
    tokens = await read_token(db, access_token)
    # 存在しない
    if tokens == None:
        raise HTTPException(status_code=401, detail=f"Unauthorized access token invalid. Retry signin.")
    # 期限切れ
    if datetime.now(default_timezone()) > tokens.expire_at:
        raise HTTPException(status_code=401, detail=f"Unauthorized access token expired. Retry signin.")
    # 検証正常通過
    pass

async def update_token(
    db: AsyncSession, body: schema.TokenCreate, original: Model
) -> Model:
    original.access_token = body.access_token
    original.user_id = body.user_id
    original.expire_at = body.expire_at
    db.add(original)
    await db.commit()
    await db.refresh(original)
    return original

async def delete_token(
    db: AsyncSession, original: Model
) -> None:
    await db.delete(original)
    await db.commit()
