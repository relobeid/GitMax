import httpx
from typing import Dict, List, Any, Optional
import openai
from app.utils.config import get_settings

settings = get_settings()

class RepositoryAnalysisService:
    """Service for analyzing GitHub repositories using AI."""
    
    @staticmethod
    async def get_user_repositories(access_token: str) -> List[Dict[str, Any]]:
        """
        Fetch user repositories from GitHub API.
        
        Args:
            access_token: The GitHub access token.
            
        Returns:
            List[Dict[str, Any]]: List of repositories.
        """
        async with httpx.AsyncClient() as client:
            try:
                headers = {
                    "Authorization": f"Bearer {access_token}",
                    "Accept": "application/json",
                }
                response = await client.get(
                    "https://api.github.com/user/repos?sort=updated&per_page=10",
                    headers=headers
                )
                response.raise_for_status()
                return response.json()
            except httpx.HTTPError:
                return []
    
    @staticmethod
    async def get_repository_languages(access_token: str, repo_full_name: str) -> Dict[str, int]:
        """
        Get languages used in a repository.
        
        Args:
            access_token: The GitHub access token.
            repo_full_name: The full name of the repository (owner/repo).
            
        Returns:
            Dict[str, int]: Dictionary of languages and byte counts.
        """
        async with httpx.AsyncClient() as client:
            try:
                headers = {
                    "Authorization": f"Bearer {access_token}",
                    "Accept": "application/json",
                }
                response = await client.get(
                    f"https://api.github.com/repos/{repo_full_name}/languages",
                    headers=headers
                )
                response.raise_for_status()
                return response.json()
            except httpx.HTTPError:
                return {}
    
    @staticmethod
    async def analyze_repository_with_ai(repo_data: Dict[str, Any], languages_data: Dict[str, int]) -> Dict[str, Any]:
        """
        Analyze a repository using AI.
        
        Args:
            repo_data: The repository data.
            languages_data: The languages data.
            
        Returns:
            Dict[str, Any]: Analysis results.
        """
        # Configure OpenAI client
        client = openai.OpenAI(api_key=settings.openai_api_key)
        
        # Prepare repository data for analysis
        repo_summary = {
            "name": repo_data.get("name"),
            "description": repo_data.get("description"),
            "languages": languages_data,
            "stars": repo_data.get("stargazers_count"),
            "forks": repo_data.get("forks_count"),
            "issues": repo_data.get("open_issues_count"),
            "created_at": repo_data.get("created_at"),
            "updated_at": repo_data.get("updated_at"),
            "topics": repo_data.get("topics", [])
        }
        
        # Generate analysis using OpenAI
        try:
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a GitHub repository analyzer that provides insights for career development."},
                    {"role": "user", "content": f"Analyze this GitHub repository and provide insights on code quality, project significance, and career relevance: {repo_summary}"}
                ]
            )
            
            analysis = response.choices[0].message.content
            
            # Structure the analysis
            return {
                "repository": repo_data.get("name"),
                "analysis": analysis,
                "languages": languages_data,
                "metrics": {
                    "stars": repo_data.get("stargazers_count"),
                    "forks": repo_data.get("forks_count"),
                    "issues": repo_data.get("open_issues_count")
                }
            }
        except Exception as e:
            return {
                "repository": repo_data.get("name"),
                "analysis": f"Error analyzing repository: {str(e)}",
                "languages": languages_data,
                "metrics": {
                    "stars": repo_data.get("stargazers_count"),
                    "forks": repo_data.get("forks_count"),
                    "issues": repo_data.get("open_issues_count")
                }
            }
    
    @staticmethod
    async def analyze_all_repositories(access_token: str) -> List[Dict[str, Any]]:
        """
        Analyze all repositories for a user.
        
        Args:
            access_token: The GitHub access token.
            
        Returns:
            List[Dict[str, Any]]: Analysis results for all repositories.
        """
        # Get repositories
        repositories = await RepositoryAnalysisService.get_user_repositories(access_token)
        
        # Analyze each repository
        results = []
        for repo in repositories:
            # Get languages for the repository
            languages = await RepositoryAnalysisService.get_repository_languages(
                access_token, 
                repo.get("full_name")
            )
            
            # Analyze the repository
            analysis = await RepositoryAnalysisService.analyze_repository_with_ai(repo, languages)
            results.append(analysis)
        
        return results 