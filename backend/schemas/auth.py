"""
Authentication Pydantic schemas for request/response validation.
"""
from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class GuestUserCreate(BaseModel):
    """Request body for creating a guest user."""
    display_name: str


class GoogleAuthRequest(BaseModel):
    """Request body for Google OAuth authentication."""
    google_id: str
    email: str
    display_name: str


class UserResponse(BaseModel):
    """User data response."""
    id: int
    email: Optional[str]
    display_name: str
    is_guest: bool
    elo_rating: int
    created_at: datetime

    class Config:
        from_attributes = True


class TokenResponse(BaseModel):
    """Authentication token response."""
    access_token: str
    token_type: str = "bearer"
    user: UserResponse
