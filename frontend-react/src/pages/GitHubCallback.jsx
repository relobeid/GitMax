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

  useEffect(() => {
    const handleCallback = async () => {
      try {
        // Get the parameters from the URL
        const searchParams = new URLSearchParams(location.search);
        const code = searchParams.get('code');
        const token = searchParams.get('token');

        if (token) {
          // If we have a token directly (from backend redirect), store it
          localStorage.setItem('token', token);
          navigate('/dashboard');
          return;
        }

        if (!code) {
          throw new Error('No authorization code found in the URL');
        }

        // Handle the GitHub callback with the code
        await handleGitHubCallback(code);

        // Redirect to dashboard on success
        navigate('/dashboard');
      } catch (err) {
        console.error('Failed to handle GitHub callback:', err);
        setError('Failed to complete GitHub authentication. Please try again.');
      }
    };

    handleCallback();
  }, [handleGitHubCallback, location.search, navigate]);

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-900 text-white p-4">
      <div className="max-w-md w-full bg-gray-800 rounded-lg shadow-lg p-8">
        <h1 className="text-2xl font-bold text-center mb-6">
          {error ? 'Authentication Failed' : 'Completing Authentication...'}
        </h1>

        {error ? (
          <div className="text-center">
            <p className="text-red-500 mb-4">{error}</p>
            <button
              onClick={() => navigate('/login')}
              className="px-4 py-2 bg-purple-600 hover:bg-purple-700 rounded-md transition-colors"
            >
              Back to Login
            </button>
          </div>
        ) : (
          <div className="flex justify-center">
            <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-purple-500"></div>
          </div>
        )}
      </div>
    </div>
  );
};

export default GitHubCallback; 