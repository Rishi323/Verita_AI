import React from 'react';
import { BrowserRouter as Router, Route, Routes, Navigate } from 'react-router-dom';
import Dashboard from './dashboard/Dashboard';
import { CreateStudy } from "./components/research/create-study";

function App() {
  return (
    <Router>
      <Routes>
        {/* Redirect root to dashboard */}
        <Route path="/" element={<Navigate to="/dashboard" replace />} />
        
        {/* Dashboard route */}
        <Route path="/dashboard" element={<Dashboard />} />
        
        {/* CreateStudy route */}
        <Route path="/create-study" element={<CreateStudy onClose={() => {}} />} />
        
        {/* Catch-all route for 404 - Not Found */}
        <Route path="*" element={<div>404 - Not Found</div>} />
      </Routes>
    </Router>
  );
}

export default App;