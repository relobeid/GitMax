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

  // Load user on mount
  useEffect(() => {
    const loadUser = async () => {
      try {
        // Check if user is authenticated
        if (AuthService.isAuthenticated()) {
          const userData = await AuthService.getCurrentUser();
          setUser(userData);
        }
      } catch (err) {
        console.error('Failed to load user:', err);
        setError('Failed to load user. Please try again.');
        // Clear token if there's an error
        AuthService.logout();
      } finally {
        setLoading(false);
      }
    };

    loadUser();
  }, []);

  /**
   * Login with GitHub
   */
  const loginWithGitHub = async () => {
    try {
      const url = await AuthService.initiateGitHubLogin();
      window.location.href = url;
    } catch (err) {
      console.error('Failed to login with GitHub:', err);
      setError('Failed to login with GitHub. Please try again.');
      throw err;
    }
  };

  /**
   * Handle GitHub callback
   * @param {string} code - The authorization code from GitHub
   */
  const handleGitHubCallback = async (code) => {
    try {
      setLoading(true);
      const { user: userData } = await AuthService.handleGitHubCallback(code);
      setUser(userData);
      return userData;
    } catch (err) {
      console.error('Failed to handle GitHub callback:', err);
      setError('Failed to complete GitHub authentication. Please try again.');
      throw err;
    } finally {
      setLoading(false);
    }
  };

  /**
   * Logout the current user
   */
  const logout = async () => {
    try {
      // Set user to null first to immediately update UI
      setUser(null);
      await AuthService.logout();
    } catch (err) {
      console.error('Failed to logout:', err);
      setError('Failed to logout. Please try again.');
      // User is still set to null, so the UI will show logged out state
    }
  };

  /**
   * Clear any authentication errors
   */
  const clearError = () => {
    setError(null);
  };

  // Context value
  const value = {
    user,
    loading,
    error,
    isAuthenticated: !!user,
    loginWithGitHub,
    handleGitHubCallback,
    logout,
    clearError,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

/**
 * Hook to use the authentication context
 * @returns {Object} Authentication context
 */
export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

export default AuthContext; 