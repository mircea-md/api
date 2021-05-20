from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class Role(str, Enum):
    admin = 'admin'
    dev = 'dev'
    simple = 'simple mortal'


class UserBase(BaseModel):
    first_name: str = Field(None, min_length=2, max_length=30)
    last_name: str = Field(None, min_length=2, max_length=30)
    role: Role
    is_active: bool

    class Config:
        use_enum_values = True


class UserIn(UserBase):
    password: str = Field(None, min_length=3, max_length=30)


class UserOutTmp(UserBase):
    created_at: int
    last_login: int


class UserOut(UserOutTmp):
    id: Optional[str]


class UserInDB(UserOutTmp):
    hashed_password: str
