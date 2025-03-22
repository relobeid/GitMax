from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status, Request, Cookie
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.utils.config import get_settings
from app.database import get_db, User
from app.models.user import TokenData
import logging

logger = logging.getLogger(__name__)
settings = get_settings()
security = HTTPBearer(auto_error=False)  # Make Bearer token optional

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Create a JWT access token.
    
    Args:
        data: The data to encode in the token.
        expires_delta: The expiration time of the token.
        
    Returns:
        str: The encoded JWT token.
    """
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode,
        settings.secret_key,
        algorithm=settings.algorithm
    )
    
    return encoded_jwt

async def get_current_user(
    request: Request,
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    """
    Get the current authenticated user from either Authorization header or cookie.
    
    Args:
        request: The request object to extract cookies.
        credentials: The HTTPAuthorizationCredentials object containing the token (optional).
        db: The database session.
        
    Returns:
        User: The authenticated user.
        
    Raises:
        HTTPException: If the token is invalid or the user is not found.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    token = None
    
    # Try to get token from Authorization header
    if credentials and credentials.credentials:
        token = credentials.credentials
    
    # If no token in header, try to get from cookie
    if not token:
        token_cookie = request.cookies.get("token")
        if token_cookie and token_cookie.startswith("Bearer "):
            token = token_cookie.replace("Bearer ", "")
    
    if not token:
        logger.error("No token found in request")
        raise credentials_exception
    
    try:
        payload = jwt.decode(
            token,
            settings.secret_key,
            algorithms=[settings.algorithm]
        )
        github_id: str = payload.get("sub")
        
        if github_id is None:
            logger.error("No github_id found in token payload")
            raise credentials_exception
        
        token_data = TokenData(github_id=github_id)
    except JWTError as e:
        logger.error(f"JWT error: {str(e)}")
        raise credentials_exception
    
    # Get the user from the database
    user = db.query(User).filter(User.github_id == token_data.github_id).first()
    
    if user is None:
        logger.error(f"User with github_id {token_data.github_id} not found")
        raise credentials_exception
    
    if not user.is_active:
        logger.error(f"User with github_id {token_data.github_id} is inactive")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user"
        )
    
    return user
