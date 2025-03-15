import openai
from typing import Dict, List, Any, Optional
from app.utils.config import get_settings

settings = get_settings()

class ProfileScoringService:
    """Service for scoring GitHub profiles and generating recommendations using AI."""
    
    @staticmethod
    async def calculate_score(user_data: Dict[str, Any], repositories_analysis: List[Dict[str, Any]], job_role: str) -> Dict[str, Any]:
        """
        Calculate profile score based on job role using AI.
        
        Args:
            user_data: The user data.
            repositories_analysis: The repositories analysis data.
            job_role: The target job role.
            
        Returns:
            Dict[str, Any]: Score data.
        """
        # Configure OpenAI client
        client = openai.OpenAI(api_key=settings.openai_api_key)
        
        # Prepare data for scoring
        profile_summary = {
            "github_username": user_data.get("username"),
            "public_repos": user_data.get("public_repos"),
            "followers": user_data.get("followers"),
            "following": user_data.get("following"),
            "repositories_analysis": repositories_analysis,
            "job_role": job_role
        }
        
        # Generate score using OpenAI
        try:
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a GitHub profile analyzer that scores profiles for job readiness."},
                    {"role": "user", "content": f"Score this GitHub profile for the {job_role} role on a scale of 0-100. Provide a breakdown of scores in different categories and an overall score: {profile_summary}"}
                ]
            )
            
            scoring_analysis = response.choices[0].message.content
            
            # Extract overall score (this is a simplification - in production, we'd parse the AI response more carefully)
            # For now, we'll generate a score based on repository count and followers as a fallback
            try:
                # Try to extract score from AI response
                import re
                score_match = re.search(r'Overall Score:\s*(\d+)', scoring_analysis)
                overall_score = int(score_match.group(1)) if score_match else None
            except:
                overall_score = None
                
            # Fallback scoring if AI doesn't provide a clear score
            if overall_score is None:
                repo_count = user_data.get("public_repos", 0)
                followers = user_data.get("followers", 0)
                
                # Simple scoring algorithm as fallback
                overall_score = min(100, (repo_count * 5) + (followers * 2))
            
            # Structure the score data
            return {
                "job_role": job_role,
                "overall_score": overall_score,
                "analysis": scoring_analysis,
                "repositories_count": len(repositories_analysis),
                "followers_count": user_data.get("followers", 0)
            }
        except Exception as e:
            # Fallback scoring if AI fails
            repo_count = user_data.get("public_repos", 0)
            followers = user_data.get("followers", 0)
            
            # Simple scoring algorithm as fallback
            overall_score = min(100, (repo_count * 5) + (followers * 2))
            
            return {
                "job_role": job_role,
                "overall_score": overall_score,
                "analysis": f"Error generating analysis: {str(e)}",
                "repositories_count": len(repositories_analysis),
                "followers_count": user_data.get("followers", 0)
            }
    
    @staticmethod
    async def generate_recommendations(user_data: Dict[str, Any], score_data: Dict[str, Any], repositories_analysis: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Generate personalized recommendations based on score using AI.
        
        Args:
            user_data: The user data.
            score_data: The score data.
            repositories_analysis: The repositories analysis data.
            
        Returns:
            List[Dict[str, Any]]: List of recommendations.
        """
        # Configure OpenAI client
        client = openai.OpenAI(api_key=settings.openai_api_key)
        
        # Prepare data for recommendations
        recommendation_context = {
            "github_username": user_data.get("username"),
            "public_repos": user_data.get("public_repos"),
            "followers": user_data.get("followers"),
            "following": user_data.get("following"),
            "job_role": score_data.get("job_role"),
            "overall_score": score_data.get("overall_score"),
            "score_analysis": score_data.get("analysis"),
            "repositories_analysis": repositories_analysis
        }
        
        # Generate recommendations using OpenAI
        try:
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a GitHub profile advisor that provides actionable recommendations to improve a profile for job applications."},
                    {"role": "user", "content": f"Based on this GitHub profile analysis for a {score_data.get('job_role')} role, provide 5 specific, actionable recommendations to improve the profile: {recommendation_context}"}
                ]
            )
            
            recommendations_text = response.choices[0].message.content
            
            # Parse recommendations (in production, we'd parse this more carefully)
            import re
            recommendations_list = re.findall(r'\d+\.\s+(.*?)(?=\d+\.|$)', recommendations_text, re.DOTALL)
            
            # Clean up recommendations
            recommendations = []
            for i, rec in enumerate(recommendations_list):
                recommendations.append({
                    "id": i + 1,
                    "text": rec.strip(),
                    "category": "general"  # In production, we'd categorize these
                })
            
            # If no recommendations were parsed, create a fallback
            if not recommendations:
                recommendations = [
                    {"id": 1, "text": "Create more public repositories to showcase your skills.", "category": "general"},
                    {"id": 2, "text": "Add detailed README files to your projects.", "category": "documentation"},
                    {"id": 3, "text": "Contribute to open-source projects related to your target job role.", "category": "community"},
                    {"id": 4, "text": "Add topics and descriptions to your repositories.", "category": "metadata"},
                    {"id": 5, "text": "Increase your GitHub activity with regular commits.", "category": "activity"}
                ]
            
            return recommendations
        except Exception as e:
            # Fallback recommendations if AI fails
            return [
                {"id": 1, "text": "Create more public repositories to showcase your skills.", "category": "general"},
                {"id": 2, "text": "Add detailed README files to your projects.", "category": "documentation"},
                {"id": 3, "text": "Contribute to open-source projects related to your target job role.", "category": "community"},
                {"id": 4, "text": "Add topics and descriptions to your repositories.", "category": "metadata"},
                {"id": 5, "text": "Increase your GitHub activity with regular commits.", "category": "activity"}
            ] 