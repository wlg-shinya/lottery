from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime

class UsersBase(BaseModel):
    account_name: str = Field(desciption="アカウント名")
    identification: str = Field(desciption="識別情報")
    pull_lottery_ids: list[int] = Field(desciption="ほかの人が作成したくじ引きID")

class Users(UsersBase):
    id: int
    created_at: datetime = Field(desciption="作成日時")
    updated_at: datetime | None = Field(desciption="更新日時")

    model_config = ConfigDict(from_attributes=True)

class UserCreate(UsersBase):
    pass

class UserCreateResponse(UserCreate):
    id: int

    model_config = ConfigDict(from_attributes=True)

class UserUpdate(UsersBase):
    access_token: str = Field(desciption="アクセストークン")

class UserUpdateResponse(UserUpdate):
    id: int

    model_config = ConfigDict(from_attributes=True)

class UserDelete(BaseModel):
    access_token: str = Field(desciption="アクセストークン")

class UserSignin(UsersBase):
    pass

class UserSigninResponse(BaseModel):
    access_token: str = Field(desciption="アクセストークン")

