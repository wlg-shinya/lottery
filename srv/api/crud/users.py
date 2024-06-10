from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from api.models import Users as Model
from hashlib import sha256
from api.schemas.tokens import TokenCreate
import api.schemas.users as schema
import api.crud.tokens as tokens

async def create_user(
    db: AsyncSession, body: schema.UserCreate
) -> Model:
    model = Model(account_name=body.account_name, identification=hash(body.account_name, body.identification))
    db.add(model)
    await db.commit()
    await db.refresh(model)
    return model

async def read_users(
    db: AsyncSession
) -> List[schema.Users]:
    result = await db.execute(select(Model.id, Model.account_name, Model.identification, Model.created_at, Model.updated_at))
    return result.all()

async def read_user(
    db: AsyncSession, id: int
) -> Model:
    model = await db.get(Model, id)
    if model is None:
        raise HTTPException(status_code=404, detail=f"Not found id({id}) in {Model.__tablename__}")
    return model

async def read_user_by_access_token(
    db: AsyncSession, access_token: str
) -> Model:
    tokens_model = await tokens.read_token(db, access_token)
    return await read_user(db, tokens_model.user_id)

async def update_user(
    db: AsyncSession, body: schema.UserCreate, original: Model
) -> Model:
    original.account_name = body.account_name
    original.identification = hash(body.account_name, body.identification)
    db.add(original)
    await db.commit()
    await db.refresh(original)
    return original

async def delete_user(
    db: AsyncSession, original: Model
) -> None:
    await db.delete(original)
    await db.commit()

async def signup(
    db: AsyncSession, body: schema.UserSignin
) -> None:
    result = (await db.execute(select(Model).filter(Model.account_name == body.account_name)))
    if len(result.all()) > 0:
        raise HTTPException(status_code=400, detail=f"Bad Request already exists account_name({body.account_name})")
    await create_user(db, body=schema.UserCreate(account_name=body.account_name, identification=body.identification))

async def signin(
    db: AsyncSession, body: schema.UserSignin
) -> schema.UserSigninResponse:
    # アカウントマッチング
    access_token = hash(body.account_name, body.identification)
    row = (await db.execute(select(Model).filter(Model.account_name == body.account_name, Model.identification == access_token))).first()
    if row is None or len(row) == 0:
        raise HTTPException(status_code=404, detail="Not found account or password")
    users = row.tuple()[0]
    
    # トークン新規作成/更新
    tokens_body = TokenCreate(access_token=access_token, user_id=users.id)
    tokens_model = await tokens.read_token(db, access_token)
    if tokens_model != None:
        # すでに存在しているならトークン有効期限を更新
        await tokens.update_token(db, tokens_body, tokens_model)
    else:
        # 存在していないならトークン新規作成
        await tokens.create_token(db, tokens_body)

    return schema.UserSigninResponse(access_token=access_token)

def hash(account_name: str, identification: str):
    src = account_name + identification # TODO:salt/pepperの検討
    return sha256(src.encode("utf-8")).hexdigest()