import React, { useState } from 'react';
import axios from 'axios';
import { FaUser, FaSpinner, FaChartBar } from 'react-icons/fa';
import { motion } from 'framer-motion';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts';

const API_URL = 'http://localhost:5000';

const IndividualPrediction = () => {
  const [formData, setFormData] = useState({
    name: '',
    usn: '',
    gender: 'MALE',
    age: 21,
    cgpa: 7.5,
    branch: 'CSE',
    backlogs: 0,
    internships: 1,
    internship_type: 'Corporate',
    research_papers: 0,
    projects: 2,
    certifications: 3,
    technical_skills: 3,
    hackathons: 0,
    soft_skills: 3,
    cocurricular_activities: 'Yes',
    leadership_roles: 'No',
    entrepreneur_cell: 'No',
    family_business: 'No'
  });

  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const branches = [
    'CSE', 'ISE', 'AIML', 'CSDS', 'CSD', 'CSBS', 'CSCY', 'CS IOT',
    'ECE', 'MECHANICAL', 'CIVIL', 'EEE', 'CHEMICAL', 'AUTOMOBILE',
    'AERONAUTICAL', 'AI and ROBOTICS', 'EIE', 'ETE', 'Medical Electronics',
    'Bio Technology', 'Other'
  ];

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setResult(null);

    try {
      const response = await axios.post(`${API_URL}/predict/individual`, formData);
      setResult(response.data);
    } catch (err) {
      setError(err.response?.data?.error || 'An error occurred during prediction');
    } finally {
      setLoading(false);
    }
  };

  const COLORS = ['#0ea5e9', '#10b981', '#f59e0b'];

  const getPathColor = (path) => {
    if (path === 'Higher Studies') return 'from-blue-500 to-cyan-600';
    if (path === 'Placement') return 'from-green-500 to-emerald-600';
    if (path === 'Startup') return 'from-orange-500 to-red-600';
    return 'from-gray-500 to-gray-600';
  };

  const getPathIcon = (path) => {
    if (path === 'Higher Studies') return '🎓';
    if (path === 'Placement') return '💼';
    if (path === 'Startup') return '🚀';
    return '📊';
  };

  return (
    <div className="max-w-7xl mx-auto px-4 py-8">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
      >
        <h1 className="text-4xl font-bold mb-2 gradient-text">Individual Career Path Prediction</h1>
        <p className="text-gray-600 mb-8">Enter your details to get personalized career path recommendation</p>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Form Section */}
          <div className="glass-card p-8">
            <h2 className="text-2xl font-bold mb-6 text-gray-800 flex items-center">
              <FaUser className="mr-3 text-primary-600" />
              Student Information
            </h2>

            <form onSubmit={handleSubmit} className="space-y-5">
              {/* Basic Info */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Name <span className="text-red-500">*</span>
                  </label>
                  <input
                    type="text"
                    name="name"
                    value={formData.name}
                    onChange={handleChange}
                    className="input-field"
                    required
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    USN <span className="text-red-500">*</span>
                  </label>
                  <input
                    type="text"
                    name="usn"
                    value={formData.usn}
                    onChange={handleChange}
                    className="input-field"
                    required
                  />
                </div>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Gender <span className="text-red-500">*</span>
                  </label>
                  <select
                    name="gender"
                    value={formData.gender}
                    onChange={handleChange}
                    className="input-field"
                    required
                  >
                    <option value="MALE">Male</option>
                    <option value="FEMALE">Female</option>
                  </select>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Age <span className="text-red-500">*</span>
                  </label>
                  <input
                    type="number"
                    name="age"
                    value={formData.age}
                    onChange={handleChange}
                    min="17"
                    max="30"
                    className="input-field"
                    required
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    CGPA <span className="text-red-500">*</span>
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
                </div>
              </div>

              {/* Academic Info */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Branch/Department <span className="text-red-500">*</span>
                  </label>
                  <select
                    name="branch"
                    value={formData.branch}
                    onChange={handleChange}
                    className="input-field"
                    required
                  >
                    {branches.map(branch => (
                      <option key={branch} value={branch}>{branch}</option>
                    ))}
                  </select>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Number of Backlogs <span className="text-red-500">*</span>
                  </label>
                  <input
                    type="number"
                    name="backlogs"
                    value={formData.backlogs}
                    onChange={handleChange}
                    min="0"
                    className="input-field"
                    required
                  />
                </div>
              </div>

              {/* Experience */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Number of Internships <span className="text-red-500">*</span>
                  </label>
                  <input
                    type="number"
                    name="internships"
                    value={formData.internships}
                    onChange={handleChange}
                    min="0"
                    className="input-field"
                    required
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Type of Internships <span className="text-red-500">*</span>
                  </label>
                  <select
                    name="internship_type"
                    value={formData.internship_type}
                    onChange={handleChange}
                    className="input-field"
                    required
                  >
                    <option value="Research">Research</option>
                    <option value="Corporate">Corporate</option>
                    <option value="Startup">Startup</option>
                    <option value="Other">Other</option>
                  </select>
                </div>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Research Papers <span className="text-red-500">*</span>
                  </label>
                  <input
                    type="number"
                    name="research_papers"
                    value={formData.research_papers}
                    onChange={handleChange}
                    min="0"
                    className="input-field"
                    required
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Number of Projects <span className="text-red-500">*</span>
                  </label>
                  <input
                    type="number"
                    name="projects"
                    value={formData.projects}
                    onChange={handleChange}
                    min="0"
                    className="input-field"
                    required
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Certifications <span className="text-red-500">*</span>
                  </label>
                  <input
                    type="number"
                    name="certifications"
                    value={formData.certifications}
                    onChange={handleChange}
                    min="0"
                    className="input-field"
                    required
                  />
                </div>
              </div>

              {/* Skills */}
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Technical Skills (1-5) <span className="text-red-500">*</span>
                  </label>
                  <select
                    name="technical_skills"
                    value={formData.technical_skills}
                    onChange={handleChange}
                    className="input-field"
                    required
                  >
                    {[1, 2, 3, 4, 5].map(val => (
                      <option key={val} value={val}>{val} - {val === 1 ? 'Poor' : val === 5 ? 'Excellent' : ''}</option>
                    ))}
                  </select>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Soft Skills (1-5) <span className="text-red-500">*</span>
                  </label>
                  <select
                    name="soft_skills"
                    value={formData.soft_skills}
                    onChange={handleChange}
                    className="input-field"
                    required
                  >
                    {[1, 2, 3, 4, 5].map(val => (
                      <option key={val} value={val}>{val} - {val === 1 ? 'Poor' : val === 5 ? 'Excellent' : ''}</option>
                    ))}
                  </select>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Hackathons Participated <span className="text-red-500">*</span>
                  </label>
                  <input
                    type="number"
                    name="hackathons"
                    value={formData.hackathons}
                    onChange={handleChange}
                    min="0"
                    className="input-field"
                    required
                  />
                </div>
              </div>

              {/* Activities */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Co-curricular Activities <span className="text-red-500">*</span>
                  </label>
                  <select
                    name="cocurricular_activities"
                    value={formData.cocurricular_activities}
                    onChange={handleChange}
                    className="input-field"
                    required
                  >
                    <option value="Yes">Yes</option>
                    <option value="No">No</option>
                  </select>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Leadership Roles <span className="text-red-500">*</span>
                  </label>
                  <select
                    name="leadership_roles"
                    value={formData.leadership_roles}
                    onChange={handleChange}
                    className="input-field"
                    required
                  >
                    <option value="Yes">Yes</option>
                    <option value="No">No</option>
                  </select>
                </div>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Entrepreneur Cell Member <span className="text-red-500">*</span>
                  </label>
                  <select
                    name="entrepreneur_cell"
                    value={formData.entrepreneur_cell}
                    onChange={handleChange}
                    className="input-field"
                    required
                  >
                    <option value="Yes">Yes</option>
                    <option value="No">No</option>
                  </select>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Family Business Background <span className="text-red-500">*</span>
                  </label>
                  <select
                    name="family_business"
                    value={formData.family_business}
                    onChange={handleChange}
                    className="input-field"
                    required
                  >
                    <option value="Yes">Yes</option>
                    <option value="No">No</option>
                  </select>
                </div>
              </div>

              {error && (
                <div className="bg-red-50 border-l-4 border-red-500 p-4 rounded">
                  <p className="text-red-700">{error}</p>
                </div>
              )}

              <button
                type="submit"
                disabled={loading}
                className="w-full btn-primary py-4"
              >
                {loading ? (
                  <span className="flex items-center justify-center">
                    <FaSpinner className="animate-spin mr-2" />
                    Predicting...
                  </span>
                ) : (
                  <span className="flex items-center justify-center">
                    <FaChartBar className="mr-2" />
                    Get Career Prediction
                  </span>
                )}
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
                className="space-y-6"
              >
                {/* Main Prediction */}
                <div className={`glass-card p-8 text-center bg-gradient-to-br ${getPathColor(result.prediction)}`}>
                  <div className="text-7xl mb-4">{getPathIcon(result.prediction)}</div>
                  <h3 className="text-white text-2xl font-semibold mb-2">Predicted Career Path</h3>
                  <div className="text-5xl font-bold text-white mb-3">
                    {result.prediction}
                  </div>
                  <div className="text-white text-lg">
                    Confidence: {(result.confidence * 100).toFixed(1)}%
                  </div>
                </div>

                {/* Probabilities */}
                <div className="glass-card p-6">
                  <h3 className="text-xl font-bold mb-4 text-gray-800">📊 Career Path Probabilities</h3>
                  <div className="space-y-3">
                    {Object.entries(result.probabilities).map(([path, prob]) => (
                      <div key={path}>
                        <div className="flex justify-between mb-1">
                          <span className="font-medium text-gray-700 flex items-center">
                            <span className="mr-2">{getPathIcon(path)}</span>
                            {path}
                          </span>
                          <span className="font-bold text-gray-800">
                            {(prob * 100).toFixed(1)}%
                          </span>
                        </div>
                        <div className="w-full bg-gray-200 rounded-full h-3">
                          <div
                            className={`h-3 rounded-full bg-gradient-to-r ${getPathColor(path)} transition-all duration-500`}
                            style={{ width: `${prob * 100}%` }}
                          ></div>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>

                {/* Pie Chart */}
                <div className="glass-card p-6">
                  <h3 className="text-xl font-bold mb-4 text-gray-800 text-center">Distribution</h3>
                  <ResponsiveContainer width="100%" height={280}>
                    <PieChart>
                      <Pie
                        data={Object.entries(result.probabilities).map(([name, value]) => ({
                          name,
                          value: value * 100
                        }))}
                        cx="50%"
                        cy="50%"
                        labelLine={false}
                        label={(entry) => `${entry.name}: ${entry.value.toFixed(1)}%`}
                        outerRadius={90}
                        fill="#8884d8"
                        dataKey="value"
                      >
                        {COLORS.map((color, index) => (
                          <Cell key={`cell-${index}`} fill={color} />
                        ))}
                      </Pie>
                      <Tooltip formatter={(value) => `${value.toFixed(1)}%`} />
                      <Legend />
                    </PieChart>
                  </ResponsiveContainer>
                </div>

                {/* Feature Importance */}
                {result.feature_importance && (
                  <div className="glass-card p-6">
                    <h3 className="text-xl font-bold mb-4 text-gray-800">🎯 Top Influential Factors</h3>
                    <ResponsiveContainer width="100%" height={300}>
                      <BarChart data={result.feature_importance.slice(0, 5)} layout="vertical">
                        <CartesianGrid strokeDasharray="3 3" />
                        <XAxis type="number" />
                        <YAxis dataKey="feature" type="category" width={120} />
                        <Tooltip />
                        <Legend />
                        <Bar dataKey="importance" fill="#0ea5e9" name="Importance" />
                      </BarChart>
                    </ResponsiveContainer>
                  </div>
                )}

                {/* Recommendations */}
                <div className="glass-card p-6">
                  <h3 className="text-xl font-bold mb-3 text-gray-800">💡 Recommendations</h3>
                  {result.prediction === 'Higher Studies' && (
                    <div className="space-y-2 text-gray-700">
                      <p>✓ Focus on research publications and academic projects</p>
                      <p>✓ Maintain high CGPA and develop analytical skills</p>
                      <p>✓ Connect with professors and research mentors</p>
                      <p>✓ Prepare for GRE/GATE examinations</p>
                    </div>
                  )}
                  {result.prediction === 'Placement' && (
                    <div className="space-y-2 text-gray-700">
                      <p>✓ Strengthen technical and communication skills</p>
                      <p>✓ Gain more internship experience</p>
                      <p>✓ Build a strong portfolio of projects</p>
                      <p>✓ Practice coding and aptitude tests</p>
                    </div>
                  )}
                  {result.prediction === 'Startup' && (
                    <div className="space-y-2 text-gray-700">
                      <p>✓ Develop leadership and business skills</p>
                      <p>✓ Network with entrepreneurs and mentors</p>
                      <p>✓ Work on innovative projects and ideas</p>
                      <p>✓ Learn about market analysis and business planning</p>
                    </div>
                  )}
                </div>
              </motion.div>
            ) : (
              <div className="glass-card p-12 text-center">
                <FaUser className="text-6xl text-gray-300 mx-auto mb-4" />
                <p className="text-gray-500 text-lg">Fill in the form and submit to get your career path prediction</p>
              </div>
            )}
          </div>
        </div>
      </motion.div>
    </div>
  );
};

export default IndividualPrediction;
