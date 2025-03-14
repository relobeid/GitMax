from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.utils.config import get_settings
from app.database import get_db, User
from app.auth import get_current_user
from app.models.user import UserResponse, UserUpdate

settings = get_settings()

router = APIRouter(
    prefix=f"{settings.api_prefix}/profile",
    tags=["profile"],
)


@router.get("", response_model=UserResponse)
async def get_profile(current_user: User = Depends(get_current_user)):
    """
    Get the authenticated user's profile.
    
    Args:
        current_user: The authenticated user.
        
    Returns:
        UserResponse: The user's profile.
    """
    return current_user


@router.put("", response_model=UserResponse)
async def update_profile(
    user_update: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Update the authenticated user's profile.
    
    Args:
        user_update: The user data to update.
        current_user: The authenticated user.
        db: The database session.
        
    Returns:
        UserResponse: The updated user's profile.
    """
    # Update user data
    for key, value in user_update.dict(exclude_unset=True).items():
        setattr(current_user, key, value)
    
    db.commit()
    db.refresh(current_user)
    
    return current_user
