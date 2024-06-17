from pydantic import BaseModel, Field
from api.schemas.common import IdBase, CreatedUpdatedAtBase, AccessTokenBase

class UserSigninBase():
    email: str = Field(json_schema_extra={ "desciption": "Eメールアドレス" })
    identification: str = Field(json_schema_extra={ "desciption": "識別情報" })

class UserCreateBase(UserSigninBase):
    account_name: str = Field(json_schema_extra={ "desciption": "アカウント名" })

class UsersBase(UserCreateBase):
    pull_lottery_ids: list[int] = Field(default=[], json_schema_extra={ "desciption": "ほかの人が作成したくじ引きID" })

class Users(BaseModel, IdBase, CreatedUpdatedAtBase, UsersBase):
    pass

class UserCreate(BaseModel, UserCreateBase):
    pass

class UserUpdate(BaseModel, AccessTokenBase, UsersBase):
    pass

class UserUpdateResponse(BaseModel, AccessTokenBase):
    pass

class UserSignin(BaseModel, UserSigninBase):
    pass

class UserSigninResponse(BaseModel, AccessTokenBase):
    pass

class UserSignupStep1(BaseModel, UserCreateBase):
    pass

class UserSignupStep2(BaseModel):
    signup_token: str = Field(json_schema_extra={ "desciption": "サインアップトークン" })

class UserChangePassword(BaseModel, AccessTokenBase):
    old_password: str = Field(json_schema_extra={ "desciption": "現在のパスワード" })
    new_password: str = Field(json_schema_extra={ "desciption": "新しいパスワード" })
