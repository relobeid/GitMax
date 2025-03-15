import api from './api';

/**
 * GitHub service for handling GitHub-related operations
 */
const GitHubService = {
  /**
   * Get the user's basic profile from our database
   * @returns {Promise} Promise that resolves to the basic profile data
   */
  getBasicProfile: async () => {
    try {
      const response = await api.get('/api/profile');
      return response.data;
    } catch (error) {
      console.error('Failed to get basic profile:', error);
      throw error;
    }
  },

  /**
   * Get the user's detailed GitHub profile
   * @returns {Promise} Promise that resolves to the detailed GitHub profile data
   */
  getProfile: async () => {
    try {
      const response = await api.get('/api/profile/github');
      return response.data;
    } catch (error) {
      console.error('Failed to get GitHub profile:', error);
      throw error;
    }
  },

  /**
   * Get the user's GitHub repositories
   * @returns {Promise} Promise that resolves to the GitHub repositories data
   */
  getRepositories: async () => {
    try {
      const response = await api.get('/api/profile/repositories');
      return response.data;
    } catch (error) {
      console.error('Failed to get GitHub repositories:', error);
      throw error;
    }
  },

  /**
   * Get the user's recent GitHub activity
   * @returns {Promise} Promise that resolves to the GitHub activity data
   */
  getActivity: async () => {
    try {
      const response = await api.get('/api/profile/activity');
      return response.data;
    } catch (error) {
      console.error('Failed to get GitHub activity:', error);
      throw error;
    }
  },

  /**
   * Get analysis for a specific repository
   * @param {string} repoName - The name of the repository
   * @returns {Promise} Promise that resolves to the repository analysis data
   */
  getRepositoryAnalysis: async (repoName) => {
    try {
      const response = await api.get(`/api/analysis/repository/${repoName}`);
      return response.data;
    } catch (error) {
      console.error(`Failed to get analysis for repository ${repoName}:`, error);
      throw error;
    }
  },

  /**
   * Get analysis for all repositories
   * @returns {Promise} Promise that resolves to the analysis data for all repositories
   */
  getAllRepositoriesAnalysis: async () => {
    try {
      const response = await api.get('/api/analysis/repositories');
      return response.data;
    } catch (error) {
      console.error('Failed to get analysis for all repositories:', error);
      throw error;
    }
  },

  /**
   * Get profile scoring based on job role
   * @param {string} jobRole - The job role to score against
   * @returns {Promise} Promise that resolves to the profile scoring data
   */
  getProfileScoring: async (jobRole) => {
    try {
      const response = await api.get(`/api/analysis/profile-scoring?job_role=${encodeURIComponent(jobRole)}`);
      return response.data;
    } catch (error) {
      console.error(`Failed to get profile scoring for job role ${jobRole}:`, error);
      throw error;
    }
  },

  /**
   * Get recommendations for improving GitHub profile
   * @param {string} jobRole - The job role to get recommendations for
   * @returns {Promise} Promise that resolves to the recommendations data
   */
  getRecommendations: async (jobRole) => {
    try {
      const response = await api.get(`/api/analysis/recommendations?job_role=${encodeURIComponent(jobRole)}`);
      return response.data;
    } catch (error) {
      console.error(`Failed to get recommendations for job role ${jobRole}:`, error);
      throw error;
    }
  }
};

export default GitHubService; 