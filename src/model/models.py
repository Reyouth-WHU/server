from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Numeric
from sqlalchemy.orm import relationship

from database import Base, engine


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)
    email = Column(String, unique=True, index=True)
    is_active = Column(Boolean, default=False)
    profile = relationship('UserProfile', uselist=False, backref='user', cascade='all, delete-orphan', passive_deletes=True)
    extend = relationship('UserExtend', uselist=False, backref='user', cascade='all, delete-orphan', passive_deletes=True)


class UserProfile(Base):
    __tablename__ = 'user_profile'
    user_id = Column(Integer, ForeignKey('user.id', ondelete='CASCADE'))
    id = Column(Integer, primary_key=True, index=True)
    nick_name = Column(String)
    telephone_num = Column(Numeric, unique=True, index=True)
    avatar = Column(String)
    age = Column(Integer)
    sex = Column(Boolean)


class UserExtend(Base):
    __tablename__ = 'user_extend'
    user_id = Column(Integer, ForeignKey('user.id', ondelete='CASCADE'))
    id = Column(Integer, primary_key=True, index=True)
    signature = Column(String)
    self_introduction = Column(String)


Base.metadata.create_all(engine)
