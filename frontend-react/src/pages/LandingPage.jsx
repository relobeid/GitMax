import React from 'react';
import { motion } from 'framer-motion';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';

const LandingPage = () => {
  const { isAuthenticated, user, logout } = useAuth();
  const navigate = useNavigate();

  // Function to handle clicks on links that aren't implemented yet
  const handleNotImplemented = (e) => {
    e.preventDefault();
    alert('This feature is coming soon!');
  };

  // Function to handle logo click
  const handleLogoClick = (e) => {
    e.preventDefault();
    if (isAuthenticated) {
      navigate('/dashboard');
    } else {
      navigate('/');
    }
  };

  return (
    <div className="bg-gradient-to-br from-gray-900 to-black min-h-screen text-white">
      {/* Hero Section */}
      <header className="container mx-auto px-6 py-16">
        <nav className="flex justify-between items-center mb-16">
          <div className="flex items-center">
            <motion.div
              initial={{ rotate: -10, scale: 0.9 }}
              animate={{ rotate: 0, scale: 1 }}
              transition={{ duration: 0.5 }}
              onClick={handleLogoClick}
              className="cursor-pointer"
            >
              <span className="text-3xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-purple-400 to-purple-600">
                GitMax
              </span>
            </motion.div>
          </div>
          <div className="hidden md:flex space-x-8">
            <a href="#features" className="hover:text-purple-400 transition-colors">Features</a>
            <a href="#how-it-works" className="hover:text-purple-400 transition-colors">How It Works</a>
            <a href="#" onClick={handleNotImplemented} className="hover:text-purple-400 transition-colors">About</a>
          </div>
          <div className="flex space-x-4">
            {isAuthenticated ? (
              <>
                <Link to="/dashboard" className="px-4 py-2 rounded border border-purple-500 hover:bg-purple-500 hover:text-white transition-colors">
                  Dashboard
                </Link>
                <button
                  onClick={logout}
                  className="px-4 py-2 rounded bg-purple-600 hover:bg-purple-700 transition-colors"
                >
                  Logout
                </button>
              </>
            ) : (
              <>
                <Link to="/login" className="px-4 py-2 rounded border border-purple-500 hover:bg-purple-500 hover:text-white transition-colors">
                  Login with GitHub
                </Link>
                <Link to="/signup" className="px-4 py-2 rounded bg-purple-600 hover:bg-purple-700 transition-colors">
                  Sign Up with GitHub
                </Link>
              </>
            )}
          </div>
        </nav>

        <div className="flex flex-col md:flex-row items-center">
          <motion.div 
            className="md:w-1/2"
            initial={{ opacity: 0, x: -50 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.8 }}
          >
            <h1 className="text-5xl font-bold leading-tight mb-4">
              Maximize Your GitHub Profile for Career Success
            </h1>
            <p className="text-xl text-gray-300 mb-8">
              GitMax analyzes your GitHub repositories and provides personalized recommendations to improve your profile for job applications.
            </p>
            <div className="flex space-x-4">
              <Link to="/signup" className="px-8 py-3 rounded-lg bg-gradient-to-r from-purple-500 to-purple-700 hover:from-purple-600 hover:to-purple-800 transition-all shadow-lg hover:shadow-purple-500/30">
                Get Started
              </Link>
              <a href="#how-it-works" className="px-8 py-3 rounded-lg border border-purple-500 hover:bg-purple-500/10 transition-all">
                Learn More
              </a>
            </div>
          </motion.div>
          
          <motion.div 
            className="md:w-1/2 mt-12 md:mt-0"
            initial={{ opacity: 0, y: 50 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, delay: 0.2 }}
          >
            <div className="relative">
              <div className="absolute -inset-0.5 bg-gradient-to-r from-purple-500 to-purple-700 rounded-lg blur opacity-30"></div>
              <div className="relative bg-gray-900 p-6 rounded-lg border border-gray-800">
                <pre className="text-sm text-gray-300 overflow-x-auto">
                  <code>
{`{
  "profile_score": {
    "overall": 85,
    "code_quality": 90,
    "project_diversity": 82,
    "contribution_activity": 78
  },
  "recommendations": [
    "Add more documentation to your projects",
    "Contribute to open-source React libraries",
    "Showcase more full-stack applications"
  ]
}`}
                  </code>
                </pre>
              </div>
            </div>
          </motion.div>
        </div>
      </header>

      {/* Features Section */}
      <section id="features" className="py-20 bg-black/50">
        <div className="container mx-auto px-6">
          <motion.div 
            className="text-center mb-16"
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
            viewport={{ once: true }}
          >
            <h2 className="text-4xl font-bold mb-4">Powerful Features</h2>
            <p className="text-xl text-gray-400 max-w-2xl mx-auto">
              GitMax uses AI to analyze your GitHub profile and provide actionable insights.
            </p>
          </motion.div>

          <div className="grid md:grid-cols-3 gap-8">
            <motion.div 
              className="bg-gray-900 p-8 rounded-xl border border-gray-800"
              initial={{ opacity: 0, y: 30 }}
              whileInView={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5, delay: 0.1 }}
              viewport={{ once: true }}
            >
              <div className="w-16 h-16 bg-purple-600/20 rounded-lg flex items-center justify-center mb-6">
                <svg className="w-8 h-8 text-purple-500" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg">
                  <path d="M9 4.804A7.968 7.968 0 005.5 4c-1.255 0-2.443.29-3.5.804v10A7.969 7.969 0 015.5 14c1.669 0 3.218.51 4.5 1.385A7.962 7.962 0 0114.5 14c1.255 0 2.443.29 3.5.804v-10A7.968 7.968 0 0014.5 4c-1.255 0-2.443.29-3.5.804V12a1 1 0 11-2 0V4.804z"></path>
                </svg>
              </div>
              <h3 className="text-2xl font-bold mb-3">Repository Analysis</h3>
              <p className="text-gray-400">
                Deep analysis of your code repositories to identify strengths and areas for improvement.
              </p>
            </motion.div>

            <motion.div 
              className="bg-gray-900 p-8 rounded-xl border border-gray-800"
              initial={{ opacity: 0, y: 30 }}
              whileInView={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5, delay: 0.2 }}
              viewport={{ once: true }}
            >
              <div className="w-16 h-16 bg-purple-600/20 rounded-lg flex items-center justify-center mb-6">
                <svg className="w-8 h-8 text-purple-500" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg">
                  <path fillRule="evenodd" d="M10 2a1 1 0 011 1v1.323l3.954 1.582 1.599-.8a1 1 0 01.894 1.79l-1.233.616 1.738 5.42a1 1 0 01-.285 1.05A3.989 3.989 0 0115 15a3.989 3.989 0 01-2.667-1.019 1 1 0 01-.285-1.05l1.715-5.349L11 6.477V16h2a1 1 0 110 2H7a1 1 0 110-2h2V6.477L6.237 7.582l1.715 5.349a1 1 0 01-.285 1.05A3.989 3.989 0 015 15a3.989 3.989 0 01-2.667-1.019 1 1 0 01-.285-1.05l1.738-5.42-1.233-.617a1 1 0 01.894-1.788l1.599.799L9 4.323V3a1 1 0 011-1z" clipRule="evenodd"></path>
                </svg>
              </div>
              <h3 className="text-2xl font-bold mb-3">Profile Scoring</h3>
              <p className="text-gray-400">
                Get a comprehensive score for your GitHub profile based on your target job role.
              </p>
            </motion.div>

            <motion.div 
              className="bg-gray-900 p-8 rounded-xl border border-gray-800"
              initial={{ opacity: 0, y: 30 }}
              whileInView={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5, delay: 0.3 }}
              viewport={{ once: true }}
            >
              <div className="w-16 h-16 bg-purple-600/20 rounded-lg flex items-center justify-center mb-6">
                <svg className="w-8 h-8 text-purple-500" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg">
                  <path d="M7 3a1 1 0 000 2h6a1 1 0 100-2H7zM4 7a1 1 0 011-1h10a1 1 0 110 2H5a1 1 0 01-1-1zM2 11a2 2 0 012-2h12a2 2 0 012 2v4a2 2 0 01-2 2H4a2 2 0 01-2-2v-4z"></path>
                </svg>
              </div>
              <h3 className="text-2xl font-bold mb-3">Personalized Recommendations</h3>
              <p className="text-gray-400">
                Receive tailored recommendations to improve your GitHub profile for job applications.
              </p>
            </motion.div>
          </div>
        </div>
      </section>

      {/* How It Works Section */}
      <section id="how-it-works" className="py-20">
        <div className="container mx-auto px-6">
          <motion.div 
            className="text-center mb-16"
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
            viewport={{ once: true }}
          >
            <h2 className="text-4xl font-bold mb-4">How It Works</h2>
            <p className="text-xl text-gray-400 max-w-2xl mx-auto">
              GitMax uses AI to analyze your GitHub profile and provide actionable insights in three simple steps.
            </p>
          </motion.div>

          <div className="grid md:grid-cols-3 gap-8">
            <motion.div 
              className="relative"
              initial={{ opacity: 0, y: 30 }}
              whileInView={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5, delay: 0.1 }}
              viewport={{ once: true }}
            >
              <div className="absolute -left-4 -top-4 w-12 h-12 rounded-full bg-purple-600 flex items-center justify-center text-xl font-bold">1</div>
              <div className="bg-gray-900 p-8 rounded-xl border border-gray-800 pt-12">
                <h3 className="text-2xl font-bold mb-3">Connect Your GitHub</h3>
                <p className="text-gray-400">
                  Sign in with your GitHub account to give GitMax access to your repositories.
                </p>
              </div>
            </motion.div>

            <motion.div 
              className="relative"
              initial={{ opacity: 0, y: 30 }}
              whileInView={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5, delay: 0.2 }}
              viewport={{ once: true }}
            >
              <div className="absolute -left-4 -top-4 w-12 h-12 rounded-full bg-purple-600 flex items-center justify-center text-xl font-bold">2</div>
              <div className="bg-gray-900 p-8 rounded-xl border border-gray-800 pt-12">
                <h3 className="text-2xl font-bold mb-3">AI Analysis</h3>
                <p className="text-gray-400">
                  Our AI analyzes your repositories, code quality, and GitHub activity.
                </p>
              </div>
            </motion.div>

            <motion.div 
              className="relative"
              initial={{ opacity: 0, y: 30 }}
              whileInView={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5, delay: 0.3 }}
              viewport={{ once: true }}
            >
              <div className="absolute -left-4 -top-4 w-12 h-12 rounded-full bg-purple-600 flex items-center justify-center text-xl font-bold">3</div>
              <div className="bg-gray-900 p-8 rounded-xl border border-gray-800 pt-12">
                <h3 className="text-2xl font-bold mb-3">Get Recommendations</h3>
                <p className="text-gray-400">
                  Receive personalized recommendations to improve your profile for your target job role.
                </p>
              </div>
            </motion.div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 bg-gradient-to-br from-purple-900/50 to-black">
        <div className="container mx-auto px-6 text-center">
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
            viewport={{ once: true }}
          >
            <h2 className="text-4xl font-bold mb-4">Ready to Maximize Your GitHub Profile?</h2>
            <p className="text-xl text-gray-300 mb-8 max-w-2xl mx-auto">
              Join GitMax today and get personalized recommendations to improve your GitHub profile for job applications.
            </p>
            <Link to="/signup" className="px-8 py-3 rounded-lg bg-gradient-to-r from-purple-500 to-purple-700 hover:from-purple-600 hover:to-purple-800 transition-all shadow-lg hover:shadow-purple-500/30 text-lg font-medium">
              Get Started for Free
            </Link>
          </motion.div>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-black py-12">
        <div className="container mx-auto px-6">
          <div className="flex flex-col md:flex-row justify-between items-center">
            <div className="mb-8 md:mb-0">
              <span className="text-2xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-purple-400 to-purple-600">
                GitMax
              </span>
              <p className="text-gray-500 mt-2">© 2023 GitMax. All rights reserved.</p>
            </div>
            <div className="flex space-x-8">
              <a href="#" onClick={handleNotImplemented} className="text-gray-400 hover:text-purple-400 transition-colors">Privacy Policy</a>
              <a href="#" onClick={handleNotImplemented} className="text-gray-400 hover:text-purple-400 transition-colors">Terms of Service</a>
              <a href="#" onClick={handleNotImplemented} className="text-gray-400 hover:text-purple-400 transition-colors">Contact</a>
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default LandingPage; 