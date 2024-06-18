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
) -> Model | None:
    row = (await db.execute(select(Model).filter(Model.token == token))).first()
    if row is None or len(row) == 0:
        return None
    else:
        return row.tuple()[0]

async def validate_token(
    db: AsyncSession, token: str
) -> None:
    tokens = await read_token(db=db, token=token)
    # 存在しない
    if tokens is None:
        raise HTTPException(status_code=404, detail="NotFoundException")
    # 期限切れ
    if datetime.now(default_timezone()) > tokens.expire_at:
        raise HTTPException(status_code=403, detail="ExpiredSignupTokenException")
    # 検証正常通過
    pass

async def update_token(
    db: AsyncSession, body: schema.SignupTokenCreate, original: Model
) -> Model:
    original.token = body.token
    original.email = body.email
    original.account_name = body.account_name
    original.identification = body.identification
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