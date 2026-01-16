"""
JWT token utilities for authentication.

Handles creation and verification of JWT tokens using HS256 algorithm.
"""
from datetime import datetime, timedelta
from typing import Optional
import os
from jose import JWTError, jwt


SECRET_KEY = os.getenv("SECRET_KEY", "dev_secret_key_change_in_production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_DAYS = 7


def create_access_token(user_id: int, expires_delta: Optional[timedelta] = None) -> str:
    """
    Create a JWT access token for a user.

    Args:
        user_id: User ID to encode in token
        expires_delta: Optional custom expiration time

    Returns:
        Encoded JWT token string
    """
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS)

    to_encode = {
        "sub": str(user_id),
        "exp": expire
    }

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str) -> Optional[int]:
    """
    Verify and decode a JWT token.

    Args:
        token: JWT token string to verify

    Returns:
        User ID if token is valid, None otherwise
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            return None
        return int(user_id)
    except JWTError:
        return None
