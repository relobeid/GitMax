import httpx
from typing import Dict, Any, Optional, List
from app.utils.config import get_settings
from pydantic import BaseModel
import logging
import base64

# Get application settings from config
settings = get_settings()
# Set up logging for this module
logger = logging.getLogger(__name__)

class UserCreate(BaseModel):
    """
    Pydantic model for creating a new user from GitHub data.
    
    This model defines the structure of user data we extract from GitHub's API
    and use to create a new user in our database.
    """
    github_id: str          # Unique GitHub ID for the user
    username: str           # GitHub username
    email: Optional[str]    # User's email (may be private/null)
    avatar_url: Optional[str]  # URL to user's GitHub avatar
    public_repos: int       # Count of public repositories
    followers: int          # Count of followers
    following: int          # Count of users they follow
    github_url: str         # URL to their GitHub profile

class GitHubService:
    """
    Service for interacting with the GitHub API.
    
    This service handles all communication with GitHub's API, including:
    - OAuth authentication flow (exchanging code for token)
    - Fetching user profile data
    - Retrieving repositories and their details
    - Getting file contents
    
    The service uses access tokens for authentication to avoid rate limiting.
    GitHub has strict rate limits for unauthenticated requests (60 per hour),
    but authenticated requests get a much higher limit (5,000 per hour).
    
    Most methods accept an optional access_token parameter that should be
    passed whenever available to ensure API calls don't hit rate limits.
    """
    
    @staticmethod
    async def get_access_token(code: str) -> Optional[str]:
        """
        Exchange authorization code for access token in the OAuth flow.
        
        This is part of the GitHub OAuth flow:
        1. User is redirected to GitHub to authorize our app
        2. GitHub redirects back to our callback URL with a temporary code
        3. We exchange that code for an access token using this method
        4. The access token is then used for all future API requests
        
        Args:
            code: The temporary authorization code from GitHub.
            
        Returns:
            Optional[str]: The access token if successful, None otherwise.
        """
        # Log the exchange attempt (hiding most of the code for security)
        logger.info(f"Exchanging code for access token. Code: {code[:5]}...")
        logger.info(f"Using client_id: {settings.github_client_id[:5]}... and redirect_uri: {settings.github_redirect_uri}")
        
        # Use httpx for async HTTP requests
        async with httpx.AsyncClient() as client:
            try:
                # Make POST request to GitHub's token endpoint
                response = await client.post(
                    "https://github.com/login/oauth/access_token",
                    data={
                        "client_id": settings.github_client_id,
                        "client_secret": settings.github_client_secret,
                        "code": code,
                        "redirect_uri": settings.github_redirect_uri,
                    },
                    headers={"Accept": "application/json"}  # Request JSON response
                )
                response.raise_for_status()  # Raise exception for HTTP errors
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
        Get basic user data from GitHub API using an access token.
        
        This method fetches the authenticated user's basic profile information
        from GitHub's API. It's typically called right after obtaining an access
        token during the OAuth flow to get the user's GitHub ID, username, etc.
        
        The data returned by this method is used to:
        1. Create a new user in our database if they don't exist
        2. Update an existing user's information if they do exist
        
        This method requires an access token and uses GitHub's authenticated API,
        which has higher rate limits than unauthenticated requests.
        
        Args:
            access_token: The GitHub access token obtained from OAuth.
            
        Returns:
            Optional[Dict[str, Any]]: The user data if successful, including:
                - id: GitHub user ID
                - login: GitHub username
                - avatar_url: URL to user's avatar
                - email: User's email (if public)
                - name: User's display name
                - bio: User's bio
                - public_repos: Count of public repositories
                - followers: Count of followers
                - following: Count of users they follow
                - html_url: URL to their GitHub profile
                
            Returns None if the request fails.
        """
        logger.info("Getting user data from GitHub API")
        
        async with httpx.AsyncClient() as client:
            try:
                # Set up authentication headers with the access token
                headers = {
                    "Authorization": f"Bearer {access_token}",
                    "Accept": "application/json",
                }
                
                # Make authenticated request to GitHub's user endpoint
                response = await client.get(
                    "https://api.github.com/user",
                    headers=headers
                )
                response.raise_for_status()  # Raise exception for HTTP errors
                
                # Parse the JSON response
                user_data = response.json()
                logger.info(f"Successfully retrieved GitHub user data for: {user_data.get('login')}")
                return user_data
            except httpx.HTTPError as e:
                # Log detailed error information for debugging
                logger.error(f"HTTP error during user data retrieval: {str(e)}")
                try:
                    logger.error(f"Response content: {response.text}")
                except:
                    pass
                return None
    
    @staticmethod
    async def get_user_profile(username: str, access_token: str = None) -> Optional[Dict[str, Any]]:
        """
        Get comprehensive user profile data from GitHub API by aggregating multiple endpoints.
        
        This method provides a much more detailed profile than get_user_data by:
        1. Fetching basic user information (name, bio, etc.)
        2. Retrieving the user's repositories
        3. Getting the user's recent activity (commits, PRs, issues)
        4. Calculating language statistics from repositories
        
        It makes multiple API calls and combines the results into a single comprehensive
        profile object that can be used to display a complete GitHub profile in the UI.
        
        Using an access token is highly recommended to avoid rate limiting, especially
        since this method makes multiple API calls for a single profile.
        
        Args:
            username: The GitHub username to fetch the profile for.
            access_token: Optional GitHub access token for authentication.
                          Strongly recommended to avoid rate limiting.
            
        Returns:
            Optional[Dict[str, Any]]: A comprehensive profile object containing:
                - Basic user info (username, name, avatar_url, bio, etc.)
                - Follower and following counts
                - Repository statistics and details
                - Language usage statistics
                - Recent activity (commits, PRs, issues)
                
            Returns None if any of the API requests fail.
        """
        logger.info(f"Getting detailed profile for user: {username}")
        
        # Set up headers with authentication if token is provided
        headers = {"Accept": "application/json"}
        if access_token:
            headers["Authorization"] = f"Bearer {access_token}"
        
        async with httpx.AsyncClient() as client:
            try:
                # Step 1: Get basic user data (profile info)
                user_response = await client.get(
                    f"https://api.github.com/users/{username}",
                    headers=headers
                )
                user_response.raise_for_status()
                user_data = user_response.json()
                
                # Step 2: Get user's repositories (most recently updated)
                repos_response = await client.get(
                    f"https://api.github.com/users/{username}/repos",
                    headers=headers,
                    params={"sort": "updated", "per_page": 10}  # Get 10 most recently updated repos
                )
                repos_response.raise_for_status()
                repos_data = repos_response.json()
                
                # Step 3: Get user's recent activity (events)
                events_response = await client.get(
                    f"https://api.github.com/users/{username}/events/public",
                    headers=headers,
                    params={"per_page": 10}
                )
                events_response.raise_for_status()
                events_data = events_response.json()
                
                # Step 4: Calculate language statistics from repositories
                # This helps us understand which languages the user works with most frequently
                languages = {}
                for repo in repos_data:
                    lang = repo.get("language")
                    if lang:
                        languages[lang] = languages.get(lang, 0) + 1
                
                # Sort languages by frequency (most used first)
                sorted_languages = sorted(languages.items(), key=lambda x: x[1], reverse=True)
                
                # Step 5: Format recent activity into a more usable structure
                # GitHub's event data is complex, so we transform it into a simpler format
                recent_activity = []
                for event in events_data[:5]:  # Process only the 5 most recent events
                    event_type = event.get("type", "")
                    repo_name = event.get("repo", {}).get("name", "")
                    created_at = event.get("created_at", "")
                    
                    # Handle different event types differently
                    if event_type == "PushEvent":
                        # For push events, extract individual commits
                        commits = event.get("payload", {}).get("commits", [])
                        for commit in commits:
                            recent_activity.append({
                                "type": "commit",
                                "repo": repo_name,
                                "message": commit.get("message", ""),
                                "date": created_at
                            })
                    elif event_type == "CreateEvent":
                        # For creation events (new branch, tag, etc.)
                        ref_type = event.get("payload", {}).get("ref_type", "")
                        recent_activity.append({
                            "type": f"created_{ref_type}",
                            "repo": repo_name,
                            "date": created_at
                        })
                    elif event_type == "IssuesEvent":
                        # For issue events (opened, closed, etc.)
                        action = event.get("payload", {}).get("action", "")
                        issue_title = event.get("payload", {}).get("issue", {}).get("title", "")
                        recent_activity.append({
                            "type": f"issue_{action}",
                            "repo": repo_name,
                            "title": issue_title,
                            "date": created_at
                        })
                    elif event_type == "PullRequestEvent":
                        # For pull request events
                        action = event.get("payload", {}).get("action", "")
                        pr_title = event.get("payload", {}).get("pull_request", {}).get("title", "")
                        recent_activity.append({
                            "type": f"pull_request_{action}",
                            "repo": repo_name,
                            "title": pr_title,
                            "date": created_at
                        })
                
                # Step 6: Combine all data into a comprehensive profile object
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
        Get a user's GitHub repositories with detailed information.
        
        This method fetches a list of repositories owned by the specified user,
        sorted by most recently updated. It's used to display repository lists
        in the UI and for analysis of a user's coding activity and skills.
        
        The method transforms GitHub's repository data into a simplified format
        that contains only the fields we need for our application, making it
        easier to work with in the frontend.
        
        Using an access token is recommended to avoid rate limiting, especially
        for users with many repositories.
        
        Args:
            username: The GitHub username whose repositories to fetch.
            access_token: Optional GitHub access token for authentication.
                          Recommended to avoid rate limiting.
            
        Returns:
            List[Dict[str, Any]]: A list of repository objects, each containing:
                - id: Repository ID
                - name: Repository name
                - description: Repository description
                - language: Primary programming language
                - stars: Number of stars
                - forks: Number of forks
                - issues: Number of open issues
                - updated_at: Last update timestamp
                - html_url: URL to the repository on GitHub
                
            Returns an empty list if the API request fails.
        """
        logger.info(f"Getting repositories for user: {username}")
        
        # Set up headers with authentication if token is provided
        headers = {"Accept": "application/json"}
        if access_token:
            headers["Authorization"] = f"Bearer {access_token}"
        
        async with httpx.AsyncClient() as client:
            try:
                # Fetch repositories, sorted by most recently updated
                response = await client.get(
                    f"https://api.github.com/users/{username}/repos",
                    headers=headers,
                    params={"sort": "updated", "per_page": 10}  # Get 10 most recently updated repos
                )
                response.raise_for_status()
                repos = response.json()
                logger.info(f"Successfully retrieved {len(repos)} repositories for user: {username}")
                
                # Transform the data to match our expected format
                # This simplifies the data structure and makes it easier to work with
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
        Get comprehensive details about a specific GitHub repository, including languages, contributors, and recent commits.
        
        This method makes multiple API calls to GitHub to gather detailed information about a repository,
        including basic metadata, language statistics, top contributors, and recent commit history.
        The collected data is structured into a single comprehensive dictionary that provides a complete
        overview of the repository's characteristics and activity.
        
        Args:
            username (str): The GitHub username who owns the repository.
            repo_name (str): The name of the repository to fetch details for.
            access_token (str, optional): GitHub access token for authentication. Using a token is
                                         recommended to avoid rate limiting and access private repositories.
            
        Returns:
            Optional[Dict[str, Any]]: A comprehensive dictionary containing repository details if successful:
                - id: Repository ID
                - name: Repository name
                - full_name: Full repository name (username/repo_name)
                - description: Repository description
                - language: Primary programming language
                - languages: Dictionary of all languages used and their byte counts
                - stars: Number of stargazers
                - forks: Number of forks
                - issues: Number of open issues
                - watchers: Number of watchers
                - created_at: Repository creation timestamp
                - updated_at: Last update timestamp
                - pushed_at: Last push timestamp
                - html_url: GitHub URL for the repository
                - contributors: List of top contributors with username, avatar URL, and contribution count
                - recent_commits: List of recent commits with SHA, message, author, and date
                
                Returns None if any API call fails or the repository doesn't exist.
        
        Note:
            This method makes multiple API calls to GitHub, which may count against rate limits.
            Using an access token is recommended for better rate limits.
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
        Get contents of a repository directory or information about a specific file.
        
        This method retrieves the contents of a specified path within a GitHub repository.
        It can return either a list of items in a directory or information about a single file,
        depending on whether the specified path points to a directory or a file. The method
        standardizes the return format to always be a list, even for a single file.
        
        Args:
            username (str): The GitHub username who owns the repository.
            repo_name (str): The name of the repository to explore.
            path (str, default=""): The path within the repository to get contents for.
                                   An empty string retrieves the root directory contents.
            access_token (str, optional): GitHub access token for authentication. Using a token is
                                         recommended to avoid rate limiting and access private repositories.
            
        Returns:
            List[Dict[str, Any]]: A list of dictionaries, each representing a file or directory:
                - name: File or directory name
                - path: Full path within the repository
                - type: Item type ("file" or "dir")
                - size: File size in bytes (0 for directories)
                - html_url: GitHub URL for viewing the item
                
                Returns an empty list if the path doesn't exist or any API call fails.
        
        Note:
            - For directories, returns a list of all items in that directory
            - For a single file, returns a list with one item containing that file's metadata
            - This method does NOT return the actual content of files, only metadata
            - To get file content, use the get_file_content method instead
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
        Get the actual content of a specific file in a GitHub repository.
        
        This method retrieves the raw content of a file from a GitHub repository by making an API call
        to fetch the file data, which is typically base64 encoded. The method handles the decoding
        process and returns the file content as a UTF-8 string. This is particularly useful for
        retrieving text-based files like READMEs, source code, configuration files, etc.
        
        Args:
            username (str): The GitHub username who owns the repository.
            repo_name (str): The name of the repository containing the file.
            path (str): The path to the file within the repository (e.g., "README.md", "src/main.py").
            access_token (str, optional): GitHub access token for authentication. Using a token is
                                         recommended to avoid rate limiting and access private repositories.
            
        Returns:
            Optional[str]: The decoded content of the file as a UTF-8 string if successful.
                          Returns None if:
                          - The file doesn't exist
                          - The path points to a directory instead of a file
                          - The file content is not base64 encoded
                          - Any API call fails
                          - The content cannot be decoded as UTF-8
        
        Note:
            - This method is designed for text files and may not work correctly with binary files
            - For large files, GitHub may not return the full content through the API
            - Some files may require authentication to access, especially in private repositories
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
