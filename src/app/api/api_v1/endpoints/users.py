from typing import Any

from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from pydantic.networks import EmailStr
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import dependency


router = APIRouter()


@router.post("/", response_model=schemas.UserCreateResponse)
def create_user(
    *,
    db: Session = Depends(dependency.get_db),
    user_in: schemas.UserCreate,
) -> Any:
    """
    Create new user.
    """
    user = crud.user.get_by_username(db, username=user_in.username)
    if user or (user_in.email is not None and crud.user.get_by_email(db, email=user_in.email)):
        raise HTTPException(
            status_code=400,
            detail="The username or email already exists in the system.",
        )
    user = crud.user.create(db, obj_in=user_in)

    return user


@router.put("/me", response_model=schemas.User)
def update_user_me(
    *,
    db: Session = Depends(dependency.get_db),
    password: str = Body(None),
    email: EmailStr = Body(None),
    profile: schemas.UserProfile = None,
    extend: schemas.UserExtend = None,
    current_user: models.User = Depends(dependency.get_current_active_user),
) -> Any:
    """
    Update own user.
    """
    current_user_data = jsonable_encoder(current_user)
    user_in = schemas.UserUpdate(**current_user_data)
    if password is not None:
        user_in.password = password
    if email is not None:
        user_in.email = email
    if profile is not None:
        user_in.profile = profile
    if extend is not None:
        user_in.extend = extend

    return crud.user.update(db, db_obj=current_user, obj_in=user_in)


@router.get("/me", response_model=schemas.User)
def read_user_me(
    db: Session = Depends(dependency.get_db),
    current_user: models.User = Depends(dependency.get_current_active_user),
) -> Any:
    """
    Get current user.
    """
    return crud.user.get_full_info(db, current_user)


@router.get("/{user_id}", response_model=schemas.User)
def read_user_by_id(
    user_id: int,
    current_user: models.User = Depends(dependency.get_current_active_user),
    db: Session = Depends(dependency.get_db),
) -> Any:
    """
    Get a specific user by id.
    """
    user = crud.user.get(db, id=user_id)
    if user == current_user:
        return crud.user.get_full_info(db, current_user)
    if not crud.user.is_superuser(current_user):
        raise HTTPException(
            status_code=400, detail="The user doesn't have enough privileges"
        )
    return crud.user.get_full_info(db, user)


@router.put("/{user_id}", response_model=schemas.User)
def update_user(
    *,
    db: Session = Depends(dependency.get_db),
    user_id: int,
    user_in: schemas.UserUpdate,
    current_user: models.User = Depends(dependency.get_current_active_superuser),
) -> Any:
    """
    Update a user.
    """
    user = crud.user.get(db, id=user_id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user with this username does not exist in the system",
        )
    user = crud.user.update(db, db_obj=user, obj_in=user_in)
    return user