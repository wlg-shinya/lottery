from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from api.db import db
from api.models import Tokens as Model
import api.schemas.tokens as schema
import api.crud.tokens as crud

router = APIRouter()

# @router.put("/api/update_token", response_model=schema.TokenCreateResponse)
# async def update_token(id: int, body: schema.TokenCreate, db: AsyncSession = Depends(db)):
#     model = await db.get(Model, id)
#     return await crud.update_token(db, body, original=model)

