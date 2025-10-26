import React from 'react';
import { Link } from 'react-router-dom';
import { FaUsers, FaUser, FaCalculator, FaChartLine, FaBrain, FaRocket } from 'react-icons/fa';
import { motion } from 'framer-motion';

const Home = () => {
  const features = [
    {
      icon: <FaUsers className="text-5xl" />,
      title: 'Batch Prediction',
      description: 'Upload Excel file with student data and get career path predictions for entire batch',
      link: '/batch',
      color: 'from-blue-500 to-cyan-500'
    },
    {
      icon: <FaUser className="text-5xl" />,
      title: 'Individual Prediction',
      description: 'Get personalized career path prediction based on individual student profile',
      link: '/individual',
      color: 'from-purple-500 to-pink-500'
    },
    {
      icon: <FaCalculator className="text-5xl" />,
      title: 'API Score Calculator',
      description: 'Calculate Academic Performance Index based on CGPA, internships, courses, and certifications',
      link: '/api-calculator',
      color: 'from-green-500 to-teal-500'
    }
  ];

  const stats = [
    { icon: <FaBrain />, value: 'ML Powered', label: 'Machine Learning Model' },
    { icon: <FaChartLine />, value: '3 Paths', label: 'Career Predictions' },
    { icon: <FaRocket />, value: 'Real-time', label: 'Instant Results' }
  ];

  return (
    <div className="max-w-7xl mx-auto px-4 py-8">
      {/* Hero Section */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6 }}
        className="text-center mb-16"
      >
        <h1 className="text-6xl font-bold mb-4">
          <span className="gradient-text">Career Path Prediction</span>
        </h1>
        <p className="text-xl text-gray-600 mb-8">
          AI-powered career guidance for engineering students
        </p>
        <div className="flex justify-center gap-4">
          <Link to="/batch" className="btn-primary">
            Get Started
          </Link>
          <a href="#features" className="btn-secondary">
            Learn More
          </a>
        </div>
      </motion.div>

      {/* Stats Section */}
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.3, duration: 0.6 }}
        className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-16"
      >
        {stats.map((stat, index) => (
          <div key={index} className="glass-card p-6 text-center card-hover">
            <div className="text-4xl text-primary-600 mb-2 flex justify-center">
              {stat.icon}
            </div>
            <div className="text-2xl font-bold text-gray-800">{stat.value}</div>
            <div className="text-gray-600">{stat.label}</div>
          </div>
        ))}
      </motion.div>

      {/* Features Section */}
      <div id="features" className="mb-16">
        <h2 className="text-4xl font-bold text-center mb-12 gradient-text">
          Our Features
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {features.map((feature, index) => (
            <motion.div
              key={index}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.4 + index * 0.1, duration: 0.5 }}
            >
              <Link to={feature.link}>
                <div className="glass-card p-8 h-full card-hover">
                  <div className={`bg-gradient-to-r ${feature.color} text-white w-20 h-20 rounded-2xl flex items-center justify-center mb-6`}>
                    {feature.icon}
                  </div>
                  <h3 className="text-2xl font-bold mb-4 text-gray-800">
                    {feature.title}
                  </h3>
                  <p className="text-gray-600 leading-relaxed">
                    {feature.description}
                  </p>
                </div>
              </Link>
            </motion.div>
          ))}
        </div>
      </div>

      {/* Career Paths Section */}
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.8, duration: 0.6 }}
        className="glass-card p-8 mb-8"
      >
        <h2 className="text-3xl font-bold mb-6 gradient-text text-center">
          Career Path Options
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="bg-gradient-to-br from-blue-50 to-blue-100 p-6 rounded-xl">
            <h3 className="text-xl font-bold text-blue-800 mb-3">Higher Studies</h3>
            <p className="text-gray-700">
              Master's, PhD programs for students with strong research interests and academic excellence
            </p>
          </div>
          <div className="bg-gradient-to-br from-green-50 to-green-100 p-6 rounded-xl">
            <h3 className="text-xl font-bold text-green-800 mb-3">Placement</h3>
            <p className="text-gray-700">
              Corporate jobs for students with strong technical and communication skills
            </p>
          </div>
          <div className="bg-gradient-to-br from-purple-50 to-purple-100 p-6 rounded-xl">
            <h3 className="text-xl font-bold text-purple-800 mb-3">Startup</h3>
            <p className="text-gray-700">
              Entrepreneurship path for students with business acumen and leadership qualities
            </p>
          </div>
        </div>
      </motion.div>
    </div>
  );
};

export default Home;
