"""
Authentication dependencies for FastAPI routes.
"""
from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from backend.db.database import get_db
from backend.services.auth_service import AuthService
from backend.db.models.user import User


security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db)
) -> User:
    """
    Dependency to get current authenticated user from JWT token.
    Raises 401 if token is invalid.
    """
    token = credentials.credentials
    auth_service = AuthService(db)
    user = await auth_service.get_current_user(token)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user


async def get_current_user_optional(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(HTTPBearer(auto_error=False)),
    db: AsyncSession = Depends(get_db)
) -> Optional[User]:
    """
    Optional dependency to get current user if authenticated.
    Returns None if no token provided (allows guest access).
    """
    if credentials is None:
        return None

    token = credentials.credentials
    auth_service = AuthService(db)
    user = await auth_service.get_current_user(token)
    return user
