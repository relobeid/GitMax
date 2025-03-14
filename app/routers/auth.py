from fastapi import APIRouter, Depends, HTTPException, status, Request, Response
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from datetime import timedelta
from app.utils.config import get_settings
from app.database import get_db, User
from app.services.github import GitHubService
from app.auth import create_access_token
from app.models.user import Token

settings = get_settings()

router = APIRouter(
    prefix=f"{settings.api_prefix}/auth",
    tags=["auth"],
)


@router.get("/login")
async def login():
    """
    Redirect to GitHub OAuth login page.
    
    Returns:
        RedirectResponse: Redirect to GitHub OAuth login page.
    """
    github_auth_url = (
        f"https://github.com/login/oauth/authorize"
        f"?client_id={settings.github_client_id}"
        f"&redirect_uri={settings.github_redirect_uri}"
        f"&scope=user:email"
    )
    return RedirectResponse(url=github_auth_url)


@router.get("/callback")
async def callback(code: str, request: Request, db: Session = Depends(get_db)):
    """
    GitHub OAuth callback endpoint.
    
    Args:
        code: The authorization code from GitHub.
        request: The request object.
        db: The database session.
        
    Returns:
        RedirectResponse: Redirect to frontend with token.
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
        db.commit()
        db.refresh(user)
    
    # Create JWT token
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    jwt_token = create_access_token(
        data={"sub": user.github_id},
        expires_delta=access_token_expires,
    )
    
    # Set token in cookie
    response = RedirectResponse(url="http://localhost:3000")  # Redirect to frontend
    response.set_cookie(
        key="access_token",
        value=f"Bearer {jwt_token}",
        httponly=True,
        max_age=settings.access_token_expire_minutes * 60,
        expires=settings.access_token_expire_minutes * 60,
    )
    
    return response


@router.get("/logout")
async def logout(response: Response):
    """
    Logout endpoint.
    
    Args:
        response: The response object.
        
    Returns:
        dict: Success message.
    """
    response.delete_cookie(key="access_token")
    return {"message": "Successfully logged out"}
