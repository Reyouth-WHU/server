from sqlalchemy import Boolean, Column, Integer, String, SMALLINT, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class User(Base):
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    email = Column(String, unique=True, index=True)
    is_active = Column(Boolean(), default=True)
    is_superuser = Column(Boolean(), default=False)

    # profile of user, one-to-one relationship
    profile = relationship("UserProfile", uselist=False, backref="user")
    # extend info of user, one-to-one relationship
    extend = relationship("UserExtend", uselist=False, backref="user")


class UserProfile(Base):
    id = Column(Integer, primary_key=True, index=True)
    nick_name = Column(String)
    telephone = Column(String, unique=True, index=True)
    avatar = Column(String)
    age = Column(SMALLINT)
    # 0 for man, 1 for woman, 2 for other
    sex = Column(SMALLINT)

    # foreign key
    user_id = Column(Integer, ForeignKey("user.id"))


class UserExtend(Base):
    id = Column(Integer, primary_key=True, index=True)
    signature = Column(String)
    self_introduction = Column(String)

    # foreign key
    user_id = Column(Integer, ForeignKey("user.id"))

