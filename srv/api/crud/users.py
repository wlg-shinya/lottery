from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from api.models import Users as Model
from hashlib import sha256
from api.schemas.access_token import AccessTokenCreate
import api.schemas.users as schema
import api.crud.access_token as access_token

async def create_user(
    db: AsyncSession, body: schema.UserCreate
) -> Model:
    model = Model(
        account_name=body.account_name, 
        identification=hash(
            account_name=body.account_name, 
            identification=body.identification
            ), 
        pull_lottery_ids=[]
        )
    return await _update_model(db=db, model=model)

async def read_users(
    db: AsyncSession
) -> List[schema.Users]:
    result = await db.execute(select(Model.id, Model.account_name, Model.identification, Model.pull_lottery_ids, Model.created_at, Model.updated_at))
    return result.all()

async def read_user(
    db: AsyncSession, id: int
) -> Model:
    model = await db.get(entity=Model, ident=id)
    if model is None:
        raise HTTPException(status_code=404, detail=f"Not found id({id}) in {Model.__tablename__}")
    return model

async def read_user_by_access_token(
    db: AsyncSession, access_token: str
) -> Model:
    tokens_model = await access_token.read_token(db=db, access_token=access_token)
    return await read_user(db=db, id=tokens_model.user_id)

async def update_user(
    db: AsyncSession, body: schema.UserUpdate, original: Model
) -> Model:
    original.account_name = body.account_name
    original.identification = hash(account_name=body.account_name, identification=body.identification)
    original.pull_lottery_ids = body.pull_lottery_ids
    return await _update_model(db=db, model=original)

async def update_user_pull_lottery_ids(
    db: AsyncSession, pull_lottery_ids: list[int], original: Model
) -> Model:
    original.pull_lottery_ids = pull_lottery_ids
    return await _update_model(db=db, model=original)

async def delete_user(
    db: AsyncSession, original: Model
) -> None:
    await db.delete(instance=original)
    await db.commit()

async def signup(
    db: AsyncSession, body: schema.UserSignin
) -> None:
    result = (await db.execute(select(Model).filter(Model.account_name == body.account_name)))
    if len(result.all()) > 0:
        raise HTTPException(status_code=400, detail=f"Bad Request already exists account_name({body.account_name})")
    await create_user(db, schema.UserCreate(account_name=body.account_name, identification=body.identification))

async def signin(
    db: AsyncSession, body: schema.UserSignin
) -> schema.UserSigninResponse:
    # アカウントマッチング
    access_token = hash(account_name=body.account_name, identification=body.identification)
    row = (await db.execute(select(Model).filter(Model.account_name == body.account_name, Model.identification == access_token))).first()
    if row is None or len(row) == 0:
        raise HTTPException(status_code=404, detail="Not found account or password")
    users = row.tuple()[0]
    
    # トークン新規作成/更新
    await _create_or_update_token(db=db, access_token=access_token, id=users.id)

    return schema.UserSigninResponse(access_token=access_token)

async def change_password(
    db: AsyncSession, body: schema.UserChangePassword
) -> schema.UserChangePasswordResponse:
    # 現在のパスワードの検証
    old_model = await read_user_by_access_token(db=db, access_token=body.access_token)
    old_access_token = hash(account_name=old_model.account_name, identification=body.old_password)
    if old_access_token != old_model.identification:
        raise HTTPException(status_code=401, detail="Unauthorized")
    # 検証を通過したので新しいパスワードでユーザーを更新
    new_model = await update_user(
        db=db, 
        body=schema.UserUpdate(
            account_name=old_model.account_name,
            identification=body.new_password,
            pull_lottery_ids=old_model.pull_lottery_ids,
            access_token=body.access_token
            ), 
        original=old_model
        )
    new_access_token = new_model.identification
    # トークン新規作成/更新
    await _create_or_update_token(db=db, access_token=new_access_token, id=new_model.id)
    
    return schema.UserChangePasswordResponse(access_token=new_access_token)

def hash(account_name: str, identification: str) -> str:
    src = account_name + identification # TODO:salt/pepperの検討
    return sha256(src.encode("utf-8")).hexdigest()

async def _update_model(db: AsyncSession, model: Model) -> Model:
    db.add(instance=model)
    await db.commit()
    await db.refresh(instance=model)
    return model

async def _create_or_update_token(db: AsyncSession, access_token: str, id: int) -> None:
    tokens_body = AccessTokenCreate(access_token=access_token, user_id=id)
    tokens_model = await access_token.read_token(db=db, access_token=access_token)
    if tokens_model != None:
        # すでに存在しているならトークン有効期限を更新
        await access_token.update_token(db=db, body=tokens_body, original=tokens_model)
    else:
        # 存在していないならトークン新規作成
        await access_token.create_token(db=db, body=tokens_body)