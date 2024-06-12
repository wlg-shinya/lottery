from datetime import datetime
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from core.config import default_timezone
from api.models import SignupTokens as Model
import api.schemas.signup_tokens as schema

async def create_token(
    db: AsyncSession, body: schema.SignupTokenCreate
) -> Model:
    model = Model(**body.model_dump())
    return await _update_model(db=db, model=model)

async def read_token(
    db: AsyncSession, token: str
) -> Model:
    row = (await db.execute(select(Model).filter(Model.token == token))).first()
    if row is None or len(row) == 0:
        raise HTTPException(status_code=401, detail=f"Unauthorized access token invalid.")
    else:
        return row.tuple()[0]

async def validate_token(
    db: AsyncSession, token: str
) -> None:
    tokens = await read_token(db=db, token=token)
    # 期限切れ
    if datetime.now(default_timezone()) > tokens.expire_at:
        raise HTTPException(status_code=401, detail=f"Unauthorized access token expired.")
    # 検証正常通過
    pass

async def update_token(
    db: AsyncSession, body: schema.SignupTokenCreate, original: Model
) -> Model:
    original.token = body.token
    original.expire_at = body.expire_at
    return await _update_model(db=db, model=original)

async def delete_token(
    db: AsyncSession, original: Model
) -> None:
    await db.delete(instance=original)
    await db.commit()

async def _update_model(db: AsyncSession, model: Model) -> Model:
    db.add(instance=model)
    await db.commit()
    await db.refresh(instance=model)
    return model