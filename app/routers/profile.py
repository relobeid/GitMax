from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.utils.config import get_settings
from app.database import get_db, User
from app.auth import get_current_user
from app.models.user import UserResponse, UserUpdate
from app.services.github import GitHubService
from typing import List, Dict, Any
import httpx

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


@router.get("/github")
async def get_github_profile(current_user: User = Depends(get_current_user)):
    """
    Get the authenticated user's detailed GitHub profile.
    
    Args:
        current_user: The authenticated user.
        
    Returns:
        Dict[str, Any]: The user's detailed GitHub profile.
    """
    try:
        # Fetch the user's detailed GitHub profile using their GitHub token
        profile = await GitHubService.get_user_profile(
            current_user.github_username, 
            access_token=current_user.github_token
        )
        
        if not profile:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="GitHub profile not found"
            )
        
        return profile
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch GitHub profile: {str(e)}"
        )


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


@router.get("/repositories", response_model=List[Dict[str, Any]])
async def get_repositories(current_user: User = Depends(get_current_user)):
    """
    Get the authenticated user's GitHub repositories.
    
    Args:
        current_user: The authenticated user.
        
    Returns:
        List[Dict[str, Any]]: The user's GitHub repositories.
    """
    # Fetch the user's repositories from GitHub using their GitHub token
    repositories = await GitHubService.get_user_repositories(
        current_user.github_username,
        access_token=current_user.github_token
    )
    return repositories


@router.get("/activity")
async def get_activity(current_user: User = Depends(get_current_user)):
    """
    Get the authenticated user's recent GitHub activity.
    
    Args:
        current_user: The authenticated user.
        
    Returns:
        List[Dict[str, Any]]: The user's recent GitHub activity.
    """
    try:
        # Fetch the user's detailed GitHub profile using their GitHub token
        profile = await GitHubService.get_user_profile(
            current_user.github_username,
            access_token=current_user.github_token
        )
        
        if not profile:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="GitHub profile not found"
            )
        
        return profile.get("recent_activity", [])
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch GitHub activity: {str(e)}"
        )
