"""
Authentication service for user management and token generation.
"""
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from backend.core.jwt_handler import create_access_token, verify_token
from backend.db.models.user import User
from backend.db.repositories.user_repository import UserRepository


class AuthService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.repo = UserRepository(session)

    async def create_guest_user(self, display_name: str) -> tuple[User, str]:
        user = await self.repo.create(
            display_name=display_name,
            is_guest=True,
            elo_rating=1200
        )
        await self.session.flush()
        await self.session.refresh(user)

        token = create_access_token(user.id)
        return user, token

    async def get_current_user(self, token: str) -> Optional[User]:
        user_id = verify_token(token)
        if user_id is None:
            return None

        user = await self.repo.get(user_id)
        return user
