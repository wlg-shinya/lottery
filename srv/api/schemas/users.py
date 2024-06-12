from pydantic import BaseModel, Field
from api.schemas.common import IdBase, CreatedUpdatedAtBase, AccessTokenBase

class UsersBase():
    email: str = Field(desciption="Eメールアドレス")
    account_name: str = Field(desciption="アカウント名")
    identification: str = Field(desciption="識別情報")
    pull_lottery_ids: list[int] = Field([], desciption="ほかの人が作成したくじ引きID")

class Users(BaseModel, IdBase, CreatedUpdatedAtBase, UsersBase):
    pass

class UserCreate(BaseModel, UsersBase):
    pass

class UserCreateResponse(BaseModel, IdBase):
    pass

class UserUpdate(BaseModel, AccessTokenBase, UsersBase):
    pass

class UserUpdateResponse(BaseModel, IdBase):
    pass

class UserDelete(BaseModel, AccessTokenBase):
    pass

class UserSignin(BaseModel, UsersBase):
    pass

class UserSigninResponse(BaseModel, AccessTokenBase):
    pass

class UserChangePassword(BaseModel, AccessTokenBase):
    old_password: str = Field(desciption="現在のパスワード")
    new_password: str = Field(desciption="新しいパスワード")

class UserChangePasswordResponse(BaseModel, AccessTokenBase):
    pass

