from typing import Annotated

from fastapi import APIRouter, Depends, status

from app.core.dependencies import (
    get_auth_service,
    get_current_user,
)
from app.core.exceptions import (
    AuthenticationError,
    ResourceAlreadyExistsError,
)
from app.models.user import User
from app.schemas.auth import (
    LoginRequest,
    RegisterRequest,
    TokenResponse,
)
from app.schemas.users import UserResponse
from app.services.auth_service import AuthService

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def register(
    request: RegisterRequest,
    service: Annotated[
        AuthService,
        Depends(get_auth_service),
    ],
):
    user = service.register(request)
    return UserResponse.model_validate(user)


@router.post(
    "/login",
    response_model=TokenResponse,
)
def login(
    request: LoginRequest,
    service: Annotated[
        AuthService,
        Depends(get_auth_service),
    ],
):
    return service.login(request)


@router.get(
    "/me",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
)
def get_me(
    current_user: Annotated[
        User,
        Depends(get_current_user),
    ],
):
    """
    Returns the currently authenticated user.
    """
    return UserResponse.model_validate(current_user)
