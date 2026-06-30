from typing import Annotated
from uuid import UUID

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.services.resume_service import ResumeService
from app.core.database import get_db
from app.core.security import (
    decode_access_token,
    security,
)
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.services.auth_service import AuthService


def get_auth_service(
    db: Annotated[Session, Depends(get_db)],
) -> AuthService:
    return AuthService(db)


def get_current_user(
    credentials: Annotated[
        HTTPAuthorizationCredentials,
        Depends(security),
    ],
    db: Annotated[Session, Depends(get_db)],
) -> User:
  
    payload = decode_access_token(
        credentials.credentials,
    )

    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token.",
        )

    user_id = payload.get("sub")

    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload.",
        )

    repository = UserRepository(db)

    user = repository.get_by_id(UUID(user_id))

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found.",
        )
    
    return user

def get_resume_service(
    db: Annotated[
        Session,
        Depends(get_db),
    ],
) -> ResumeService:
    return ResumeService(db)