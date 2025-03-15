import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import LandingPage from './pages/LandingPage';
import Login from './pages/Login';
import Signup from './pages/Signup';
import Dashboard from './pages/Dashboard';
import RepositoryAnalysis from './pages/RepositoryAnalysis';
import ProfileScoring from './pages/ProfileScoring';
import './App.css';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<LandingPage />} />
        <Route path="/login" element={<Login />} />
        <Route path="/signup" element={<Signup />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/repository-analysis" element={<RepositoryAnalysis />} />
        <Route path="/profile-scoring" element={<ProfileScoring />} />
      </Routes>
    </Router>
  );
}

export default App;
