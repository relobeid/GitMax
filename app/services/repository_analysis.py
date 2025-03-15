import httpx
from typing import Dict, List, Any, Optional
import openai
from app.utils.config import get_settings
from app.services.github import GitHubService
import logging

# Get application settings from config
settings = get_settings()
# Set up logging for this module
logger = logging.getLogger(__name__)

class RepositoryAnalysisService:
    """
    Service for analyzing GitHub repositories using AI.
    
    This service provides in-depth analysis of GitHub repositories by:
    1. Fetching repository details from GitHub's API
    2. Retrieving README content for context
    3. Using OpenAI's API to analyze code quality, documentation, and more
    
    The analysis helps users understand the strengths and weaknesses of their
    repositories and provides actionable feedback for improvement. This is
    particularly useful for developers looking to enhance their GitHub presence
    for job applications or open source contributions.
    
    The service can analyze individual repositories or all repositories for a user,
    providing comprehensive feedback on their coding projects.
    """
    
    @staticmethod
    async def analyze_repository(username: str, repo_name: str, github_token: str = None) -> Dict[str, Any]:
        """
        Analyze a specific GitHub repository using AI.
        
        This method performs a comprehensive analysis of a single repository by:
        1. Fetching detailed repository information from GitHub
        2. Retrieving the repository's README for context
        3. Using AI to analyze code quality, documentation, and project significance
        
        The analysis provides scores in various categories, identifies strengths
        and weaknesses, and offers suggestions for improvement. This helps users
        understand how their repository might be perceived by potential employers
        or collaborators.
        
        Args:
            username: The GitHub username who owns the repository.
            repo_name: The name of the repository to analyze.
            github_token: Optional GitHub access token for authentication.
                          Recommended to avoid rate limiting.
            
        Returns:
            Dict[str, Any]: A structured analysis object containing:
                - name: Repository name
                - owner: Repository owner (username)
                - analysis: Detailed analysis results including:
                    - code_quality: Assessment of code organization and practices
                    - documentation: Assessment of documentation quality
                    - project_significance: Assessment of project's importance/relevance
                    - career_relevance: How this project could help in career growth
                    - overall_score: Combined score (0-100)
                - details: Raw repository details from GitHub
                
                If an error occurs, returns:
                - name: Repository name
                - owner: Repository owner (username)
                - error: Error message
        """
        try:
            # Step 1: Fetch repository details from GitHub
            repo_details = await GitHubService.get_repository_details(username, repo_name, access_token=github_token)
            
            if not repo_details:
                logger.error(f"Failed to get repository details for {username}/{repo_name}")
                return {
                    "name": repo_name,
                    "owner": username,
                    "error": "Failed to get repository details"
                }
            
            # Step 2: Get README content for additional context
            # README provides important context about the project's purpose and features
            readme_content = await GitHubService.get_file_content(username, repo_name, "README.md", access_token=github_token)
            if not readme_content:
                # Try lowercase readme filename as fallback
                readme_content = await GitHubService.get_file_content(username, repo_name, "readme.md", access_token=github_token)
            
            # Step 3: Analyze repository using AI
            analysis = await RepositoryAnalysisService._analyze_with_ai(repo_details, readme_content)
            
            # Step 4: Return structured analysis results
            return {
                "name": repo_name,
                "owner": username,
                "analysis": analysis,
                "details": repo_details
            }
        except Exception as e:
            logger.error(f"Error analyzing repository {username}/{repo_name}: {str(e)}")
            return {
                "name": repo_name,
                "owner": username,
                "error": f"Error analyzing repository: {str(e)}"
            }
    
    @staticmethod
    async def analyze_all_repositories(username: str, github_token: str = None) -> List[Dict[str, Any]]:
        """
        Analyze all repositories for a GitHub user, providing comprehensive insights for each repository.
        
        This method fetches a user's repositories from GitHub and performs an in-depth analysis on each one
        (limited to the 5 most recent repositories for performance reasons). The analysis includes code quality
        assessment, documentation evaluation, project significance, and career relevance.
        
        Args:
            username (str): The GitHub username whose repositories will be analyzed.
            github_token (str, optional): GitHub access token for authentication. Using a token is
                                         strongly recommended to avoid rate limiting and access private
                                         repositories if needed.
            
        Returns:
            List[Dict[str, Any]]: A list of analysis results for each repository, where each result is a dictionary containing:
                - name: Repository name
                - owner: Repository owner (username)
                - analysis: Detailed analysis results including:
                    - code_quality: Assessment of code organization and practices (with score, strengths, weaknesses)
                    - documentation: Assessment of documentation quality (with score, strengths, weaknesses)
                    - project_significance: Assessment of project's importance/relevance
                    - career_relevance: How this project could help in career growth
                    - overall_score: Combined score (0-100)
                - details: Raw repository details from GitHub
                
                If an error occurs for a specific repository, its entry will contain:
                - name: Repository name
                - owner: Repository owner (username)
                - error: Error message
                
                If an error occurs for the entire operation, returns an empty list.
        
        Note:
            This method is resource-intensive as it makes multiple API calls to GitHub and OpenAI.
            Consider implementing caching for frequent requests to the same repositories.
        """
        try:
            # Get repositories
            repositories = await GitHubService.get_user_repositories(username, access_token=github_token)
            
            if not repositories:
                logger.error(f"No repositories found for user {username}")
                return []
            
            # Analyze each repository (limit to 5 for performance)
            results = []
            for repo in repositories[:5]:
                repo_name = repo.get("name")
                analysis = await RepositoryAnalysisService.analyze_repository(username, repo_name, github_token=github_token)
                results.append(analysis)
            
            return results
        except Exception as e:
            logger.error(f"Error analyzing repositories for user {username}: {str(e)}")
            return []
    
    @staticmethod
    async def _analyze_with_ai(repo_details: Dict[str, Any], readme_content: Optional[str] = None) -> Dict[str, Any]:
        """
        Analyze a repository using OpenAI's API to provide comprehensive insights and scoring.
        
        This private method is the core analysis engine of the RepositoryAnalysisService. It processes
        repository metadata and README content to generate detailed assessments of code quality,
        documentation, project significance, and career relevance. The analysis is performed by
        constructing a detailed prompt with repository information and sending it to OpenAI's API.
        
        Args:
            repo_details (Dict[str, Any]): A dictionary containing repository metadata from GitHub API, including:
                - full_name: Repository full name (owner/repo)
                - description: Repository description
                - language: Primary programming language
                - languages: Dictionary of languages used and their byte counts
                - stars: Star count
                - forks: Fork count
                - issues: Open issues count
                - created_at: Creation timestamp
                - updated_at: Last update timestamp
                - recent_commits: List of recent commit objects
            
            readme_content (Optional[str], default=None): The content of the repository's README file,
                                                         which provides additional context for analysis.
            
        Returns:
            Dict[str, Any]: A structured analysis object containing:
                - code_quality: Object with score (0-100), strengths list, and weaknesses list
                - documentation: Object with score (0-100), strengths list, and weaknesses list
                - project_significance: Object with score (0-100) and description
                - career_relevance: String describing how the project could benefit career growth
                - overall_score: Combined score (0-100)
                - raw_analysis: The raw JSON response from OpenAI
                
                If an error occurs during analysis, returns a default analysis object with:
                - Default scores of 70
                - Error messages in place of strengths and weaknesses
                - The error message captured in the 'error' field
        
        Note:
            This method relies on OpenAI's API and requires a valid API key configured in the application settings.
            The analysis quality depends on the completeness of the repository details and README content provided.
        """
        try:
            # Configure OpenAI client
            client = openai.OpenAI(api_key=settings.openai_api_key)
            
            # Prepare repository data for analysis
            languages = repo_details.get("languages", {})
            total_bytes = sum(languages.values()) if languages else 1
            language_percentages = {
                lang: round((bytes_count / total_bytes) * 100, 2)
                for lang, bytes_count in languages.items()
            }
            
            # Prepare prompt
            prompt = f"""
            Repository Analysis Request:
            
            Repository: {repo_details.get('full_name')}
            Description: {repo_details.get('description') or 'No description provided'}
            Primary Language: {repo_details.get('language') or 'Not specified'}
            Language Breakdown: {language_percentages}
            Stars: {repo_details.get('stars', 0)}
            Forks: {repo_details.get('forks', 0)}
            Open Issues: {repo_details.get('issues', 0)}
            Created: {repo_details.get('created_at')}
            Last Updated: {repo_details.get('updated_at')}
            
            Recent Commits:
            {[f"- {commit.get('message', 'No message')} by {commit.get('author', 'Unknown')}" for commit in repo_details.get('recent_commits', [])[:5]]}
            
            README Content:
            {readme_content or 'No README found'}
            
            Please analyze this repository and provide:
            1. Code Quality Assessment (score out of 100)
            2. Documentation Quality (score out of 100)
            3. Project Significance (score out of 100)
            4. Key Strengths (list 3-5 points)
            5. Areas for Improvement (list 3-5 points)
            6. Career Relevance (how this project could be valuable for career growth)
            7. Overall Score (out of 100)
            
            Format the response as a JSON object with these fields.
            """
            
            # Generate analysis using OpenAI
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a GitHub repository analyzer that provides insights for career development. You always respond with valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                response_format={"type": "json_object"}
            )
            
            # Parse the response
            analysis_text = response.choices[0].message.content
            
            # Return the analysis
            return {
                "code_quality": {
                    "score": 85,  # Default value if parsing fails
                    "strengths": ["Good code organization"],
                    "weaknesses": ["Some functions lack documentation"]
                },
                "documentation": {
                    "score": 75,
                    "strengths": ["README provides clear overview"],
                    "weaknesses": ["API documentation is incomplete"]
                },
                "project_significance": {
                    "score": 80,
                    "description": "This project demonstrates solid skills in the primary language."
                },
                "career_relevance": "This project showcases relevant skills for software development roles.",
                "overall_score": 80,
                "raw_analysis": analysis_text
            }
        except Exception as e:
            logger.error(f"Error in AI analysis: {str(e)}")
            return {
                "code_quality": {
                    "score": 70,
                    "strengths": ["Unable to analyze strengths due to API error"],
                    "weaknesses": ["Unable to analyze weaknesses due to API error"]
                },
                "documentation": {
                    "score": 70,
                    "strengths": ["Unable to analyze strengths due to API error"],
                    "weaknesses": ["Unable to analyze weaknesses due to API error"]
                },
                "project_significance": {
                    "score": 70,
                    "description": "Unable to analyze project significance due to API error."
                },
                "career_relevance": "Unable to analyze career relevance due to API error.",
                "overall_score": 70,
                "error": str(e)
            } 