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
      
      // Direct redirect to GitHub OAuth page
      window.location.href = response.data.url;
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
      
      // Store the token in localStorage for persistence
      if (access_token) {
        localStorage.setItem('token', access_token);
        console.log('Token stored in localStorage:', access_token.substring(0, 10) + '...');
      }
      
      // Store the user's GitHub account in recent accounts
      if (user && user.github_username) {
        // Get existing recent accounts
        const recentAccounts = JSON.parse(localStorage.getItem('recentGitHubAccounts') || '[]');
        
        // Create account object with timestamp
        const accountInfo = {
          id: user.id,
          github_id: user.github_id,
          github_username: user.github_username,
          avatar_url: user.avatar_url || `https://github.com/${user.github_username}.png`,
          last_login: new Date().toISOString(),
          last_login_relative: 'Just now'
        };
        
        // Check if account already exists
        const existingIndex = recentAccounts.findIndex(acc => acc.github_id === user.github_id);
        
        if (existingIndex !== -1) {
          // Update existing account
          recentAccounts[existingIndex] = {
            ...recentAccounts[existingIndex],
            ...accountInfo
          };
        } else {
          // Add new account
          recentAccounts.push(accountInfo);
        }
        
        // Store updated accounts list
        localStorage.setItem('recentGitHubAccounts', JSON.stringify(recentAccounts));
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
      
      // Try to get token from cookie first, then localStorage
      const response = await api.get('/api/auth/me', {
        withCredentials: true // This enables sending cookies with the request
      });
      
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
    // Remove token from localStorage
    localStorage.removeItem('token');
    console.log('Token removed from localStorage');
    
    try {
      // Call logout endpoint to clear the cookie
      await api.post('/api/auth/logout', {}, {
        withCredentials: true
      });
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
    // Check both cookie and localStorage
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
  },

  /**
   * Get recent GitHub accounts
   * @returns {Array} Array of recent GitHub accounts
   */
  getRecentGitHubAccounts: () => {
    try {
      const accounts = JSON.parse(localStorage.getItem('recentGitHubAccounts') || '[]');
      
      // Update relative timestamps
      return accounts.map(account => {
        if (account.last_login) {
          const lastLogin = new Date(account.last_login);
          const now = new Date();
          const diffMs = now - lastLogin;
          const diffDays = Math.floor(diffMs / (1000 * 60 * 60 * 24));
          const diffHours = Math.floor(diffMs / (1000 * 60 * 60));
          const diffMinutes = Math.floor(diffMs / (1000 * 60));
          
          let relativeTime = 'Just now';
          if (diffDays > 0) {
            relativeTime = `${diffDays} ${diffDays === 1 ? 'day' : 'days'} ago`;
          } else if (diffHours > 0) {
            relativeTime = `${diffHours} ${diffHours === 1 ? 'hour' : 'hours'} ago`;
          } else if (diffMinutes > 0) {
            relativeTime = `${diffMinutes} ${diffMinutes === 1 ? 'minute' : 'minutes'} ago`;
          }
          
          return {
            ...account,
            last_login_relative: relativeTime
          };
        }
        return account;
      });
    } catch (error) {
      console.error('Failed to get recent GitHub accounts:', error);
      return [];
    }
  }
};

export default AuthService; 