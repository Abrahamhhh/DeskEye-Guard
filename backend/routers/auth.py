from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from database import get_db
from models import User
from schemas import PasswordChange, Token, UserCreate, UserLogin, UserOut
from services.auth_service import CurrentUser, create_access_token, get_password_hash, verify_password

router = APIRouter()
Database = Annotated[Session, Depends(get_db)]


@router.post("/login", response_model=Token)
def login(data: UserLogin, db: Database) -> Token:
    user = db.scalar(select(User).where(User.username == data.username))
    if user is None or not verify_password(data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="用户名或密码错误")
    return Token(access_token=create_access_token(user.id))


@router.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def register(data: UserCreate, db: Database) -> User:
    if db.scalar(select(User).where(User.username == data.username)):
        raise HTTPException(status_code=409, detail="用户名已存在")
    user = User(username=data.username, password_hash=get_password_hash(data.password), role="user")
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.get("/me", response_model=UserOut)
def me(current_user: CurrentUser) -> User:
    return current_user


@router.post("/change-password")
def change_password(data: PasswordChange, db: Database, current_user: CurrentUser) -> dict[str, str]:
    if not verify_password(data.current_password, current_user.password_hash):
        raise HTTPException(status_code=400, detail="当前密码错误")
    current_user.password_hash = get_password_hash(data.new_password)
    db.commit()
    return {"message": "密码修改成功"}
