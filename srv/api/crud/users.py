from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from hashlib import sha256
from core.config import env
from api.models import Users as Model
from api.schemas.access_tokens import AccessTokenCreate, default_expire_at as access_tokens_default_expire_at
from api.schemas.signup_tokens import SignupTokenCreate, default_expire_at as signup_tokens_default_expire_at
import api.schemas.users as schema
import api.crud.access_tokens as access_tokens
import api.crud.signup_tokens as signup_tokens

async def create_user(
    db: AsyncSession, body: schema.UserCreate
) -> Model:
    model = Model(
        account_name=body.account_name, 
        identification=access_token_hash(
            email=body.email, 
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
    tokens_model = await access_tokens.read_token(db=db, token=access_token)
    return await read_user(db=db, id=tokens_model.user_id)

async def update_user(
    db: AsyncSession, body: schema.UserUpdate, original: Model
) -> Model:
    original.account_name = body.account_name
    original.identification = access_token_hash(email=body.email, identification=body.identification)
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

async def signup_step1(
    db: AsyncSession, body: schema.UserSignupStep1
) -> str:
    # すでに登録済みのEメールならはじく
    result = (await db.execute(select(Model).filter(Model.email == body.email)))
    if len(result.all()) > 0:
        raise HTTPException(status_code=400, detail=f"Bad Request already exists email({body.email})")
    # サインアップトークンの発行
    token = signup_token_hash(email=body.email, account_name=body.account_name, identification=body.identification)
    await _create_or_update_signup_token(
        db=db, 
        body=SignupTokenCreate(
            token=token,
            email=body.email,
            account_name=body.account_name,
            identification=body.identification,
            expire_at=signup_tokens_default_expire_at()
            ))
    # 認証用URL
    return f"{env().frontend_url}/signup_step2/?signup_token={token}"

async def signup_step2(
    db: AsyncSession, body: schema.UserSignupStep2
) -> None:
    tokens_model = await signup_tokens.read_token(db=db, token=body.signup_token)
    # 念のためユーザー作成直前でもEメール重複チェックを行う
    result = (await db.execute(select(Model).filter(Model.email == tokens_model.email)))
    if len(result.all()) > 0:
        raise HTTPException(status_code=400, detail=f"Bad Request already exists email({tokens_model.email})")
    # ユーザ作成
    await create_user(
        db=db, 
        body=schema.UserCreate(
            email=tokens_model.email,
            account_name=tokens_model.account_name,
            identification=tokens_model.identification
            )
        )

async def signin(
    db: AsyncSession, body: schema.UserSignin
) -> schema.UserSigninResponse:
    # アカウントマッチング
    access_token = access_token_hash(email=body.email, identification=body.identification)
    row = (await db.execute(select(Model).filter(Model.email == body.email, Model.identification == access_token))).first()
    if row is None or len(row) == 0:
        raise HTTPException(status_code=404, detail="Not found email or password")
    users = row.tuple()[0]
    
    # トークン新規作成/更新
    await _create_or_update_access_token(
        db=db, 
        body=AccessTokenCreate(
            token=access_token,
            user_id=users.id,
            expire_at=access_tokens_default_expire_at()
            ))

    return schema.UserSigninResponse(access_token=access_token)

async def change_password(
    db: AsyncSession, body: schema.UserChangePassword
) -> schema.UserChangePasswordResponse:
    # 現在のパスワードの検証
    old_model = await read_user_by_access_token(db=db, access_token=body.access_token)
    old_access_token = access_token_hash(email=old_model.email, identification=body.old_password)
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
    await _create_or_update_access_token(
        db=db, 
        body=AccessTokenCreate(
            token=new_access_token,
            user_id=new_model.id,
            expire_at=access_tokens_default_expire_at()
            ))
    
    return schema.UserChangePasswordResponse(access_token=new_access_token)

def access_token_hash(email: str, identification: str) -> str:
    src = email + identification # TODO:salt/pepperの検討
    return sha256(src.encode("utf-8")).hexdigest()

def signup_token_hash(email: str, account_name:str, identification: str) -> str:
    src = email + account_name + identification
    return sha256(src.encode("utf-8")).hexdigest()

async def _update_model(db: AsyncSession, model: Model) -> Model:
    db.add(instance=model)
    await db.commit()
    await db.refresh(instance=model)
    return model

async def _create_or_update_access_token(db: AsyncSession, body: AccessTokenCreate) -> None:
    tokens_model = await access_tokens.read_token(db=db, token=body.token)
    if tokens_model != None:
        # すでに存在しているならトークン有効期限を更新
        await access_tokens.update_token(db=db, body=body, original=tokens_model)
    else:
        # 存在していないならトークン新規作成
        await access_tokens.create_token(db=db, body=body)

async def _create_or_update_signup_token(db: AsyncSession, body: SignupTokenCreate) -> None:
    tokens_model = await signup_tokens.read_token(db=db, token=body.token)
    if tokens_model != None:
        await signup_tokens.update_token(db=db, body=body, original=tokens_model)
    else:
        await signup_tokens.create_token(db=db, body=body)