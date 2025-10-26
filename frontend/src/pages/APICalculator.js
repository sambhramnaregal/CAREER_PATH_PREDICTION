import React, { useState } from 'react';
import axios from 'axios';
import { FaCalculator, FaGraduationCap, FaBriefcase, FaBook, FaCertificate } from 'react-icons/fa';
import { motion } from 'framer-motion';
import { PieChart, Pie, Cell, ResponsiveContainer, Legend, Tooltip } from 'recharts';

const API_URL = 'http://localhost:5000';

const APICalculator = () => {
  const [formData, setFormData] = useState({
    cgpa: 7.5,
    paid_internships: 1,
    unpaid_internships: 0,
    research_papers: 2,
    certificates: 5
  });

  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: parseFloat(value) || 0
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      const response = await axios.post(`${API_URL}/calculate/api`, formData);
      setResult(response.data);
    } catch (error) {
      console.error('Error calculating API:', error);
    } finally {
      setLoading(false);
    }
  };

  const getScoreColor = (level) => {
    const colors = {
      excellent: 'from-green-500 to-emerald-600',
      good: 'from-blue-500 to-cyan-600',
      fair: 'from-yellow-500 to-orange-600',
      needs_improvement: 'from-red-500 to-pink-600'
    };
    return colors[level] || colors.fair;
  };

  const COLORS = ['#0ea5e9', '#10b981', '#a855f7', '#f59e0b'];

  return (
    <div className="max-w-6xl mx-auto px-4 py-8">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
      >
        <h1 className="text-4xl font-bold mb-2 gradient-text">API Score Calculator</h1>
        <p className="text-gray-600 mb-8">Calculate your Academic Performance Index based on various parameters</p>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Form Section */}
          <div className="glass-card p-8">
            <h2 className="text-2xl font-bold mb-6 text-gray-800 flex items-center">
              <FaCalculator className="mr-3 text-primary-600" />
              Enter Your Details
            </h2>

            <form onSubmit={handleSubmit} className="space-y-6">
              {/* CGPA */}
              <div>
                <label className="flex items-center text-gray-700 font-medium mb-2">
                  <FaGraduationCap className="mr-2 text-primary-600" />
                  CGPA (out of 10)
                </label>
                <input
                  type="number"
                  name="cgpa"
                  value={formData.cgpa}
                  onChange={handleChange}
                  min="0"
                  max="10"
                  step="0.01"
                  className="input-field"
                  required
                />
                <p className="text-xs text-gray-500 mt-1">Weight: 20% (Max 2 points)</p>
              </div>

              {/* Internships */}
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="flex items-center text-gray-700 font-medium mb-2">
                    <FaBriefcase className="mr-2 text-green-600" />
                    Paid Internships
                  </label>
                  <input
                    type="number"
                    name="paid_internships"
                    value={formData.paid_internships}
                    onChange={handleChange}
                    min="0"
                    max="5"
                    className="input-field"
                    required
                  />
                  <p className="text-xs text-gray-500 mt-1">2 points each</p>
                </div>
                <div>
                  <label className="flex items-center text-gray-700 font-medium mb-2">
                    <FaBriefcase className="mr-2 text-blue-600" />
                    Unpaid Internships
                  </label>
                  <input
                    type="number"
                    name="unpaid_internships"
                    value={formData.unpaid_internships}
                    onChange={handleChange}
                    min="0"
                    max="5"
                    className="input-field"
                    required
                  />
                  <p className="text-xs text-gray-500 mt-1">1 point each</p>
                </div>
              </div>
              <p className="text-xs text-blue-600 font-medium">Total weight: 40% (Maximum 4 points)</p>

              {/* Research Work */}
              <div>
                <label className="flex items-center text-gray-700 font-medium mb-2">
                  <FaBook className="mr-2 text-purple-600" />
                  Research Papers / Publications
                </label>
                <input
                  type="number"
                  name="research_papers"
                  value={formData.research_papers}
                  onChange={handleChange}
                  min="0"
                  max="10"
                  className="input-field"
                  required
                />
                <p className="text-xs text-gray-500 mt-1">0.5 points each</p>
                <p className="text-xs text-blue-600 font-medium mt-1">Total weight: 20% (Maximum 2 points)</p>
              </div>

              {/* Certificates */}
              <div>
                <label className="flex items-center text-gray-700 font-medium mb-2">
                  <FaCertificate className="mr-2 text-orange-600" />
                  Certifications Completed
                </label>
                <input
                  type="number"
                  name="certificates"
                  value={formData.certificates}
                  onChange={handleChange}
                  min="0"
                  max="20"
                  className="input-field"
                  required
                />
                <p className="text-xs text-gray-500 mt-1">0.1 points each</p>
                <p className="text-xs text-blue-600 font-medium mt-1">Total weight: 20% (Maximum 2 points)</p>
              </div>

              <button
                type="submit"
                disabled={loading}
                className="w-full btn-primary"
              >
                {loading ? 'Calculating...' : 'Calculate API Score'}
              </button>
            </form>
          </div>

          {/* Results Section */}
          <div className="space-y-6">
            {result ? (
              <motion.div
                initial={{ opacity: 0, scale: 0.9 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ duration: 0.5 }}
              >
                {/* Score Display */}
                <div className={`glass-card p-8 text-center bg-gradient-to-br ${getScoreColor(result.level)}`}>
                  <h3 className="text-white text-xl font-semibold mb-2">Your API Score</h3>
                  <div className="text-6xl font-bold text-white mb-2">
                    {result.total_score}
                  </div>
                  <div className="text-white text-lg">out of {result.max_score}</div>
                </div>

                {/* Feedback */}
                <div className="glass-card p-6">
                  <h3 className="text-xl font-bold mb-3 text-gray-800">📊 Analysis</h3>
                  <p className="text-gray-700 leading-relaxed">{result.feedback}</p>
                </div>

                {/* Breakdown */}
                <div className="glass-card p-6">
                  <h3 className="text-xl font-bold mb-4 text-gray-800">Score Breakdown</h3>
                  <div className="space-y-3">
                    {Object.entries(result.breakdown).map(([key, value]) => {
                      const labels = {
                        cgpa_points: { name: 'CGPA (20%)', max: 2, color: 'bg-blue-500', desc: 'Academic performance' },
                        internship_points: { name: 'Internships (40%)', max: 4, color: 'bg-green-500', desc: 'Work experience' },
                        research_points: { name: 'Research Work (20%)', max: 2, color: 'bg-purple-500', desc: 'Publications & papers' },
                        cert_points: { name: 'Certifications (20%)', max: 2, color: 'bg-orange-500', desc: 'Skills & courses' }
                      };
                      const label = labels[key];
                      if (!label) return null;
                      const percentage = (value / label.max) * 100;

                      return (
                        <div key={key}>
                          <div className="flex justify-between mb-1">
                            <div>
                              <span className="text-sm font-bold text-gray-800">{label.name}</span>
                              <span className="text-xs text-gray-500 block">{label.desc}</span>
                            </div>
                            <span className="text-lg font-bold text-primary-600">
                              {value} / {label.max}
                            </span>
                          </div>
                          <div className="w-full bg-gray-200 rounded-full h-4">
                            <div
                              className={`h-4 rounded-full ${label.color} transition-all duration-500 flex items-center justify-end pr-2`}
                              style={{ width: `${percentage}%` }}
                            >
                              {percentage > 20 && <span className="text-xs text-white font-semibold">{Math.round(percentage)}%</span>}
                            </div>
                          </div>
                        </div>
                      );
                    })}
                  </div>
                </div>

                {/* Pie Chart */}
                <div className="glass-card p-6">
                  <h3 className="text-xl font-bold mb-4 text-gray-800 text-center">Score Distribution</h3>
                  <ResponsiveContainer width="100%" height={250}>
                    <PieChart>
                      <Pie
                        data={[
                          { name: 'CGPA (20%)', value: result.breakdown.cgpa_points, max: 2 },
                          { name: 'Internships (40%)', value: result.breakdown.internship_points, max: 4 },
                          { name: 'Research (20%)', value: result.breakdown.research_points, max: 2 },
                          { name: 'Certifications (20%)', value: result.breakdown.cert_points, max: 2 }
                        ]}
                        cx="50%"
                        cy="50%"
                        labelLine={false}
                        label={(entry) => `${entry.name}: ${entry.value}`}
                        outerRadius={80}
                        fill="#8884d8"
                        dataKey="value"
                      >
                        {COLORS.map((color, index) => (
                          <Cell key={`cell-${index}`} fill={color} />
                        ))}
                      </Pie>
                      <Tooltip />
                      <Legend />
                    </PieChart>
                  </ResponsiveContainer>
                </div>
              </motion.div>
            ) : (
              <div className="glass-card p-12 text-center">
                <FaCalculator className="text-6xl text-gray-300 mx-auto mb-4" />
                <p className="text-gray-500 text-lg">Fill in the form and click Calculate to see your API Score</p>
              </div>
            )}
          </div>
        </div>
      </motion.div>
    </div>
  );
};

export default APICalculator;
