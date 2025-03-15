import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { motion } from 'framer-motion';

const RepositoryAnalysis = () => {
  const [repositories, setRepositories] = useState([
    { id: 1, name: 'react-portfolio', language: 'JavaScript', stars: 12, forks: 5, analyzed: true },
    { id: 2, name: 'node-api-starter', language: 'JavaScript', stars: 8, forks: 3, analyzed: false },
    { id: 3, name: 'python-data-analysis', language: 'Python', stars: 15, forks: 7, analyzed: false },
    { id: 4, name: 'flutter-mobile-app', language: 'Dart', stars: 6, forks: 2, analyzed: false },
    { id: 5, name: 'personal-blog', language: 'HTML/CSS', stars: 3, forks: 1, analyzed: false }
  ]);

  const [selectedRepo, setSelectedRepo] = useState(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [analysis, setAnalysis] = useState(null);

  const handleAnalyze = (repo) => {
    setSelectedRepo(repo);
    setIsAnalyzing(true);
    
    // Simulate API call
    setTimeout(() => {
      setIsAnalyzing(false);
      setAnalysis({
        codeQuality: 85,
        documentation: 70,
        testCoverage: 60,
        architecture: 80,
        strengths: [
          'Well-structured component hierarchy',
          'Good use of modern JavaScript features',
          'Responsive design implementation'
        ],
        weaknesses: [
          'Limited test coverage',
          'Some components could be more reusable',
          'Documentation could be improved'
        ],
        recommendations: [
          'Add more unit tests to increase coverage',
          'Refactor larger components into smaller, reusable ones',
          'Add more inline documentation for complex functions'
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
                <Link to="/repository-analysis" className="border-purple-500 text-white inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium">
                  Repository Analysis
                </Link>
                <Link to="/profile-scoring" className="border-transparent text-gray-300 hover:border-gray-300 hover:text-white inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium">
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
            <h1 className="text-2xl font-bold text-white mb-2">Repository Analysis</h1>
            <p className="text-gray-300">
              Select a repository to analyze its code quality, structure, and get personalized recommendations.
            </p>
          </div>
        </motion.div>

        <div className="mt-8 px-4 sm:px-0">
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            {/* Repository List */}
            <motion.div 
              className="lg:col-span-1"
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.5, delay: 0.1 }}
            >
              <h2 className="text-xl font-bold text-white mb-4">Your Repositories</h2>
              <div className="bg-gray-900 shadow overflow-hidden sm:rounded-md border border-gray-800">
                <ul className="divide-y divide-gray-800">
                  {repositories.map((repo) => (
                    <li key={repo.id} className={`${selectedRepo?.id === repo.id ? 'bg-gray-800' : ''}`}>
                      <button
                        onClick={() => handleAnalyze(repo)}
                        className="w-full px-4 py-4 sm:px-6 text-left hover:bg-gray-800 transition-colors"
                      >
                        <div className="flex items-center justify-between">
                          <p className="text-sm font-medium text-purple-500 truncate">
                            {repo.name}
                          </p>
                          <div className="ml-2 flex-shrink-0 flex">
                            <p className="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-gray-700 text-gray-300">
                              {repo.language}
                            </p>
                          </div>
                        </div>
                        <div className="mt-2 sm:flex sm:justify-between">
                          <div className="sm:flex">
                            <p className="flex items-center text-sm text-gray-400">
                              <svg className="flex-shrink-0 mr-1.5 h-4 w-4 text-gray-400" fill="currentColor" viewBox="0 0 20 20">
                                <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
                              </svg>
                              {repo.stars} stars
                            </p>
                            <p className="mt-2 flex items-center text-sm text-gray-400 sm:mt-0 sm:ml-6">
                              <svg className="flex-shrink-0 mr-1.5 h-4 w-4 text-gray-400" fill="currentColor" viewBox="0 0 20 20">
                                <path fillRule="evenodd" d="M12.316 3.051a1 1 0 01.633 1.265l-4 12a1 1 0 11-1.898-.632l4-12a1 1 0 011.265-.633zM5.707 6.293a1 1 0 010 1.414L3.414 10l2.293 2.293a1 1 0 11-1.414 1.414l-3-3a1 1 0 010-1.414l3-3a1 1 0 011.414 0zm8.586 0a1 1 0 011.414 0l3 3a1 1 0 010 1.414l-3 3a1 1 0 11-1.414-1.414L16.586 10l-2.293-2.293a1 1 0 010-1.414z" clipRule="evenodd" />
                              </svg>
                              {repo.forks} forks
                            </p>
                          </div>
                        </div>
                      </button>
                    </li>
                  ))}
                </ul>
              </div>
            </motion.div>

            {/* Analysis Results */}
            <motion.div 
              className="lg:col-span-2"
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.5, delay: 0.2 }}
            >
              <h2 className="text-xl font-bold text-white mb-4">Analysis Results</h2>
              
              {!selectedRepo && (
                <div className="bg-gray-900 rounded-lg p-6 border border-gray-800 flex items-center justify-center h-64">
                  <p className="text-gray-400">Select a repository to see analysis results</p>
                </div>
              )}

              {isAnalyzing && (
                <div className="bg-gray-900 rounded-lg p-6 border border-gray-800 flex flex-col items-center justify-center h-64">
                  <svg className="animate-spin h-10 w-10 text-purple-500 mb-4" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
                  <p className="text-gray-300">Analyzing {selectedRepo?.name}...</p>
                </div>
              )}

              {selectedRepo && analysis && !isAnalyzing && (
                <div className="bg-gray-900 rounded-lg border border-gray-800 overflow-hidden">
                  <div className="px-6 py-4 border-b border-gray-800">
                    <h3 className="text-lg font-medium text-white">{selectedRepo.name}</h3>
                  </div>
                  
                  <div className="px-6 py-4">
                    <h4 className="text-md font-medium text-white mb-2">Scores</h4>
                    <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
                      <div className="bg-gray-800 p-3 rounded-lg">
                        <div className="text-sm text-gray-400">Code Quality</div>
                        <div className="text-2xl font-bold text-purple-500">{analysis.codeQuality}%</div>
                      </div>
                      <div className="bg-gray-800 p-3 rounded-lg">
                        <div className="text-sm text-gray-400">Documentation</div>
                        <div className="text-2xl font-bold text-purple-500">{analysis.documentation}%</div>
                      </div>
                      <div className="bg-gray-800 p-3 rounded-lg">
                        <div className="text-sm text-gray-400">Test Coverage</div>
                        <div className="text-2xl font-bold text-purple-500">{analysis.testCoverage}%</div>
                      </div>
                      <div className="bg-gray-800 p-3 rounded-lg">
                        <div className="text-sm text-gray-400">Architecture</div>
                        <div className="text-2xl font-bold text-purple-500">{analysis.architecture}%</div>
                      </div>
                    </div>

                    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                      <div>
                        <h4 className="text-md font-medium text-white mb-2">Strengths</h4>
                        <ul className="list-disc pl-5 space-y-1">
                          {analysis.strengths.map((strength, index) => (
                            <li key={index} className="text-sm text-gray-300">{strength}</li>
                          ))}
                        </ul>
                      </div>
                      <div>
                        <h4 className="text-md font-medium text-white mb-2">Areas for Improvement</h4>
                        <ul className="list-disc pl-5 space-y-1">
                          {analysis.weaknesses.map((weakness, index) => (
                            <li key={index} className="text-sm text-gray-300">{weakness}</li>
                          ))}
                        </ul>
                      </div>
                    </div>

                    <div className="mt-6">
                      <h4 className="text-md font-medium text-white mb-2">Recommendations</h4>
                      <div className="bg-gray-800 rounded-lg p-4">
                        <ul className="space-y-2">
                          {analysis.recommendations.map((recommendation, index) => (
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

export default RepositoryAnalysis; 