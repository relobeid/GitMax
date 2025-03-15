from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.utils.config import get_settings
from app.database import get_db, User
from app.auth import get_current_user
from app.services.repository_analysis import RepositoryAnalysisService
from app.services.profile_scoring import ProfileScoringService
from app.services.github import GitHubService
from typing import List, Dict, Any

settings = get_settings()

router = APIRouter(
    prefix=f"{settings.api_prefix}/analysis",
    tags=["analysis"],
)


@router.get("/repositories")
async def analyze_repositories(current_user: User = Depends(get_current_user)):
    """
    Analyze the authenticated user's repositories.
    
    Args:
        current_user: The authenticated user.
        
    Returns:
        List[Dict[str, Any]]: Analysis results for all repositories.
    """
    try:
        # Analyze repositories using the enhanced service with GitHub token
        analysis_results = await RepositoryAnalysisService.analyze_all_repositories(
            current_user.username,
            github_token=current_user.github_token
        )
        
        return analysis_results
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to analyze repositories: {str(e)}"
        )


@router.get("/repository/{repo_name}")
async def analyze_repository(
    repo_name: str,
    current_user: User = Depends(get_current_user)
):
    """
    Analyze a specific repository.
    
    Args:
        repo_name: The name of the repository to analyze.
        current_user: The authenticated user.
        
    Returns:
        Dict[str, Any]: Analysis results for the repository.
    """
    try:
        # Analyze the repository using the enhanced service with GitHub token
        analysis_result = await RepositoryAnalysisService.analyze_repository(
            current_user.username,
            repo_name,
            github_token=current_user.github_token
        )
        
        return analysis_result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to analyze repository: {str(e)}"
        )


@router.get("/profile-scoring")
async def get_profile_score(
    job_role: str,
    current_user: User = Depends(get_current_user)
):
    """
    Get the authenticated user's profile score for a specific job role.
    
    Args:
        job_role: The target job role.
        current_user: The authenticated user.
        
    Returns:
        Dict[str, Any]: Profile score data.
    """
    try:
        # Score the profile using the enhanced service with GitHub token
        score_data = await ProfileScoringService.score_profile(
            current_user.username,
            job_role,
            github_token=current_user.github_token
        )
        
        return score_data
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to calculate profile score: {str(e)}"
        )


@router.get("/recommendations")
async def get_recommendations(
    job_role: str,
    current_user: User = Depends(get_current_user)
):
    """
    Get personalized recommendations for the authenticated user.
    
    Args:
        job_role: The target job role.
        current_user: The authenticated user.
        
    Returns:
        List[Dict[str, Any]]: Personalized recommendations.
    """
    try:
        # Generate recommendations using the enhanced service with GitHub token
        recommendations = await ProfileScoringService.generate_recommendations(
            current_user.username,
            job_role,
            github_token=current_user.github_token
        )
        
        return recommendations
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate recommendations: {str(e)}"
        ) 