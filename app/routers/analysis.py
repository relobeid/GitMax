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
        # Get GitHub access token (in a real app, we'd store this or have a refresh mechanism)
        # For this demo, we'll simulate having the token
        access_token = "simulated_access_token"  # In production, get this from a secure source
        
        # Analyze repositories
        analysis_results = await RepositoryAnalysisService.analyze_all_repositories(access_token)
        
        return analysis_results
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to analyze repositories: {str(e)}"
        )


@router.get("/score")
async def get_profile_score(
    job_role: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get the authenticated user's profile score for a specific job role.
    
    Args:
        job_role: The target job role.
        current_user: The authenticated user.
        db: The database session.
        
    Returns:
        Dict[str, Any]: Profile score data.
    """
    try:
        # Get GitHub access token (in a real app, we'd store this or have a refresh mechanism)
        # For this demo, we'll simulate having the token
        access_token = "simulated_access_token"  # In production, get this from a secure source
        
        # Get user data
        user_data = {
            "username": current_user.username,
            "github_id": current_user.github_id,
            "public_repos": current_user.public_repos,
            "followers": current_user.followers,
            "following": current_user.following,
            "github_url": current_user.github_url
        }
        
        # Analyze repositories
        repositories_analysis = await RepositoryAnalysisService.analyze_all_repositories(access_token)
        
        # Calculate score
        score_data = await ProfileScoringService.calculate_score(
            user_data,
            repositories_analysis,
            job_role
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
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get personalized recommendations for the authenticated user.
    
    Args:
        job_role: The target job role.
        current_user: The authenticated user.
        db: The database session.
        
    Returns:
        List[Dict[str, Any]]: Personalized recommendations.
    """
    try:
        # Get GitHub access token (in a real app, we'd store this or have a refresh mechanism)
        # For this demo, we'll simulate having the token
        access_token = "simulated_access_token"  # In production, get this from a secure source
        
        # Get user data
        user_data = {
            "username": current_user.username,
            "github_id": current_user.github_id,
            "public_repos": current_user.public_repos,
            "followers": current_user.followers,
            "following": current_user.following,
            "github_url": current_user.github_url
        }
        
        # Analyze repositories
        repositories_analysis = await RepositoryAnalysisService.analyze_all_repositories(access_token)
        
        # Calculate score
        score_data = await ProfileScoringService.calculate_score(
            user_data,
            repositories_analysis,
            job_role
        )
        
        # Generate recommendations
        recommendations = await ProfileScoringService.generate_recommendations(
            user_data,
            score_data,
            repositories_analysis
        )
        
        return recommendations
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate recommendations: {str(e)}"
        ) 