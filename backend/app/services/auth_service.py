from uuid import UUID

from sqlalchemy.orm import Session

from app.core.security import (
    create_access_token,
    hash_password,
    verify_password,
)
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.auth import (
    LoginRequest,
    RegisterRequest,
    TokenResponse,
)


class AuthService:
    def __init__(self, db: Session):
        self.user_repository = UserRepository(db)

    def register(
        self,
        request: RegisterRequest,
    ) -> User:

        existing_user = self.user_repository.get_by_email(
            request.email
        )

        if existing_user:
            raise ValueError(
                "Email is already registered."
            )

        user = User(
            full_name=request.full_name,
            email=request.email,
            password_hash=hash_password(
                request.password
            ),
        )

        return self.user_repository.create(user)

    def login(
        self,
        request: LoginRequest,
    ) -> TokenResponse:

        user = self.user_repository.get_by_email(
            request.email
        )

        if not user:
            raise ValueError(
                "Invalid email or password."
            )

        if not verify_password(
            request.password,
            user.password_hash,
        ):
            raise ValueError(
                "Invalid email or password."
            )

        token = create_access_token(
            user_id=str(user.id),
        )

        return TokenResponse(
            access_token=token,
        )