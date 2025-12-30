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
    { icon: <FaChartLine />, value: '5 Paths', label: 'Career Predictions' },
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
          Career Path Profiles
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {[
            {
              title: "Technical Innovators",
              desc: "Core software developers and architects who excel in transforming abstract ideas into functional systems. They stand out by their reliability in coding complex algorithms and building scalable products, focusing on application utility rather than just theory.",
              color: "bg-gradient-to-br from-blue-50 to-blue-100 text-blue-800"
            },
            {
              title: "Research & Data Learners",
              desc: "Future data scientists and analysts driven by curiosity and patterns. Their uniqueness lies in a strong theoretical foundation and mathematical rigor, prioritizing accuracy and deep understanding of data over immediate software deployment.",
              color: "bg-gradient-to-br from-green-50 to-green-100 text-green-800"
            },
            {
              title: "Career Growth Learners",
              desc: "High-potential talent defined by their adaptability and rapid learning velocity. Unlike specialists with static skills, they thrive in changing environments, constantly upskilling and bridging gaps between different technical domains.",
              color: "bg-gradient-to-br from-purple-50 to-purple-100 text-purple-800"
            },
            {
              title: "Technical Specialist",
              desc: "Experts in critical infrastructure, security, and utilization. They differ by focusing on the 'how' and 'where' applications run—ensuring robustness, security, and uptime—rather than just the feature development itself.",
              color: "bg-gradient-to-br from-orange-50 to-orange-100 text-orange-800"
            },
            {
              title: "Research Innovator",
              desc: "The bridge between cutting-edge theory and practical application (e.g., R&D, AI Engineers). They possess the rare ability to not only understand complex research but also operationalize it into tangible innovations, unlike pure researchers or pure devs.",
              color: "bg-gradient-to-br from-pink-50 to-pink-100 text-pink-800"
            }
          ].map((path, index) => (
            <div key={index} className={`${path.color} p-6 rounded-xl hover:shadow-md transition-shadow`}>
              <h3 className="text-xl font-bold mb-3">{path.title}</h3>
              <p className="text-gray-700 text-sm">
                {path.desc}
              </p>
            </div>
          ))}
        </div>
      </motion.div>
    </div>
  );
};

export default Home;
