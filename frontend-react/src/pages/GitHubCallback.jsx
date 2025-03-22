import React, { useEffect, useState } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';

/**
 * GitHub callback page to handle OAuth callback
 * @returns {JSX.Element} GitHub callback page
 */
const GitHubCallback = () => {
  const { handleGitHubCallback } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();
  const [error, setError] = useState(null);
  const [message, setMessage] = useState('');
  const [isProcessing, setIsProcessing] = useState(true);

  useEffect(() => {
    const handleCallback = async () => {
      try {
        // Get the parameters from the URL
        const searchParams = new URLSearchParams(location.search);
        const code = searchParams.get('code');
        const token = searchParams.get('token');
        const isNewUser = searchParams.get('is_new_user') === 'true';

        if (token) {
          // If we have a token directly (from backend redirect), store it
          localStorage.setItem('token', token);
          
          // Show different message based on whether user is new or returning
          if (isNewUser) {
            setMessage('Welcome to GitMax! Your account has been created.');
          } else {
            setMessage('Welcome back! You have successfully signed in.');
          }
          
          // Immediately navigate to dashboard
          navigate('/dashboard');
          return;
        }

        if (!code) {
          throw new Error('No authorization code found in the URL');
        }

        // Handle the GitHub callback with the code
        const { token: newToken, user } = await handleGitHubCallback(code);
        
        if (!newToken) {
          throw new Error('No token received from server');
        }
        
        // Show different message based on whether user is new or returning
        if (user?.is_new_user) {
          setMessage('Welcome to GitMax! Your account has been created.');
        } else {
          setMessage('Welcome back! You have successfully signed in.');
        }
        
        // Immediately navigate to dashboard
        navigate('/dashboard');
        
      } catch (err) {
        console.error('Failed to handle GitHub callback:', err);
        setError(err.response?.data?.detail || err.message || 'Failed to complete GitHub authentication. Please try again.');
        setIsProcessing(false);
      }
    };

    handleCallback();
  }, [handleGitHubCallback, location.search, navigate]);

  // Only render this if there's an error - otherwise we should redirect immediately
  if (error) {
    return (
      <div className="flex flex-col items-center justify-center min-h-screen bg-gray-900 text-white p-4">
        <div className="max-w-md w-full bg-gray-800 rounded-lg shadow-lg p-8">
          <h1 className="text-2xl font-bold text-center mb-6">
            Authentication Failed
          </h1>
          <div className="text-center">
            <p className="text-red-500 mb-4">{error}</p>
            <button
              onClick={() => navigate('/login')}
              className="px-4 py-2 bg-purple-600 hover:bg-purple-700 rounded-md transition-colors"
            >
              Back to Login
            </button>
          </div>
        </div>
      </div>
    );
  }

  // Loading state while processing - should be brief
  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-900 text-white p-4">
      <div className="max-w-md w-full bg-gray-800 rounded-lg shadow-lg p-8">
        <h1 className="text-2xl font-bold text-center mb-6">
          Completing Authentication...
        </h1>
        <div className="flex justify-center">
          <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-purple-500"></div>
        </div>
      </div>
    </div>
  );
};

export default GitHubCallback; 