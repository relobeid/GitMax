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
        f"&allow_signup=true"
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
    try:
        # Exchange code for access token
        access_token = await GitHubService.get_access_token(code)
        if not access_token:
            raise HTTPException(status_code=400, detail="Failed to get GitHub access token")
        
        # Get user data from GitHub
        user_data = await GitHubService.get_user_data(access_token)
        if not user_data:
            raise HTTPException(status_code=400, detail="Failed to get GitHub user data")
        
        # Check if user already exists
        user = db.query(User).filter(User.github_id == str(user_data['id'])).first()
        is_new_user = False
        
        if not user:
            # Create new user
            user = User(
                github_id=str(user_data['id']),
                github_username=user_data['login'],
                github_token=access_token
            )
            db.add(user)
            is_new_user = True
        else:
            # Update existing user
            user.github_token = access_token
            user.github_username = user_data['login']
        
        db.commit()
        
        # Create access token
        jwt_token = create_access_token(
            data={"sub": str(user_data['id'])},
            expires_delta=timedelta(minutes=settings.access_token_expire_minutes)
        )
        
        # Return token if API request, redirect if browser request
        if request and request.headers.get('accept') == 'application/json':
            return {
                "access_token": jwt_token,
                "token_type": "bearer",
                "user": {
                    "id": user.id,
                    "github_id": user.github_id,
                    "github_username": user.github_username,
                    "is_new_user": is_new_user
                }
            }
        else:
            # Redirect directly to dashboard with the token in both URL and cookie
            redirect_url = f"{settings.frontend_url}/dashboard?token={jwt_token}"
            if is_new_user:
                redirect_url += "&is_new_user=true"
                
            response = RedirectResponse(url=redirect_url)
            response.set_cookie(
                key="token",
                value=f"Bearer {jwt_token}",
                httponly=True,
                max_age=30 * 24 * 60 * 60,  # 30 days
                samesite="lax",
                secure=False  # Set to True in production with HTTPS
            )
            return response
            
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    """
    Get current user info.
    
    Args:
        current_user: The current authenticated user.
        
    Returns:
        UserResponse: Current user data.
    """
    return current_user


@router.post("/logout")
async def logout(response: Response):
    """
    Logout current user.
    
    Args:
        response: The response object.
        
    Returns:
        dict: Success message.
    """
    response.delete_cookie(key="token")
    return {"message": "Successfully logged out"}
