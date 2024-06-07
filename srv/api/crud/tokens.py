from sqlalchemy.ext.asyncio import AsyncSession
from api.models import Tokens as Model
from hashlib import sha256
from datetime import datetime
import api.schemas.tokens as schema

async def create_token(
    db: AsyncSession, body: schema.TokenCreate
) -> Model:
    access_token = sha256(body.src)
    model = Model(access_token=access_token, user_id=body.user_id, expire_at=body.expire_at)
    db.add(model)
    await db.commit()
    await db.refresh(model)
    return model

async def validate_token(
    db: AsyncSession, access_token: str
) -> bool:
    tokens = await db.get(Model, access_token)
    # 存在しない
    if (tokens == None):
        return False
    # 期限切れ
    if (datetime.now() > tokens.expire_at):
        return False
    # 検証正常通過
    return True

async def update_token_expire(
    db: AsyncSession, expire_at: datetime, original: Model
) -> Model:
    original.expire_at = expire_at
    db.add(original)
    await db.commit()
    await db.refresh(original)
    return original

async def delete_token(
    db: AsyncSession, original: Model
) -> None:
    await db.delete(original)
    await db.commit()
