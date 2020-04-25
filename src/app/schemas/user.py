from typing import Optional

from pydantic import BaseModel, EmailStr, AnyHttpUrl


# corresponding to table `user`
class UserBase(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False


# corresponding to table `userprofile`
class UserProfile(BaseModel):
    nick_name: Optional[str] = None
    telephone: Optional[str] = None
    avatar: Optional[AnyHttpUrl] = None
    age: Optional[int] = None
    sex: Optional[int] = None


# corresponding to table `userextend`
class UserExtend(BaseModel):
    signature: Optional[str] = None
    self_introduction: Optional[str] = None


# model when create user
# 创建的必要字段为 `用户名` 和 `密码`
class UserCreate(UserBase):
    username: str
    password: str


# 创建用户后的返回模型
class UserCreateResponse(UserBase):
    username: str


# model when update user
# 更新可以包括所有的字段
class UserUpdate(UserBase):
    password: Optional[str] = None

    # corresponding to `userprofile`
    profile: Optional[UserProfile] = None
    # corresponding to `userextend`
    extend: Optional[UserExtend] = None


# model when retrieve user
class User(UserBase):
    id: Optional[int] = None

    profile: Optional[UserProfile] = None
    extend: Optional[UserExtend] = None

