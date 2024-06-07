from pydantic import BaseModel, ConfigDict, Field
import datetime

class UsersBase(BaseModel):
    account_name: str = Field(desciption="アカウント名")
    identification: str = Field(desciption="識別情報")

class Users(UsersBase):
    id: int
    created_at: datetime.datetime = Field(desciption="作成日時")
    updated_at: datetime.datetime | None = Field(desciption="更新日時")

    model_config = ConfigDict(from_attributes=True)

class UserCreate(UsersBase):
    pass

class UserCreateResponse(UsersBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
