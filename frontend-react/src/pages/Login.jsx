import React, { useEffect, useState } from 'react';
import { Link, useNavigate, useLocation } from 'react-router-dom';
import { motion } from 'framer-motion';
import { useAuth } from '../contexts/AuthContext';
import GitHubAccountSelector from '../components/GitHubAccountSelector';

const Login = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const { loginWithGitHub, isAuthenticated, recentAccounts } = useAuth();
  const [showAccountSelector, setShowAccountSelector] = useState(false);

  // Redirect if already authenticated
  useEffect(() => {
    if (isAuthenticated) {
      const from = location.state?.from?.pathname || '/dashboard';
      navigate(from, { replace: true });
    }
  }, [isAuthenticated, navigate, location]);

  const handleAccountSelect = (account) => {
    // Store the selected account to localStorage to remember it
    localStorage.setItem('selectedGitHubAccount', account.github_username);
    // Hide the selector
    setShowAccountSelector(false);
    // Proceed with GitHub login
    loginWithGitHub();
  };

  const handleNewAccount = () => {
    // Hide the selector
    setShowAccountSelector(false);
    // Clear selected account if any
    localStorage.removeItem('selectedGitHubAccount');
    // Proceed with GitHub login
    loginWithGitHub();
  };

  const handleLoginClick = () => {
    // Always show the account selector if we have accounts, even just one
    if (recentAccounts.length > 0 && !showAccountSelector) {
      setShowAccountSelector(true);
    } else {
      // Otherwise proceed directly to GitHub login
      loginWithGitHub();
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 to-black flex flex-col justify-center py-12 sm:px-6 lg:px-8">
      <motion.div 
        className="sm:mx-auto sm:w-full sm:max-w-md"
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
      >
        <Link to="/">
          <h2 className="text-center text-3xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-purple-400 to-purple-600">
            GitMax
          </h2>
        </Link>
        <h2 className="mt-6 text-center text-3xl font-extrabold text-white">
          Sign in to GitMax
        </h2>
        <p className="mt-2 text-center text-sm text-gray-400">
          New to GitMax?{' '}
          <Link to="/signup" className="font-medium text-purple-500 hover:text-purple-400">
            Create an account
          </Link>
        </p>
      </motion.div>

      <motion.div 
        className="mt-8 sm:mx-auto sm:w-full sm:max-w-md"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.2 }}
      >
        <div className="bg-gray-800 py-8 px-6 shadow rounded-lg sm:px-10">
          <div className="mb-6 text-center">
            <p className="text-gray-300 mb-4">
              Sign in with your GitHub account to access GitMax's features. We'll analyze your GitHub profile to provide personalized insights and recommendations.
            </p>
          </div>
          
          <div className="space-y-6">
            <button
              onClick={handleLoginClick}
              className="w-full flex justify-center py-3 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-purple-600 hover:bg-purple-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-purple-500 transition-colors"
            >
              <svg className="w-5 h-5 mr-2" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M10 0C4.477 0 0 4.477 0 10c0 4.42 2.87 8.17 6.84 9.5.5.08.66-.23.66-.5v-1.69c-2.77.6-3.36-1.34-3.36-1.34-.46-1.16-1.11-1.47-1.11-1.47-.91-.62.07-.6.07-.6 1 .07 1.53 1.03 1.53 1.03.87 1.52 2.34 1.07 2.91.83.09-.65.35-1.09.63-1.34-2.22-.25-4.55-1.11-4.55-4.92 0-1.11.38-2 1.03-2.71-.1-.25-.45-1.29.1-2.64 0 0 .84-.27 2.75 1.02.79-.22 1.65-.33 2.5-.33.85 0 1.71.11 2.5.33 1.91-1.29 2.75-1.02 2.75-1.02.55 1.35.2 2.39.1 2.64.65.71 1.03 1.6 1.03 2.71 0 3.82-2.34 4.66-4.57 4.91.36.31.69.92.69 1.85V19c0 .27.16.59.67.5C17.14 18.16 20 14.42 20 10A10 10 0 0010 0z" clipRule="evenodd" />
              </svg>
              Continue with GitHub
            </button>
            
            <p className="text-xs text-center text-gray-400">
              By signing in, you agree to our{' '}
              <Link to="/terms" className="text-purple-500 hover:text-purple-400">Terms of Service</Link>
              {' '}and{' '}
              <Link to="/privacy" className="text-purple-500 hover:text-purple-400">Privacy Policy</Link>
            </p>
          </div>
        </div>
      </motion.div>

      {/* GitHub Account Selector */}
      {showAccountSelector && (
        <GitHubAccountSelector 
          accounts={recentAccounts}
          onSelectAccount={handleAccountSelect}
          onNewAccount={handleNewAccount}
        />
      )}
    </div>
  );
};

export default Login; 