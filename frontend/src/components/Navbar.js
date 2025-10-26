import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { FaGraduationCap, FaUsers, FaUser, FaCalculator } from 'react-icons/fa';

const Navbar = () => {
  const location = useLocation();
  
  const navItems = [
    { path: '/', label: 'Home', icon: <FaGraduationCap /> },
    { path: '/batch', label: 'Batch Prediction', icon: <FaUsers /> },
    { path: '/individual', label: 'Individual Prediction', icon: <FaUser /> },
    { path: '/api-calculator', label: 'API Calculator', icon: <FaCalculator /> },
  ];

  return (
    <nav className="glass-card m-4 p-4">
      <div className="max-w-7xl mx-auto flex items-center justify-between">
        <Link to="/" className="flex items-center space-x-2">
          <FaGraduationCap className="text-3xl text-primary-600" />
          <span className="text-2xl font-bold gradient-text">Career Path Prediction</span>
        </Link>
        
        <div className="flex space-x-2">
          {navItems.map((item) => {
            const isActive = location.pathname === item.path;
            return (
              <Link
                key={item.path}
                to={item.path}
                className={`flex items-center space-x-2 px-4 py-2 rounded-lg transition-all duration-200 ${
                  isActive
                    ? 'bg-gradient-to-r from-primary-600 to-primary-700 text-white shadow-lg'
                    : 'hover:bg-primary-50 text-gray-700'
                }`}
              >
                <span className="text-lg">{item.icon}</span>
                <span className="font-medium">{item.label}</span>
              </Link>
            );
          })}
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
