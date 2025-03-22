import React, { useState, useEffect } from 'react';
import { Link, useNavigate, useLocation } from 'react-router-dom';
import { motion } from 'framer-motion';
import { useAuth } from '../contexts/AuthContext';
import GitHubService from '../services/github';
import AuthService from '../services/auth';

const Dashboard = () => {
  const [profile, setProfile] = useState(null);
  const [repositories, setRepositories] = useState([]);
  const [activity, setActivity] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();

  // Handle token from URL if present (from OAuth redirect)
  useEffect(() => {
    const handleUrlToken = () => {
      const searchParams = new URLSearchParams(location.search);
      const token = searchParams.get('token');
      const isNewUser = searchParams.get('is_new_user') === 'true';

      if (token) {
        // Store the token and remove it from URL
        localStorage.setItem('token', token);
        
        // Display welcome message based on whether user is new or returning
        if (isNewUser) {
          // Could show a welcome notification here
          console.log('Welcome to GitMax! Your account has been created.');
        } else {
          console.log('Welcome back! You have successfully signed in.');
        }
        
        // Update URL to remove the token parameter
        const cleanUrl = window.location.pathname;
        window.history.replaceState({}, document.title, cleanUrl);
      }
    };

    handleUrlToken();
  }, [location]);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        
        // Fetch GitHub profile, repositories, and activity
        const profileData = await GitHubService.getProfile();
        setProfile(profileData);
        
        const reposData = await GitHubService.getRepositories();
        setRepositories(reposData);
        
        const activityData = await GitHubService.getActivity();
        setActivity(activityData);
      } catch (err) {
        console.error('Failed to fetch GitHub data:', err);
        setError('Failed to fetch GitHub data. Please try again.');
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  const handleLogout = async () => {
    try {
      await logout();
      navigate('/login');
    } catch (err) {
      console.error('Failed to logout:', err);
    }
  };

  // Format date for display
  const formatDate = (dateString) => {
    if (!dateString) return '';
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', { 
      year: 'numeric', 
      month: 'short', 
      day: 'numeric' 
    });
  };

  // Calculate time ago for display
  const timeAgo = (dateString) => {
    if (!dateString) return '';
    const date = new Date(dateString);
    const now = new Date();
    const seconds = Math.floor((now - date) / 1000);
    
    let interval = Math.floor(seconds / 31536000);
    if (interval >= 1) {
      return interval === 1 ? '1 year ago' : `${interval} years ago`;
    }
    
    interval = Math.floor(seconds / 2592000);
    if (interval >= 1) {
      return interval === 1 ? '1 month ago' : `${interval} months ago`;
    }
    
    interval = Math.floor(seconds / 86400);
    if (interval >= 1) {
      return interval === 1 ? '1 day ago' : `${interval} days ago`;
    }
    
    interval = Math.floor(seconds / 3600);
    if (interval >= 1) {
      return interval === 1 ? '1 hour ago' : `${interval} hours ago`;
    }
    
    interval = Math.floor(seconds / 60);
    if (interval >= 1) {
      return interval === 1 ? '1 minute ago' : `${interval} minutes ago`;
    }
    
    return seconds < 10 ? 'just now' : `${Math.floor(seconds)} seconds ago`;
  };

  // Loading state
  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen bg-gray-900">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-purple-500"></div>
      </div>
    );
  }

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
                  src={profile?.avatar_url || user?.avatar_url || 'https://avatars.githubusercontent.com/u/12345678'}
                  alt={profile?.name || user?.username || 'GitHub User'}
                />
              </div>
              <div className="ml-3 relative">
                <div>
                  <button
                    onClick={handleLogout}
                    className="ml-4 px-3 py-1 rounded-md text-sm font-medium text-white bg-gray-800 hover:bg-gray-700"
                  >
                    Logout
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </nav>

      {/* Error message */}
      {error && (
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 mt-4">
          <div className="p-3 bg-red-900/50 border border-red-500 text-red-200 rounded-md text-sm">
            {error}
          </div>
        </div>
      )}

      {/* Main content */}
      <main className="py-10">
        {/* Welcome Section */}
        <motion.div 
          className="px-4 py-6 sm:px-0"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
        >
          <div className="relative bg-gray-900 rounded-lg p-6 border border-gray-800">
            <h1 className="text-2xl font-bold text-white mb-2">Welcome back, {profile?.name || user?.username || 'GitHub User'}!</h1>
            <p className="text-gray-300">
              Here's an overview of your GitHub profile and recommendations.
            </p>
          </div>
        </motion.div>

        {/* Profile Section */}
        <motion.div 
          className="mt-8 px-4 sm:px-0"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.05 }}
        >
          <div className="bg-gray-900 overflow-hidden shadow rounded-lg border border-gray-800">
            <div className="px-4 py-5 sm:p-6">
              <div className="flex flex-col md:flex-row">
                <div className="flex-shrink-0 mb-4 md:mb-0 md:mr-6">
                  <img 
                    src={profile?.avatar_url || user?.avatar_url || 'https://avatars.githubusercontent.com/u/12345678'} 
                    alt={profile?.name || user?.username || 'GitHub User'} 
                    className="h-24 w-24 rounded-full border-2 border-purple-500"
                  />
                </div>
                <div className="flex-1">
                  <h2 className="text-xl font-bold text-white">{profile?.name || user?.username || 'GitHub User'}</h2>
                  <p className="text-gray-400">@{profile?.username || user?.username || 'github-user'}</p>
                  
                  {profile?.bio && (
                    <p className="mt-2 text-gray-300">{profile.bio}</p>
                  )}
                  
                  <div className="mt-3 flex flex-wrap gap-2">
                    {profile?.location && (
                      <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-gray-800 text-gray-300">
                        <svg className="mr-1 h-3 w-3" fill="currentColor" viewBox="0 0 20 20">
                          <path fillRule="evenodd" d="M5.05 4.05a7 7 0 119.9 9.9L10 18.9l-4.95-4.95a7 7 0 010-9.9zM10 11a2 2 0 100-4 2 2 0 000 4z" clipRule="evenodd" />
                        </svg>
                        {profile.location}
                      </span>
                    )}
                    
                    {profile?.company && (
                      <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-gray-800 text-gray-300">
                        <svg className="mr-1 h-3 w-3" fill="currentColor" viewBox="0 0 20 20">
                          <path fillRule="evenodd" d="M4 4a2 2 0 012-2h8a2 2 0 012 2v12a1 1 0 01-1 1h-2a1 1 0 01-1-1v-2a1 1 0 00-1-1H7a1 1 0 00-1 1v2a1 1 0 01-1 1H3a1 1 0 01-1-1V4zm3 1h2v2H7V5zm2 4H7v2h2V9zm2-4h2v2h-2V5zm2 4h-2v2h2V9z" clipRule="evenodd" />
                        </svg>
                        {profile.company}
                      </span>
                    )}
                    
                    {profile?.blog && (
                      <a 
                        href={profile.blog.startsWith('http') ? profile.blog : `https://${profile.blog}`} 
                        target="_blank" 
                        rel="noopener noreferrer"
                        className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-gray-800 text-gray-300 hover:bg-gray-700"
                      >
                        <svg className="mr-1 h-3 w-3" fill="currentColor" viewBox="0 0 20 20">
                          <path fillRule="evenodd" d="M12.586 4.586a2 2 0 112.828 2.828l-3 3a2 2 0 01-2.828 0 1 1 0 00-1.414 1.414 4 4 0 005.656 0l3-3a4 4 0 00-5.656-5.656l-1.5 1.5a1 1 0 101.414 1.414l1.5-1.5zm-5 5a2 2 0 012.828 0 1 1 0 101.414-1.414 4 4 0 00-5.656 0l-3 3a4 4 0 105.656 5.656l1.5-1.5a1 1 0 10-1.414-1.414l-1.5 1.5a2 2 0 11-2.828-2.828l3-3z" clipRule="evenodd" />
                        </svg>
                        Website
                      </a>
                    )}
                    
                    {profile?.twitter_username && (
                      <a 
                        href={`https://twitter.com/${profile.twitter_username}`} 
                        target="_blank" 
                        rel="noopener noreferrer"
                        className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-gray-800 text-gray-300 hover:bg-gray-700"
                      >
                        <svg className="mr-1 h-3 w-3" fill="currentColor" viewBox="0 0 20 20">
                          <path d="M6.29 18.251c7.547 0 11.675-6.253 11.675-11.675 0-.178 0-.355-.012-.53A8.348 8.348 0 0020 3.92a8.19 8.19 0 01-2.357.646 4.118 4.118 0 001.804-2.27 8.224 8.224 0 01-2.605.996 4.107 4.107 0 00-6.993 3.743 11.65 11.65 0 01-8.457-4.287 4.106 4.106 0 001.27 5.477A4.073 4.073 0 01.8 7.713v.052a4.105 4.105 0 003.292 4.022 4.095 4.095 0 01-1.853.07 4.108 4.108 0 003.834 2.85A8.233 8.233 0 010 16.407a11.616 11.616 0 006.29 1.84" />
                        </svg>
                        @{profile.twitter_username}
                      </a>
                    )}
                  </div>
                  
                  <div className="mt-4 grid grid-cols-2 sm:grid-cols-4 gap-4">
                    <div className="text-center">
                      <div className="text-2xl font-bold text-purple-500">{profile?.public_repos || repositories.length || 0}</div>
                      <div className="text-xs text-gray-400">Repositories</div>
                    </div>
                    <div className="text-center">
                      <div className="text-2xl font-bold text-purple-500">{profile?.followers || 0}</div>
                      <div className="text-xs text-gray-400">Followers</div>
                    </div>
                    <div className="text-center">
                      <div className="text-2xl font-bold text-purple-500">{profile?.following || 0}</div>
                      <div className="text-xs text-gray-400">Following</div>
                    </div>
                    <div className="text-center">
                      <div className="text-2xl font-bold text-purple-500">{profile?.public_gists || 0}</div>
                      <div className="text-xs text-gray-400">Gists</div>
                    </div>
                  </div>
                  
                  {profile?.created_at && (
                    <div className="mt-4 text-sm text-gray-400">
                      GitHub member since {formatDate(profile.created_at)}
                    </div>
                  )}
                </div>
              </div>
            </div>
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
                    {profile?.public_repos || repositories.length || 0}
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
                    {profile?.followers || 0}
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
                    {profile?.following || 0}
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
              {activity && activity.length > 0 ? (
                activity.slice(0, 5).map((item, index) => (
                  <li key={index}>
                    <div className="px-4 py-4 sm:px-6">
                      <div className="flex items-center justify-between">
                        <p className="text-sm font-medium text-purple-500 truncate">
                          {item.type === 'commit' ? (
                            <>Commit to {item.repo}: {item.message}</>
                          ) : item.type?.startsWith('created_') ? (
                            <>Created {item.type.replace('created_', '')} in {item.repo}</>
                          ) : item.type?.startsWith('issue_') ? (
                            <>{item.type.replace('issue_', 'Issue ')} in {item.repo}: {item.title}</>
                          ) : item.type?.startsWith('pull_request_') ? (
                            <>{item.type.replace('pull_request_', 'Pull request ')} in {item.repo}: {item.title}</>
                          ) : (
                            <>Activity in {item.repo}</>
                          )}
                        </p>
                        <div className="ml-2 flex-shrink-0 flex">
                          <p className="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-green-100 text-green-800">
                            {timeAgo(item.date)}
                          </p>
                        </div>
                      </div>
                    </div>
                  </li>
                ))
              ) : (
                <li>
                  <div className="px-4 py-4 sm:px-6 text-gray-400">
                    No recent activity found.
                  </div>
                </li>
              )}
            </ul>
          </div>
        </motion.div>
      </main>
    </div>
  );
};

export default Dashboard; 