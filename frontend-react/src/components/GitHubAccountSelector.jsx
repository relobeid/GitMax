import React from 'react';
import { motion } from 'framer-motion';

/**
 * GitHub account selector component.
 * This displays a list of GitHub accounts that have been previously used with GitMax
 * and allows the user to select one or sign in with a new account.
 */
const GitHubAccountSelector = ({ accounts, onSelectAccount, onNewAccount }) => {
  if (!accounts || accounts.length === 0) {
    return null;
  }

  return (
    <div className="fixed inset-0 bg-gray-900 bg-opacity-75 flex items-center justify-center z-50">
      <motion.div 
        className="bg-gray-800 rounded-lg shadow-xl max-w-md w-full p-6"
        initial={{ scale: 0.9, opacity: 0 }}
        animate={{ scale: 1, opacity: 1 }}
        transition={{ duration: 0.3 }}
      >
        <div className="text-center">
          <div className="inline-flex items-center justify-center h-20 w-20 rounded-full bg-gray-700 mb-4">
            <svg className="h-12 w-12 text-purple-500" fill="currentColor" viewBox="0 0 20 20">
              <path fillRule="evenodd" d="M10 0C4.477 0 0 4.477 0 10c0 4.42 2.87 8.17 6.84 9.5.5.08.66-.23.66-.5v-1.69c-2.77.6-3.36-1.34-3.36-1.34-.46-1.16-1.11-1.47-1.11-1.47-.91-.62.07-.6.07-.6 1 .07 1.53 1.03 1.53 1.03.87 1.52 2.34 1.07 2.91.83.09-.65.35-1.09.63-1.34-2.22-.25-4.55-1.11-4.55-4.92 0-1.11.38-2 1.03-2.71-.1-.25-.45-1.29.1-2.64 0 0 .84-.27 2.75 1.02.79-.22 1.65-.33 2.5-.33.85 0 1.71.11 2.5.33 1.91-1.29 2.75-1.02 2.75-1.02.55 1.35.2 2.39.1 2.64.65.71 1.03 1.6 1.03 2.71 0 3.82-2.34 4.66-4.57 4.91.36.31.69.92.69 1.85V19c0 .27.16.59.67.5C17.14 18.16 20 14.42 20 10A10 10 0 0010 0z" clipRule="evenodd" />
            </svg>
          </div>
          <h2 className="text-xl font-bold text-white mb-2">Choose a GitHub Account</h2>
          <p className="text-gray-400 mb-6">
            Select which GitHub account you want to use with GitMax
          </p>
        </div>

        <div className="space-y-3 mb-6">
          {accounts.map(account => (
            <button
              key={account.id}
              onClick={() => onSelectAccount(account)}
              className="w-full flex items-center space-x-3 p-3 rounded-lg bg-gray-700 hover:bg-gray-600 transition-colors"
            >
              <img 
                src={account.avatar_url} 
                alt={account.github_username} 
                className="h-10 w-10 rounded-full"
              />
              <div className="flex-1 text-left">
                <p className="text-white font-medium">{account.github_username}</p>
                <p className="text-gray-400 text-sm">Last used {account.last_login_relative}</p>
              </div>
            </button>
          ))}
        </div>

        <div className="border-t border-gray-700 pt-4">
          <button
            onClick={onNewAccount}
            className="w-full flex items-center justify-center space-x-2 p-3 rounded-lg bg-purple-600 hover:bg-purple-700 transition-colors text-white"
          >
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
            </svg>
            <span>Use Another Account</span>
          </button>
        </div>
      </motion.div>
    </div>
  );
};

export default GitHubAccountSelector; 