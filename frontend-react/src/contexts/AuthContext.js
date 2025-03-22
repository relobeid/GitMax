import React, { createContext, useState, useEffect, useContext } from 'react';
import AuthService from '../services/auth';

// Create the authentication context
const AuthContext = createContext();

/**
 * Authentication provider component
 * @param {Object} props - Component props
 * @returns {JSX.Element} AuthProvider component
 */
export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [recentAccounts, setRecentAccounts] = useState([]);

  // Load user and recent accounts on mount
  useEffect(() => {
    const loadUserAndAccounts = async () => {
      try {
        // Get recent accounts
        const accounts = AuthService.getRecentGitHubAccounts();
        setRecentAccounts(accounts);
        
        const token = localStorage.getItem('token');
        // Check if token exists
        if (token) {
          const userData = await AuthService.getCurrentUser();
          setUser(userData);
        } else {
          setUser(null);
        }
      } catch (err) {
        console.error('Failed to load user:', err);
        setError(err.response?.data?.detail || err.message || 'Failed to load user. Please try again.');
        // Clear token if there's an error
        AuthService.logout();
        setUser(null);
      } finally {
        setLoading(false);
      }
    };

    loadUserAndAccounts();
  }, []);

  /**
   * Login with GitHub
   */
  const loginWithGitHub = async () => {
    try {
      const url = await AuthService.initiateGitHubLogin();
      // The redirect happens in the service now
    } catch (err) {
      console.error('Failed to login with GitHub:', err);
      setError(err.response?.data?.detail || err.message || 'Failed to login with GitHub. Please try again.');
      throw err;
    }
  };

  /**
   * Handle GitHub callback
   * @param {string} code - The authorization code from GitHub
   */
  const handleGitHubCallback = async (code) => {
    try {
      const { token, user: userData } = await AuthService.handleGitHubCallback(code);
      
      if (userData) {
        setUser(userData);
        
        // Refresh recent accounts list
        const accounts = AuthService.getRecentGitHubAccounts();
        setRecentAccounts(accounts);
      }
      
      return { token, user: userData };
    } catch (err) {
      console.error('Failed to handle GitHub callback:', err);
      setError(err.response?.data?.detail || err.message || 'Failed to complete GitHub authentication.');
      throw err;
    }
  };

  /**
   * Logout user
   */
  const logout = async () => {
    try {
      await AuthService.logout();
      setUser(null);
      // Redirect to home page
      window.location.href = '/';
    } catch (err) {
      console.error('Failed to logout:', err);
      // Still clear local state even if server logout fails
      setUser(null);
      window.location.href = '/';
    }
  };

  // Provide auth context value
  const value = {
    user,
    loading,
    error,
    recentAccounts,
    loginWithGitHub,
    handleGitHubCallback,
    logout,
    isAuthenticated: !!user,
  };

  return (
    <AuthContext.Provider value={value}>
      {!loading && children}
    </AuthContext.Provider>
  );
};

// Custom hook to use auth context
export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

export default AuthContext; 