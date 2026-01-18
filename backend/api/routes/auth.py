from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from backend.api.dependencies import get_current_user
from backend.db.database import get_db
from backend.db.models.user import User
from backend.schemas.auth import GuestUserCreate, TokenResponse, UserResponse
from backend.services.auth_service import AuthService

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/guest", response_model=TokenResponse, status_code=201)
async def create_guest(
    guest_data: GuestUserCreate,
    db: AsyncSession = Depends(get_db)
):
    """Create a guest user and return JWT token"""
    auth_service = AuthService(db)

    try:
        user, token = await auth_service.create_guest_user(guest_data.display_name)

        return TokenResponse(
            access_token=token,
            token_type="bearer",
            user=UserResponse(
                id=user.id,
                email=user.email,
                display_name=user.display_name,
                is_guest=user.is_guest,
                elo_rating=user.elo_rating,
                created_at=user.created_at
            )
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create guest user: {str(e)}"
        )


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    current_user: User = Depends(get_current_user)
):
    """Get current authenticated user information"""
    return UserResponse(
        id=current_user.id,
        email=current_user.email,
        display_name=current_user.display_name,
        is_guest=current_user.is_guest,
        elo_rating=current_user.elo_rating,
        created_at=current_user.created_at
    )
