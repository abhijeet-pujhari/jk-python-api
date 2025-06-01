from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.security import verify_password, create_access_token, decode_access_token
from app.db.session import get_db
from app.db import models
from app.core.config import settings
from app.services.users import get_user_by_username

from typing import Optional

# Authentication logic

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

async def authenticate_user(db: AsyncSession, username: str, password: str) -> Optional[models.User]:
    # Placeholder: implement user lookup and password check
    # For demo, always return None (no user table yet)
    return None

async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    payload = decode_access_token(token)
    if payload is None or 'sub' not in payload:
        raise credentials_exception
    username = payload['sub']
    user = await get_user_by_username(db, username)
    if user is None:
        raise credentials_exception
    return user
