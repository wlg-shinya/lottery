from pydantic import BaseModel, Field
from api.schemas.common import IdBase, CreatedUpdatedAtBase, AccessTokenBase

class UserCreateBase():
    email: str = Field(desciption="Eメールアドレス")
    account_name: str = Field(desciption="アカウント名")
    identification: str = Field(desciption="識別情報")

class UsersBase(UserCreateBase):
    pull_lottery_ids: list[int] = Field([], desciption="ほかの人が作成したくじ引きID")

class Users(BaseModel, IdBase, CreatedUpdatedAtBase, UsersBase):
    pass

class UserCreate(BaseModel, UserCreateBase):
    pass

class UserCreateResponse(BaseModel, IdBase):
    pass

class UserUpdate(BaseModel, AccessTokenBase, UsersBase):
    pass

class UserUpdateResponse(BaseModel, IdBase):
    pass

class UserDelete(BaseModel, AccessTokenBase):
    pass

class UserSignin(BaseModel, UserCreateBase):
    pass

class UserSigninResponse(BaseModel, AccessTokenBase):
    pass

class UserSignupStep2(BaseModel):
    signup_token: str = Field(desciption="サインアップトークン")

class UserChangePassword(BaseModel, AccessTokenBase):
    old_password: str = Field(desciption="現在のパスワード")
    new_password: str = Field(desciption="新しいパスワード")

class UserChangePasswordResponse(BaseModel, AccessTokenBase):
    pass

