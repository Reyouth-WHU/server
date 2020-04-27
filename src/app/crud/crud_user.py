from typing import Any, Dict, Union, Optional

from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder

from app.core.security import get_password_hash, verify_password
from app.crud.base import CRUDBase
from app.models.user import User, UserProfile, UserExtend
from app.schemas.user import UserCreate, UserUpdate, UserCreateResponse, User as UserScheme
from app.db.utils import add_and_commit


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):

    def create(self, db: Session, *, obj_in: UserCreate) -> User:
        db_obj = User(
            username=obj_in.username,
            hashed_password=get_password_hash(obj_in.password),
            email=obj_in.email,
            is_active=obj_in.is_active,
            is_superuser=obj_in.is_superuser,
        )
        # 在 `userprofile` 表和 `userextend` 表同时初始化空项目
        db_obj.profile = UserProfile(user_id=db_obj.id)
        db_obj.extend = UserExtend(user_id=db_obj.id)
        add_and_commit(db, db_obj)
        return db_obj

    def update(
        self,
        db: Session,
        *,
        db_obj: User,
        obj_in: Union[UserUpdate, Dict[str, Any]]
    ) -> UserScheme:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        if update_data["password"]:
            hashed_password = get_password_hash(update_data["password"])
            del update_data["password"]
            update_data["hashed_password"] = hashed_password

        # update `userprofile` table
        # db_profile = self.update_once(db_obj.profile, update_data.get("profile"))
        if update_data.get("profile"):
            self.update_once(db_obj.profile, update_data.get("profile"))
            del update_data["profile"]
        # update `userextend` table
        if update_data.get("extend"):
            self.update_once(db_obj.extend, update_data.get("extend"))
            del update_data["extend"]
        # update `user` table
        self.update_once(db_obj, update_data)
        add_and_commit(db, db_obj)
        return self.get_full_info(db, db_obj)

    def remove(self, db: Session, *, id: int) -> User:
        user = db.query(self.model).get(id)
        user_info = self.get_full_info(db, user)
        db.delete(user)
        db.query(UserProfile).filter(UserProfile.user_id == user.id).delete()
        db.query(UserExtend).filter(UserExtend.user_id == user.id).delete()
        db.commit()
        return user_info

    def get_by_username(self, db: Session, username: str) -> User:
        return db.query(self.model).filter(self.model.username == username).first()

    def get_by_email(self, db: Session, email: str) -> User:
        return db.query(self.model).filter(self.model.email == email).first()

    def get_full_info(self, db: Session, user: User) -> UserScheme:
        profile = db.query(UserProfile).filter(UserProfile.user_id == user.id).first()
        extend = db.query(UserExtend).filter(UserExtend.user_id == user.id).first()

        user_data = jsonable_encoder(user)
        profile_data = jsonable_encoder(profile)
        extend_data = jsonable_encoder(extend)

        full_info = UserScheme(**user_data)
        full_info.profile = profile_data
        full_info.extend = extend_data

        return full_info

    def authenticate(self, db: Session, *, username: str, password: str) -> Optional[User]:
        user = self.get_by_username(db, username=username)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

    def is_active(self, user: User) -> bool:
        return user.is_active

    def is_superuser(self, user: User) -> bool:
        return user.is_superuser


user = CRUDUser(User)
