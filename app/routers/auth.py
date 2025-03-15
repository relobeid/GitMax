from fastapi import APIRouter, Depends, HTTPException, status, Request, Response
from fastapi.responses import RedirectResponse, JSONResponse
from sqlalchemy.orm import Session
from datetime import timedelta
from app.utils.config import get_settings
from app.database import get_db, User
from app.services.github import GitHubService
from app.auth import create_access_token, get_current_user
from app.models.user import Token, UserResponse
from typing import Dict, Any

settings = get_settings()

router = APIRouter(
    prefix=f"{settings.api_prefix}/auth",
    tags=["auth"],
)


@router.get("/login")
async def login():
    """
    Get GitHub OAuth login URL.
    
    Returns:
        dict: GitHub OAuth login URL.
    """
    github_auth_url = (
        f"https://github.com/login/oauth/authorize"
        f"?client_id={settings.github_client_id}"
        f"&redirect_uri={settings.github_redirect_uri}"
        f"&scope=user:email"
    )
    return {"url": github_auth_url}


@router.post("/callback")
@router.get("/callback")
async def callback(code: str, request: Request = None, db: Session = Depends(get_db)):
    """
    GitHub OAuth callback endpoint.
    
    Args:
        code: The authorization code from GitHub.
        request: The request object.
        db: The database session.
        
    Returns:
        dict or RedirectResponse: User data and access token or redirect to frontend.
    """
    # Exchange code for access token
    access_token = await GitHubService.get_access_token(code)
    
    if not access_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Failed to get access token from GitHub",
        )
    
    # Get user data from GitHub
    github_user = await GitHubService.get_user_data(access_token)
    
    if not github_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Failed to get user data from GitHub",
        )
    
    # Check if user exists in database
    github_id = str(github_user.get("id"))
    user = db.query(User).filter(User.github_id == github_id).first()
    
    if not user:
        # Create new user
        user_create = GitHubService.map_github_user_to_user_create(github_user)
        user = User(
            github_id=user_create.github_id,
            username=user_create.username,
            email=user_create.email,
            avatar_url=user_create.avatar_url,
            public_repos=user_create.public_repos,
            followers=user_create.followers,
            following=user_create.following,
            github_url=user_create.github_url,
            github_token=access_token,
        )
        db.add(user)
        db.commit()
        db.refresh(user)
    else:
        # Update existing user
        user.username = github_user.get("login")
        user.email = github_user.get("email")
        user.avatar_url = github_user.get("avatar_url")
        user.public_repos = github_user.get("public_repos", 0)
        user.followers = github_user.get("followers", 0)
        user.following = github_user.get("following", 0)
        user.github_url = github_user.get("html_url")
        user.github_token = access_token
        db.commit()
        db.refresh(user)
    
    # Create JWT token
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    jwt_token = create_access_token(
        data={"sub": user.github_id},
        expires_delta=access_token_expires,
    )
    
    # Check if this is a browser redirect (GET request) or API call (POST request)
    if request and request.method == "GET":
        # For browser redirects, redirect to frontend with token in URL
        frontend_url = f"{settings.frontend_url}?token={jwt_token}"
        return RedirectResponse(url=frontend_url)
    else:
        # For API calls, return JSON response
        return {
            "access_token": jwt_token,
            "token_type": "bearer",
            "user": {
                "id": user.id,
                "github_id": user.github_id,
                "username": user.username,
                "email": user.email,
                "avatar_url": user.avatar_url,
                "public_repos": user.public_repos,
                "followers": user.followers,
                "following": user.following,
                "github_url": user.github_url,
            }
        }


@router.post("/logout")
async def logout():
    """
    Logout endpoint.
    
    Returns:
        dict: Success message.
    """
    # Since we're using JWT tokens, we don't need to do anything server-side
    # The client will remove the token from storage
    return {"message": "Successfully logged out", "success": True}


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    """
    Get current user info.
    
    Args:
        current_user: The current authenticated user.
        
    Returns:
        UserResponse: The current user info.
    """
    return UserResponse(
        id=current_user.id,
        github_id=current_user.github_id,
        username=current_user.username,
        email=current_user.email,
        avatar_url=current_user.avatar_url,
        public_repos=current_user.public_repos,
        followers=current_user.followers,
        following=current_user.following,
        github_url=current_user.github_url,
        created_at=current_user.created_at,
        updated_at=current_user.updated_at,
        is_active=current_user.is_active
    )


@router.post("/refresh")
async def refresh_token(current_user: User = Depends(get_current_user)):
    """
    Refresh access token.
    
    Args:
        current_user: The current authenticated user.
        
    Returns:
        Token: The new access token.
    """
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": current_user.github_id},
        expires_delta=access_token_expires,
    )
    return {"access_token": access_token, "token_type": "bearer"}
