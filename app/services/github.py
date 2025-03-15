import httpx
from typing import Dict, Any, Optional, List
from app.utils.config import get_settings
from pydantic import BaseModel
import logging
import base64

settings = get_settings()
logger = logging.getLogger(__name__)

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
        logger.info(f"Exchanging code for access token. Code: {code[:5]}...")
        logger.info(f"Using client_id: {settings.github_client_id[:5]}... and redirect_uri: {settings.github_redirect_uri}")
        
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
                result = response.json()
                logger.info(f"GitHub token exchange response: {result.keys()}")
                
                if "error" in result:
                    logger.error(f"GitHub OAuth error: {result.get('error')}, {result.get('error_description')}")
                    return None
                    
                return result.get("access_token")
            except httpx.HTTPError as e:
                logger.error(f"HTTP error during token exchange: {str(e)}")
                try:
                    logger.error(f"Response content: {response.text}")
                except:
                    pass
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
        logger.info("Getting user data from GitHub API")
        
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
                user_data = response.json()
                logger.info(f"Successfully retrieved GitHub user data for: {user_data.get('login')}")
                return user_data
            except httpx.HTTPError as e:
                logger.error(f"HTTP error during user data retrieval: {str(e)}")
                try:
                    logger.error(f"Response content: {response.text}")
                except:
                    pass
                return None
    
    @staticmethod
    async def get_user_profile(username: str, access_token: str = None) -> Optional[Dict[str, Any]]:
        """
        Get detailed user profile data from GitHub API.
        
        Args:
            username: The GitHub username.
            access_token: Optional GitHub access token for authentication.
            
        Returns:
            Optional[Dict[str, Any]]: The user profile data if successful, None otherwise.
        """
        logger.info(f"Getting detailed profile for user: {username}")
        
        headers = {"Accept": "application/json"}
        if access_token:
            headers["Authorization"] = f"Bearer {access_token}"
        
        async with httpx.AsyncClient() as client:
            try:
                # Get user data
                user_response = await client.get(
                    f"https://api.github.com/users/{username}",
                    headers=headers
                )
                user_response.raise_for_status()
                user_data = user_response.json()
                
                # Get user repositories
                repos_response = await client.get(
                    f"https://api.github.com/users/{username}/repos",
                    headers=headers,
                    params={"sort": "updated", "per_page": 10}
                )
                repos_response.raise_for_status()
                repos_data = repos_response.json()
                
                # Get user events (activity)
                events_response = await client.get(
                    f"https://api.github.com/users/{username}/events/public",
                    headers=headers,
                    params={"per_page": 10}
                )
                events_response.raise_for_status()
                events_data = events_response.json()
                
                # Calculate language statistics
                languages = {}
                for repo in repos_data:
                    lang = repo.get("language")
                    if lang:
                        languages[lang] = languages.get(lang, 0) + 1
                
                # Sort languages by frequency
                sorted_languages = sorted(languages.items(), key=lambda x: x[1], reverse=True)
                
                # Format recent activity
                recent_activity = []
                for event in events_data[:5]:
                    event_type = event.get("type", "")
                    repo_name = event.get("repo", {}).get("name", "")
                    created_at = event.get("created_at", "")
                    
                    if event_type == "PushEvent":
                        commits = event.get("payload", {}).get("commits", [])
                        for commit in commits:
                            recent_activity.append({
                                "type": "commit",
                                "repo": repo_name,
                                "message": commit.get("message", ""),
                                "date": created_at
                            })
                    elif event_type == "CreateEvent":
                        ref_type = event.get("payload", {}).get("ref_type", "")
                        recent_activity.append({
                            "type": f"created_{ref_type}",
                            "repo": repo_name,
                            "date": created_at
                        })
                    elif event_type == "IssuesEvent":
                        action = event.get("payload", {}).get("action", "")
                        issue_title = event.get("payload", {}).get("issue", {}).get("title", "")
                        recent_activity.append({
                            "type": f"issue_{action}",
                            "repo": repo_name,
                            "title": issue_title,
                            "date": created_at
                        })
                    elif event_type == "PullRequestEvent":
                        action = event.get("payload", {}).get("action", "")
                        pr_title = event.get("payload", {}).get("pull_request", {}).get("title", "")
                        recent_activity.append({
                            "type": f"pull_request_{action}",
                            "repo": repo_name,
                            "title": pr_title,
                            "date": created_at
                        })
                
                # Combine all data
                profile_data = {
                    "username": user_data.get("login"),
                    "name": user_data.get("name"),
                    "avatar_url": user_data.get("avatar_url"),
                    "html_url": user_data.get("html_url"),
                    "bio": user_data.get("bio"),
                    "company": user_data.get("company"),
                    "location": user_data.get("location"),
                    "email": user_data.get("email"),
                    "blog": user_data.get("blog"),
                    "twitter_username": user_data.get("twitter_username"),
                    "public_repos": user_data.get("public_repos"),
                    "public_gists": user_data.get("public_gists"),
                    "followers": user_data.get("followers"),
                    "following": user_data.get("following"),
                    "created_at": user_data.get("created_at"),
                    "updated_at": user_data.get("updated_at"),
                    "languages": sorted_languages,
                    "recent_activity": recent_activity,
                    "repositories": [
                        {
                            "id": repo.get("id"),
                            "name": repo.get("name"),
                            "full_name": repo.get("full_name"),
                            "description": repo.get("description"),
                            "language": repo.get("language"),
                            "stars": repo.get("stargazers_count", 0),
                            "forks": repo.get("forks_count", 0),
                            "issues": repo.get("open_issues_count", 0),
                            "updated_at": repo.get("updated_at"),
                            "html_url": repo.get("html_url"),
                        }
                        for repo in repos_data
                    ]
                }
                
                logger.info(f"Successfully retrieved detailed profile for user: {username}")
                return profile_data
            except httpx.HTTPError as e:
                logger.error(f"HTTP error during user profile retrieval: {str(e)}")
                try:
                    logger.error(f"Response content: {e.response.text if hasattr(e, 'response') else 'No response'}")
                except:
                    pass
                return None
    
    @staticmethod
    async def get_user_repositories(username: str, access_token: str = None) -> List[Dict[str, Any]]:
        """
        Get user repositories from GitHub API.
        
        Args:
            username: The GitHub username.
            access_token: Optional GitHub access token for authentication.
            
        Returns:
            List[Dict[str, Any]]: The user repositories if successful, empty list otherwise.
        """
        logger.info(f"Getting repositories for user: {username}")
        
        headers = {"Accept": "application/json"}
        if access_token:
            headers["Authorization"] = f"Bearer {access_token}"
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    f"https://api.github.com/users/{username}/repos",
                    headers=headers,
                    params={"sort": "updated", "per_page": 10}
                )
                response.raise_for_status()
                repos = response.json()
                logger.info(f"Successfully retrieved {len(repos)} repositories for user: {username}")
                
                # Transform the data to match our expected format
                transformed_repos = []
                for repo in repos:
                    transformed_repos.append({
                        "id": repo.get("id"),
                        "name": repo.get("name"),
                        "description": repo.get("description"),
                        "language": repo.get("language"),
                        "stars": repo.get("stargazers_count", 0),
                        "forks": repo.get("forks_count", 0),
                        "issues": repo.get("open_issues_count", 0),
                        "updated_at": repo.get("updated_at"),
                        "html_url": repo.get("html_url"),
                    })
                
                return transformed_repos
            except httpx.HTTPError as e:
                logger.error(f"HTTP error during repository retrieval: {str(e)}")
                try:
                    logger.error(f"Response content: {response.text}")
                except:
                    pass
                return []
    
    @staticmethod
    async def get_repository_details(username: str, repo_name: str, access_token: str = None) -> Optional[Dict[str, Any]]:
        """
        Get detailed information about a specific repository.
        
        Args:
            username: The GitHub username.
            repo_name: The repository name.
            access_token: Optional GitHub access token for authentication.
            
        Returns:
            Optional[Dict[str, Any]]: The repository details if successful, None otherwise.
        """
        logger.info(f"Getting details for repository: {username}/{repo_name}")
        
        headers = {"Accept": "application/json"}
        if access_token:
            headers["Authorization"] = f"Bearer {access_token}"
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    f"https://api.github.com/repos/{username}/{repo_name}",
                    headers=headers
                )
                response.raise_for_status()
                repo_data = response.json()
                
                # Get languages used in the repository
                languages_response = await client.get(
                    f"https://api.github.com/repos/{username}/{repo_name}/languages",
                    headers=headers
                )
                languages_response.raise_for_status()
                languages = languages_response.json()
                
                # Get contributors
                contributors_response = await client.get(
                    f"https://api.github.com/repos/{username}/{repo_name}/contributors",
                    headers=headers,
                    params={"per_page": 5}
                )
                contributors_response.raise_for_status()
                contributors = contributors_response.json()
                
                # Get commits
                commits_response = await client.get(
                    f"https://api.github.com/repos/{username}/{repo_name}/commits",
                    headers=headers,
                    params={"per_page": 10}
                )
                commits_response.raise_for_status()
                commits = commits_response.json()
                
                # Combine all data
                repo_details = {
                    "id": repo_data.get("id"),
                    "name": repo_data.get("name"),
                    "full_name": repo_data.get("full_name"),
                    "description": repo_data.get("description"),
                    "language": repo_data.get("language"),
                    "languages": languages,
                    "stars": repo_data.get("stargazers_count", 0),
                    "forks": repo_data.get("forks_count", 0),
                    "issues": repo_data.get("open_issues_count", 0),
                    "watchers": repo_data.get("watchers_count", 0),
                    "created_at": repo_data.get("created_at"),
                    "updated_at": repo_data.get("updated_at"),
                    "pushed_at": repo_data.get("pushed_at"),
                    "html_url": repo_data.get("html_url"),
                    "contributors": [
                        {
                            "username": contributor.get("login"),
                            "avatar_url": contributor.get("avatar_url"),
                            "contributions": contributor.get("contributions"),
                            "html_url": contributor.get("html_url")
                        }
                        for contributor in contributors
                    ],
                    "recent_commits": [
                        {
                            "sha": commit.get("sha"),
                            "message": commit.get("commit", {}).get("message", ""),
                            "author": commit.get("commit", {}).get("author", {}).get("name", ""),
                            "date": commit.get("commit", {}).get("author", {}).get("date", "")
                        }
                        for commit in commits
                    ]
                }
                
                logger.info(f"Successfully retrieved details for repository: {username}/{repo_name}")
                return repo_details
            except httpx.HTTPError as e:
                logger.error(f"HTTP error during repository details retrieval: {str(e)}")
                try:
                    logger.error(f"Response content: {response.text}")
                except:
                    pass
                return None
    
    @staticmethod
    async def get_repository_contents(username: str, repo_name: str, path: str = "", access_token: str = None) -> List[Dict[str, Any]]:
        """
        Get contents of a repository directory.
        
        Args:
            username: The GitHub username.
            repo_name: The repository name.
            path: The path within the repository.
            access_token: Optional GitHub access token for authentication.
            
        Returns:
            List[Dict[str, Any]]: The directory contents if successful, empty list otherwise.
        """
        logger.info(f"Getting contents for repository: {username}/{repo_name}, path: {path}")
        
        headers = {"Accept": "application/json"}
        if access_token:
            headers["Authorization"] = f"Bearer {access_token}"
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    f"https://api.github.com/repos/{username}/{repo_name}/contents/{path}",
                    headers=headers
                )
                response.raise_for_status()
                contents = response.json()
                
                if isinstance(contents, list):
                    # Directory contents
                    return [
                        {
                            "name": item.get("name"),
                            "path": item.get("path"),
                            "type": item.get("type"),
                            "size": item.get("size"),
                            "html_url": item.get("html_url")
                        }
                        for item in contents
                    ]
                else:
                    # Single file
                    return [
                        {
                            "name": contents.get("name"),
                            "path": contents.get("path"),
                            "type": contents.get("type"),
                            "size": contents.get("size"),
                            "html_url": contents.get("html_url")
                        }
                    ]
            except httpx.HTTPError as e:
                logger.error(f"HTTP error during repository contents retrieval: {str(e)}")
                try:
                    logger.error(f"Response content: {response.text}")
                except:
                    pass
                return []
    
    @staticmethod
    async def get_file_content(username: str, repo_name: str, path: str, access_token: str = None) -> Optional[str]:
        """
        Get content of a specific file in a repository.
        
        Args:
            username: The GitHub username.
            repo_name: The repository name.
            path: The file path within the repository.
            access_token: Optional GitHub access token for authentication.
            
        Returns:
            Optional[str]: The file content if successful, None otherwise.
        """
        logger.info(f"Getting file content: {username}/{repo_name}/{path}")
        
        headers = {"Accept": "application/json"}
        if access_token:
            headers["Authorization"] = f"Bearer {access_token}"
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    f"https://api.github.com/repos/{username}/{repo_name}/contents/{path}",
                    headers=headers
                )
                response.raise_for_status()
                file_data = response.json()
                
                if file_data.get("type") == "file" and file_data.get("encoding") == "base64":
                    content = base64.b64decode(file_data.get("content", "")).decode("utf-8")
                    return content
                
                return None
            except httpx.HTTPError as e:
                logger.error(f"HTTP error during file content retrieval: {str(e)}")
                try:
                    logger.error(f"Response content: {response.text}")
                except:
                    pass
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
