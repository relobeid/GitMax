import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { motion } from 'framer-motion';

const Dashboard = () => {
  const [user, setUser] = useState({
    name: 'John Doe',
    username: 'johndoe',
    avatar: 'https://avatars.githubusercontent.com/u/12345678',
    repositories: 15,
    followers: 120,
    following: 80
  });

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 to-black text-white">
      {/* Navigation */}
      <nav className="bg-gray-900 border-b border-gray-800">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16">
            <div className="flex">
              <div className="flex-shrink-0 flex items-center">
                <Link to="/">
                  <span className="text-2xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-purple-400 to-purple-600">
                    GitMax
                  </span>
                </Link>
              </div>
              <div className="hidden sm:ml-6 sm:flex sm:space-x-8">
                <Link to="/dashboard" className="border-purple-500 text-white inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium">
                  Dashboard
                </Link>
                <Link to="/repository-analysis" className="border-transparent text-gray-300 hover:border-gray-300 hover:text-white inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium">
                  Repository Analysis
                </Link>
                <Link to="/profile-scoring" className="border-transparent text-gray-300 hover:border-gray-300 hover:text-white inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium">
                  Profile Scoring
                </Link>
              </div>
            </div>
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <img
                  className="h-8 w-8 rounded-full"
                  src={user.avatar}
                  alt={user.name}
                />
              </div>
              <div className="ml-3 relative">
                <div>
                  <button
                    type="button"
                    className="max-w-xs bg-gray-800 rounded-full flex items-center text-sm focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-offset-gray-800 focus:ring-white"
                    id="user-menu-button"
                  >
                    <span className="sr-only">Open user menu</span>
                    <span className="ml-2 text-gray-300 text-sm font-medium lg:block">
                      <span className="sr-only">Open user menu for </span>
                      {user.username}
                    </span>
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
        {/* Welcome Section */}
        <motion.div 
          className="px-4 py-6 sm:px-0"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
        >
          <div className="relative bg-gray-900 rounded-lg p-6 border border-gray-800">
            <h1 className="text-2xl font-bold text-white mb-2">Welcome back, {user.name}!</h1>
            <p className="text-gray-300">
              Here's an overview of your GitHub profile and recommendations.
            </p>
          </div>
        </motion.div>

        {/* Stats Section */}
        <motion.div 
          className="mt-8 px-4 sm:px-0"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.1 }}
        >
          <h2 className="text-xl font-bold text-white mb-4">Your GitHub Stats</h2>
          <div className="grid grid-cols-1 gap-5 sm:grid-cols-3">
            <div className="bg-gray-900 overflow-hidden shadow rounded-lg border border-gray-800">
              <div className="px-4 py-5 sm:p-6">
                <dl>
                  <dt className="text-sm font-medium text-gray-400 truncate">
                    Repositories
                  </dt>
                  <dd className="mt-1 text-3xl font-semibold text-purple-500">
                    {user.repositories}
                  </dd>
                </dl>
              </div>
            </div>
            <div className="bg-gray-900 overflow-hidden shadow rounded-lg border border-gray-800">
              <div className="px-4 py-5 sm:p-6">
                <dl>
                  <dt className="text-sm font-medium text-gray-400 truncate">
                    Followers
                  </dt>
                  <dd className="mt-1 text-3xl font-semibold text-purple-500">
                    {user.followers}
                  </dd>
                </dl>
              </div>
            </div>
            <div className="bg-gray-900 overflow-hidden shadow rounded-lg border border-gray-800">
              <div className="px-4 py-5 sm:p-6">
                <dl>
                  <dt className="text-sm font-medium text-gray-400 truncate">
                    Following
                  </dt>
                  <dd className="mt-1 text-3xl font-semibold text-purple-500">
                    {user.following}
                  </dd>
                </dl>
              </div>
            </div>
          </div>
        </motion.div>

        {/* Quick Actions */}
        <motion.div 
          className="mt-8 px-4 sm:px-0"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.2 }}
        >
          <h2 className="text-xl font-bold text-white mb-4">Quick Actions</h2>
          <div className="grid grid-cols-1 gap-5 sm:grid-cols-2">
            <Link to="/repository-analysis" className="group">
              <div className="bg-gray-900 overflow-hidden shadow rounded-lg border border-gray-800 hover:border-purple-500 transition-colors">
                <div className="px-4 py-5 sm:p-6">
                  <h3 className="text-lg font-medium text-white group-hover:text-purple-400 transition-colors">Analyze Your Repositories</h3>
                  <p className="mt-2 text-sm text-gray-400">
                    Get detailed analysis of your code repositories to identify strengths and areas for improvement.
                  </p>
                </div>
              </div>
            </Link>
            <Link to="/profile-scoring" className="group">
              <div className="bg-gray-900 overflow-hidden shadow rounded-lg border border-gray-800 hover:border-purple-500 transition-colors">
                <div className="px-4 py-5 sm:p-6">
                  <h3 className="text-lg font-medium text-white group-hover:text-purple-400 transition-colors">Score Your Profile</h3>
                  <p className="mt-2 text-sm text-gray-400">
                    Get a comprehensive score for your GitHub profile based on your target job role.
                  </p>
                </div>
              </div>
            </Link>
          </div>
        </motion.div>

        {/* Recent Activity */}
        <motion.div 
          className="mt-8 px-4 sm:px-0 mb-12"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.3 }}
        >
          <h2 className="text-xl font-bold text-white mb-4">Recent Activity</h2>
          <div className="bg-gray-900 shadow overflow-hidden sm:rounded-md border border-gray-800">
            <ul className="divide-y divide-gray-800">
              <li>
                <div className="px-4 py-4 sm:px-6">
                  <div className="flex items-center justify-between">
                    <p className="text-sm font-medium text-purple-500 truncate">
                      Updated repository: react-portfolio
                    </p>
                    <div className="ml-2 flex-shrink-0 flex">
                      <p className="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-green-100 text-green-800">
                        2 days ago
                      </p>
                    </div>
                  </div>
                  <div className="mt-2 sm:flex sm:justify-between">
                    <div className="sm:flex">
                      <p className="flex items-center text-sm text-gray-400">
                        3 commits
                      </p>
                    </div>
                  </div>
                </div>
              </li>
              <li>
                <div className="px-4 py-4 sm:px-6">
                  <div className="flex items-center justify-between">
                    <p className="text-sm font-medium text-purple-500 truncate">
                      Created repository: node-api-starter
                    </p>
                    <div className="ml-2 flex-shrink-0 flex">
                      <p className="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-green-100 text-green-800">
                        5 days ago
                      </p>
                    </div>
                  </div>
                  <div className="mt-2 sm:flex sm:justify-between">
                    <div className="sm:flex">
                      <p className="flex items-center text-sm text-gray-400">
                        Initial commit
                      </p>
                    </div>
                  </div>
                </div>
              </li>
              <li>
                <div className="px-4 py-4 sm:px-6">
                  <div className="flex items-center justify-between">
                    <p className="text-sm font-medium text-purple-500 truncate">
                      Forked repository: awesome-react-components
                    </p>
                    <div className="ml-2 flex-shrink-0 flex">
                      <p className="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-green-100 text-green-800">
                        1 week ago
                      </p>
                    </div>
                  </div>
                  <div className="mt-2 sm:flex sm:justify-between">
                    <div className="sm:flex">
                      <p className="flex items-center text-sm text-gray-400">
                        Fork
                      </p>
                    </div>
                  </div>
                </div>
              </li>
            </ul>
          </div>
        </motion.div>
      </main>
    </div>
  );
};

export default Dashboard; 