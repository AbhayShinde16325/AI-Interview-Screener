from datetime import datetime, timedelta, timezone
from typing import Any

from jose import JWTError, jwt
from pwdlib import PasswordHash

from app.core.config import settings
from fastapi.security import HTTPBearer

security = HTTPBearer()
# Password Hashing Configuration
password_hasher = PasswordHash.recommended()


def hash_password(password: str) -> str:
    """
    Hash a plain text password.
    """
    return password_hasher.hash(password)


def verify_password(
    plain_password: str,
    hashed_password: str,
) -> bool:
    """
    Verify a plain text password against its hash.
    """
    return password_hasher.verify(
        plain_password,
        hashed_password,
    )


def create_access_token(
    user_id: str,
    expires_delta: timedelta | None = None,
) -> str:
    """
    Create a JWT access token.
    """

    expire = datetime.now(timezone.utc) + (
        expires_delta
        or timedelta(
            minutes=settings.access_token_expire_minutes
        )
    )

    payload: dict[str, Any] = {
        "sub": user_id,
        "exp": expire,
    }

    encoded_jwt = jwt.encode(
        payload,
        settings.secret_key,
        algorithm=settings.algorithm,
    )

    return encoded_jwt


def decode_access_token(
    token: str,
) -> dict[str, Any] | None:
    """
    Decode a JWT access token.

    Returns:
        Payload dictionary if valid, otherwise None.
    """

    # Accept both:
    # "Bearer eyJ..."
    # "eyJ..."
    if token.startswith("Bearer "):
        token = token.removeprefix("Bearer ").strip()

    try:
        payload = jwt.decode(
            token,
            settings.secret_key,
            algorithms=[settings.algorithm],
        )

        return payload

    except JWTError:
        return None