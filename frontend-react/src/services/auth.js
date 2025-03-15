import api from './api';

/**
 * Authentication service for handling user authentication
 */
const AuthService = {
  /**
   * Initiate GitHub OAuth login
   * @returns {Promise} Promise that resolves to the GitHub OAuth URL
   */
  initiateGitHubLogin: async () => {
    try {
      console.log('Initiating GitHub login...');
      const response = await api.get('/api/auth/login');
      console.log('GitHub login URL:', response.data.url);
      return response.data.url;
    } catch (error) {
      console.error('Failed to initiate GitHub login:', error);
      console.error('Error details:', error.response?.data || error.message);
      throw error;
    }
  },

  /**
   * Handle GitHub OAuth callback
   * @param {string} code - The authorization code from GitHub
   * @returns {Promise} Promise that resolves to the user data and token
   */
  handleGitHubCallback: async (code) => {
    try {
      console.log('Handling GitHub callback with code:', code);
      const response = await api.post('/api/auth/callback', { code });
      console.log('GitHub callback response:', response.data);
      const { access_token, user } = response.data;
      
      // Store the token in localStorage
      localStorage.setItem('token', access_token);
      console.log('Token stored in localStorage:', access_token.substring(0, 10) + '...');
      
      // Verify the token works by making a test request
      try {
        console.log('Testing token with /api/auth/me endpoint...');
        const testResponse = await api.get('/api/auth/me');
        console.log('Token test successful:', testResponse.data);
      } catch (testError) {
        console.error('Token test failed:', testError);
        console.error('Token test error details:', testError.response?.data || testError.message);
      }
      
      return { token: access_token, user };
    } catch (error) {
      console.error('Failed to handle GitHub callback:', error);
      console.error('Error details:', error.response?.data || error.message);
      throw error;
    }
  },

  /**
   * Get the current authenticated user
   * @returns {Promise} Promise that resolves to the user data
   */
  getCurrentUser: async () => {
    try {
      console.log('Getting current user...');
      console.log('Current token:', localStorage.getItem('token')?.substring(0, 10) + '...');
      
      // Log the request headers
      const token = localStorage.getItem('token');
      console.log('Authorization header will be:', token ? `Bearer ${token.substring(0, 10)}...` : 'None');
      
      const response = await api.get('/api/auth/me');
      console.log('Current user data:', response.data);
      return response.data;
    } catch (error) {
      console.error('Failed to get current user:', error);
      console.error('Error details:', error.response?.data || error.message);
      throw error;
    }
  },

  /**
   * Logout the current user
   * @returns {Promise} Promise that resolves when logout is complete
   */
  logout: async () => {
    console.log('Logging out...');
    // Remove token from localStorage first
    localStorage.removeItem('token');
    console.log('Token removed from localStorage');
    
    try {
      // Try to call the logout endpoint, but don't wait for it
      await api.post('/api/auth/logout');
      return { success: true };
    } catch (error) {
      console.error('Failed to call logout endpoint:', error);
      console.error('Error details:', error.response?.data || error.message);
      // Return success anyway since we've already removed the token
      return { success: true };
    }
  },

  /**
   * Check if the user is authenticated
   * @returns {boolean} True if the user is authenticated
   */
  isAuthenticated: () => {
    const token = localStorage.getItem('token');
    console.log('Checking authentication, token exists:', !!token);
    return !!token;
  },

  /**
   * Get the authentication token
   * @returns {string|null} The authentication token or null if not authenticated
   */
  getToken: () => {
    return localStorage.getItem('token');
  }
};

export default AuthService; 