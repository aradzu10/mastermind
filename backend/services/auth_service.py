"""
Authentication service for user management and token generation.
"""
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from backend.db.repositories.user_repository import UserRepository
from backend.db.models.user import User
from backend.core.jwt_handler import create_access_token, verify_token


class AuthService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.repo = UserRepository(session)

    async def create_guest_user(self, display_name: str) -> tuple[User, str]:
        """
        Create a new guest user and generate access token.

        Args:
            display_name: Display name for the guest user

        Returns:
            Tuple of (User object, JWT token)
        """
        user = await self.repo.create(
            display_name=display_name,
            is_guest=True,
            elo_rating=1200
        )
        await self.session.flush()
        await self.session.refresh(user)

        token = create_access_token(user.id)
        return user, token

    async def authenticate_google(self, google_id: str, email: str, display_name: str) -> tuple[User, str]:
        """
        Authenticate user via Google OAuth. Creates user if doesn't exist.

        Args:
            google_id: Google user ID
            email: User email from Google
            display_name: Display name from Google

        Returns:
            Tuple of (User object, JWT token)
        """
        # Try to find existing user by Google ID
        user = await self.repo.get_by_google_id(google_id)

        if not user:
            # Create new OAuth user
            user = await self.repo.create(
                email=email,
                google_id=google_id,
                display_name=display_name,
                is_guest=False,
                elo_rating=1200
            )
            await self.session.flush()
            await self.session.refresh(user)

        token = create_access_token(user.id)
        return user, token

    async def get_current_user(self, token: str) -> Optional[User]:
        """
        Get user from JWT token.

        Args:
            token: JWT token string

        Returns:
            User object if token is valid, None otherwise
        """
        user_id = verify_token(token)
        if user_id is None:
            return None

        user = await self.repo.get(user_id)
        return user
