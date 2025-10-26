import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar';
import Home from './pages/Home';
import BatchPrediction from './pages/BatchPrediction';
import IndividualPrediction from './pages/IndividualPrediction';
import APICalculator from './pages/APICalculator';

function App() {
  return (
    <Router>
      <div className="min-h-screen">
        <Navbar />
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/batch" element={<BatchPrediction />} />
          <Route path="/individual" element={<IndividualPrediction />} />
          <Route path="/api-calculator" element={<APICalculator />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
