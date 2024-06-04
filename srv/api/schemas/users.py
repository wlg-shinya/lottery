from pydantic import BaseModel, ConfigDict, Field

class UsersBase(BaseModel):
    account_name: str = Field("", desciption="アカウント名")
    identification: str = Field("", desciption="識別情報")

class Users(UsersBase):
    id: int

    model_config = ConfigDict(from_attributes=True)

class UserCreate(UsersBase):
    pass

class UserCreateResponse(UsersBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
