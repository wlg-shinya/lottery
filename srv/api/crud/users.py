from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from api.models import Users as Model
import api.schemas.users as schema

async def create_user(
    db: AsyncSession, body: schema.UserCreate
) -> Model:
    model = Model(**body.model_dump())
    db.add(model)
    await db.commit()
    await db.refresh(model)
    return model

async def read_users(
    db: AsyncSession
) -> List[schema.Users]:
    result = await db.execute(select(Model.id, Model.account_name, Model.identification))
    return result.all()

async def read_user(
    db: AsyncSession, id: int
) -> Model | None:
    return await db.get(Model, id)

async def update_user(
    db: AsyncSession, body: schema.UserCreate, original: Model
) -> Model:
    original.account_name = body.account_name
    original.identification = body.identification
    db.add(original)
    await db.commit()
    await db.refresh(original)
    return original

async def delete_user(
    db: AsyncSession, original: Model
) -> None:
    await db.delete(original)
    await db.commit()