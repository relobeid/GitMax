from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class Token(BaseModel):
    access_token: str
    token_type: str


class UserResponse(BaseModel):
    id: int
    github_id: str
    github_username: str
    created_at: datetime
    updated_at: datetime
    is_active: bool

    class Config:
        from_attributes = True


class UserBase(BaseModel):
    """Base user model with common attributes."""
    username: str
    email: Optional[str] = None
    avatar_url: Optional[str] = None
    github_url: Optional[str] = None


class UserCreate(UserBase):
    """Model for creating a new user."""
    github_id: str
    public_repos: int = 0
    followers: int = 0
    following: int = 0


class UserUpdate(BaseModel):
    """Model for updating user data."""
    username: Optional[str] = None
    email: Optional[str] = None
    avatar_url: Optional[str] = None
    public_repos: Optional[int] = None
    followers: Optional[int] = None
    following: Optional[int] = None
    github_url: Optional[str] = None
    is_active: Optional[bool] = None


class UserInDB(UserBase):
    """Model for user data stored in the database."""
    id: int
    github_id: str
    public_repos: int
    followers: int
    following: int
    created_at: datetime
    updated_at: datetime
    is_active: bool

    class Config:
        orm_mode = True


class TokenData(BaseModel):
    """Model for data stored in JWT token."""
    username: Optional[str] = None
    github_id: Optional[str] = None
