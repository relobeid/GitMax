import httpx
from typing import Dict, Any, Optional
from app.utils.config import get_settings
from pydantic import BaseModel

settings = get_settings()

class UserCreate(BaseModel):
    github_id: str
    username: str
    email: Optional[str]
    avatar_url: Optional[str]
    public_repos: int
    followers: int
    following: int
    github_url: str

class GitHubService:
    """Service for interacting with the GitHub API."""
    
    @staticmethod
    async def get_access_token(code: str) -> Optional[str]:
        """
        Exchange authorization code for access token.
        
        Args:
            code: The authorization code from GitHub.
            
        Returns:
            Optional[str]: The access token if successful, None otherwise.
        """
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    "https://github.com/login/oauth/access_token",
                    data={
                        "client_id": settings.github_client_id,
                        "client_secret": settings.github_client_secret,
                        "code": code,
                        "redirect_uri": settings.github_redirect_uri,
                    },
                    headers={"Accept": "application/json"}
                )
                response.raise_for_status()
                return response.json().get("access_token")
            except httpx.HTTPError:
                return None
    
    @staticmethod
    async def get_user_data(access_token: str) -> Optional[Dict[str, Any]]:
        """
        Get user data from GitHub API.
        
        Args:
            access_token: The GitHub access token.
            
        Returns:
            Optional[Dict[str, Any]]: The user data if successful, None otherwise.
        """
        async with httpx.AsyncClient() as client:
            try:
                headers = {
                    "Authorization": f"Bearer {access_token}",
                    "Accept": "application/json",
                }
                response = await client.get(
                    "https://api.github.com/user",
                    headers=headers
                )
                response.raise_for_status()
                return response.json()
            except httpx.HTTPError:
                return None
    
    @staticmethod
    def map_github_user_to_user_create(github_user: Dict[str, Any]) -> UserCreate:
        """
        Map GitHub user data to UserCreate model.
        
        Args:
            github_user: The GitHub user data.
            
        Returns:
            UserCreate: The UserCreate model.
        """
        return UserCreate(
            github_id=str(github_user["id"]),
            username=github_user["login"],
            email=github_user.get("email"),
            avatar_url=github_user.get("avatar_url"),
            public_repos=github_user.get("public_repos", 0),
            followers=github_user.get("followers", 0),
            following=github_user.get("following", 0),
            github_url=github_user.get("html_url", "")
        )
