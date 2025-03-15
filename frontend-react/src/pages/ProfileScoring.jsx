import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { motion } from 'framer-motion';

const ProfileScoring = () => {
  const [jobRoles, setJobRoles] = useState([
    { id: 'frontend', name: 'Frontend Developer' },
    { id: 'backend', name: 'Backend Developer' },
    { id: 'fullstack', name: 'Full Stack Developer' },
    { id: 'mobile', name: 'Mobile Developer' },
    { id: 'devops', name: 'DevOps Engineer' },
    { id: 'data', name: 'Data Scientist' }
  ]);

  const [selectedRole, setSelectedRole] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [profileScore, setProfileScore] = useState(null);

  const handleRoleSelect = (role) => {
    setSelectedRole(role);
    setIsLoading(true);
    
    // Simulate API call
    setTimeout(() => {
      setIsLoading(false);
      setProfileScore({
        overall: 78,
        categories: [
          { name: 'Technical Skills', score: 82 },
          { name: 'Project Diversity', score: 75 },
          { name: 'Code Quality', score: 85 },
          { name: 'Collaboration', score: 70 },
          { name: 'Documentation', score: 65 }
        ],
        strengths: [
          'Strong JavaScript and React skills',
          'Good code organization and structure',
          'Regular commits and active development'
        ],
        weaknesses: [
          'Limited backend technology exposure',
          'Few collaborative projects',
          'Documentation could be improved'
        ],
        recommendations: [
          'Contribute to open-source React projects to showcase collaboration skills',
          'Add more documentation to your repositories',
          'Create a full-stack project that demonstrates backend skills',
          'Add unit tests to your projects to demonstrate testing knowledge',
          'Create a technical blog to share your knowledge'
        ]
      });
    }, 2000);
  };

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
                <Link to="/dashboard" className="border-transparent text-gray-300 hover:border-gray-300 hover:text-white inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium">
                  Dashboard
                </Link>
                <Link to="/repository-analysis" className="border-transparent text-gray-300 hover:border-gray-300 hover:text-white inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium">
                  Repository Analysis
                </Link>
                <Link to="/profile-scoring" className="border-purple-500 text-white inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium">
                  Profile Scoring
                </Link>
              </div>
            </div>
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
        <motion.div 
          className="px-4 py-6 sm:px-0"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
        >
          <div className="relative bg-gray-900 rounded-lg p-6 border border-gray-800">
            <h1 className="text-2xl font-bold text-white mb-2">Profile Scoring</h1>
            <p className="text-gray-300">
              Get a comprehensive score for your GitHub profile based on your target job role.
            </p>
          </div>
        </motion.div>

        <div className="mt-8 px-4 sm:px-0">
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            {/* Job Role Selection */}
            <motion.div 
              className="lg:col-span-1"
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.5, delay: 0.1 }}
            >
              <h2 className="text-xl font-bold text-white mb-4">Select Job Role</h2>
              <div className="bg-gray-900 shadow overflow-hidden sm:rounded-md border border-gray-800">
                <ul className="divide-y divide-gray-800">
                  {jobRoles.map((role) => (
                    <li key={role.id} className={`${selectedRole?.id === role.id ? 'bg-gray-800' : ''}`}>
                      <button
                        onClick={() => handleRoleSelect(role)}
                        className="w-full px-4 py-4 sm:px-6 text-left hover:bg-gray-800 transition-colors"
                      >
                        <div className="flex items-center justify-between">
                          <p className="text-sm font-medium text-purple-500 truncate">
                            {role.name}
                          </p>
                          {selectedRole?.id === role.id && (
                            <div className="ml-2 flex-shrink-0 flex">
                              <svg className="h-5 w-5 text-purple-500" fill="currentColor" viewBox="0 0 20 20">
                                <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                              </svg>
                            </div>
                          )}
                        </div>
                      </button>
                    </li>
                  ))}
                </ul>
              </div>
            </motion.div>

            {/* Profile Score Results */}
            <motion.div 
              className="lg:col-span-2"
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.5, delay: 0.2 }}
            >
              <h2 className="text-xl font-bold text-white mb-4">Profile Score</h2>
              
              {!selectedRole && (
                <div className="bg-gray-900 rounded-lg p-6 border border-gray-800 flex items-center justify-center h-64">
                  <p className="text-gray-400">Select a job role to see your profile score</p>
                </div>
              )}

              {isLoading && (
                <div className="bg-gray-900 rounded-lg p-6 border border-gray-800 flex flex-col items-center justify-center h-64">
                  <svg className="animate-spin h-10 w-10 text-purple-500 mb-4" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
                  <p className="text-gray-300">Analyzing your profile for {selectedRole?.name}...</p>
                </div>
              )}

              {selectedRole && profileScore && !isLoading && (
                <div className="bg-gray-900 rounded-lg border border-gray-800 overflow-hidden">
                  <div className="px-6 py-4 border-b border-gray-800">
                    <h3 className="text-lg font-medium text-white">Score for {selectedRole.name}</h3>
                  </div>
                  
                  <div className="px-6 py-4">
                    {/* Overall Score */}
                    <div className="flex items-center justify-center mb-6">
                      <div className="relative">
                        <svg className="w-32 h-32" viewBox="0 0 36 36">
                          <path
                            d="M18 2.0845
                              a 15.9155 15.9155 0 0 1 0 31.831
                              a 15.9155 15.9155 0 0 1 0 -31.831"
                            fill="none"
                            stroke="#4B5563"
                            strokeWidth="3"
                            strokeDasharray="100, 100"
                          />
                          <path
                            d="M18 2.0845
                              a 15.9155 15.9155 0 0 1 0 31.831
                              a 15.9155 15.9155 0 0 1 0 -31.831"
                            fill="none"
                            stroke="#8B5CF6"
                            strokeWidth="3"
                            strokeDasharray={`${profileScore.overall}, 100`}
                          />
                        </svg>
                        <div className="absolute inset-0 flex items-center justify-center">
                          <div className="text-center">
                            <div className="text-3xl font-bold text-white">{profileScore.overall}</div>
                            <div className="text-sm text-gray-400">Overall Score</div>
                          </div>
                        </div>
                      </div>
                    </div>

                    {/* Category Scores */}
                    <h4 className="text-md font-medium text-white mb-3">Category Scores</h4>
                    <div className="space-y-4 mb-6">
                      {profileScore.categories.map((category, index) => (
                        <div key={index}>
                          <div className="flex justify-between items-center mb-1">
                            <span className="text-sm text-gray-300">{category.name}</span>
                            <span className="text-sm font-medium text-purple-500">{category.score}%</span>
                          </div>
                          <div className="w-full bg-gray-800 rounded-full h-2">
                            <div 
                              className="bg-gradient-to-r from-purple-500 to-purple-700 h-2 rounded-full" 
                              style={{ width: `${category.score}%` }}
                            ></div>
                          </div>
                        </div>
                      ))}
                    </div>

                    <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
                      <div>
                        <h4 className="text-md font-medium text-white mb-2">Strengths</h4>
                        <ul className="list-disc pl-5 space-y-1">
                          {profileScore.strengths.map((strength, index) => (
                            <li key={index} className="text-sm text-gray-300">{strength}</li>
                          ))}
                        </ul>
                      </div>
                      <div>
                        <h4 className="text-md font-medium text-white mb-2">Areas for Improvement</h4>
                        <ul className="list-disc pl-5 space-y-1">
                          {profileScore.weaknesses.map((weakness, index) => (
                            <li key={index} className="text-sm text-gray-300">{weakness}</li>
                          ))}
                        </ul>
                      </div>
                    </div>

                    <div>
                      <h4 className="text-md font-medium text-white mb-2">Recommendations</h4>
                      <div className="bg-gray-800 rounded-lg p-4">
                        <ul className="space-y-2">
                          {profileScore.recommendations.map((recommendation, index) => (
                            <li key={index} className="flex items-start">
                              <svg className="h-5 w-5 text-purple-500 mr-2 mt-0.5" fill="currentColor" viewBox="0 0 20 20">
                                <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                              </svg>
                              <span className="text-sm text-gray-300">{recommendation}</span>
                            </li>
                          ))}
                        </ul>
                      </div>
                    </div>
                  </div>
                </div>
              )}
            </motion.div>
          </div>
        </div>
      </main>
    </div>
  );
};

export default ProfileScoring; 