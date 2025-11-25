import React, { useState } from 'react';
import axios from 'axios';
import { FaUser, FaSpinner, FaChartBar, FaDownload, FaRobot, FaComments } from 'react-icons/fa';
import { motion } from 'framer-motion';

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

  // Chatbot State
  const [chatInput, setChatInput] = useState('');
  const [chatHistory, setChatHistory] = useState([]);
  const [chatLoading, setChatLoading] = useState(false);

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

  const handleDownloadRoadmap = () => {
    if (!result || !result.roadmap) return;

    const element = document.createElement("a");
    const file = new Blob([result.roadmap], { type: 'text/markdown' });
    element.href = URL.createObjectURL(file);
    element.download = `${formData.name}_Career_Roadmap.md`;
    document.body.appendChild(element);
    element.click();
    document.body.removeChild(element);
  };

  const handleChatSubmit = async (e) => {
    e.preventDefault();
    if (!chatInput.trim()) return;

    const userMessage = chatInput;
    setChatInput('');
    setChatHistory(prev => [...prev, { role: 'user', content: userMessage }]);
    setChatLoading(true);

    try {
      const response = await axios.post(`${API_URL}/chat`, {
        message: userMessage,
        history: chatHistory,
        context: {
          profile_name: result.profile_name,
          roles: result.suggested_roles.join(', '),
          technical_score: formData.technical_skills
        }
      });

      setChatHistory(prev => [...prev, { role: 'ai', content: response.data.response }]);
    } catch (err) {
      setChatHistory(prev => [...prev, { role: 'ai', content: "Sorry, I encountered an error. Please try again." }]);
    } finally {
      setChatLoading(false);
    }
  };

  return (
    <div className="max-w-7xl mx-auto px-4 py-8">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
      >
        <h1 className="text-4xl font-bold mb-2 gradient-text">AI Career Path Predictor</h1>
        <p className="text-gray-600 mb-8">Get your personalized career profile and roadmap powered by Career Path AI</p>

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
                    Analyzing Profile...
                  </span>
                ) : (
                  <span className="flex items-center justify-center">
                    <FaChartBar className="mr-2" />
                    Generate Career Roadmap
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
                <div className="glass-card p-8 text-center bg-gradient-to-br from-indigo-600 to-purple-700">
                  <div className="text-7xl mb-4">🚀</div>
                  <h3 className="text-white text-2xl font-semibold mb-2">Your Career Profile</h3>
                  <div className="text-4xl font-bold text-white mb-3">
                    {result.profile_name}
                  </div>
                  <p className="text-indigo-100 text-lg italic">
                    "{result.description}"
                  </p>
                </div>

                {/* Suggested Roles */}
                <div className="glass-card p-6">
                  <h3 className="text-xl font-bold mb-4 text-gray-800">🎯 Suggested Roles</h3>
                  <div className="flex flex-wrap gap-2">
                    {result.suggested_roles && result.suggested_roles.map((role, index) => (
                      <span key={index} className="px-4 py-2 bg-indigo-100 text-indigo-800 rounded-full font-medium">
                        {role}
                      </span>
                    ))}
                  </div>
                </div>

                {/* Roadmap */}
                <div className="glass-card p-6">
                  <div className="flex justify-between items-center mb-4">
                    <h3 className="text-xl font-bold text-gray-800 flex items-center">
                      <FaRobot className="mr-2 text-indigo-600" />
                      AI Generated Roadmap
                    </h3>
                    <button
                      onClick={handleDownloadRoadmap}
                      className="flex items-center text-sm bg-green-600 text-white px-3 py-1.5 rounded hover:bg-green-700 transition"
                    >
                      <FaDownload className="mr-1" /> Download
                    </button>
                  </div>

                  <div className="bg-gray-50 p-4 rounded-lg border border-gray-200 max-h-[500px] overflow-y-auto">
                    <pre className="whitespace-pre-wrap font-sans text-gray-700 text-sm leading-relaxed">
                      {result.roadmap}
                    </pre>
                  </div>
                </div>

                {/* Chatbot Interface */}
                <div className="glass-card p-6 bg-gradient-to-b from-white to-indigo-50">
                  <h3 className="text-xl font-bold mb-4 text-gray-800 flex items-center">
                    <FaComments className="mr-2 text-indigo-600" />
                    Chat with Career AI
                  </h3>

                  <div className="bg-white border border-gray-200 rounded-lg h-[300px] overflow-y-auto p-4 mb-4 space-y-3">
                    {chatHistory.map((msg, idx) => (
                      <div key={idx} className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
                        <div className={`max-w-[80%] p-3 rounded-lg ${msg.role === 'user'
                          ? 'bg-indigo-600 text-white rounded-br-none'
                          : 'bg-gray-100 text-gray-800 rounded-bl-none'
                          }`}>
                          <p className="text-sm">{msg.content}</p>
                        </div>
                      </div>
                    ))}
                    {chatLoading && (
                      <div className="flex justify-start">
                        <div className="bg-gray-100 p-3 rounded-lg rounded-bl-none">
                          <FaSpinner className="animate-spin text-indigo-600" />
                        </div>
                      </div>
                    )}
                  </div>

                  <form onSubmit={handleChatSubmit} className="flex gap-2">
                    <input
                      type="text"
                      value={chatInput}
                      onChange={(e) => setChatInput(e.target.value)}
                      placeholder="Ask about your career path..."
                      className="flex-1 input-field"
                      disabled={chatLoading}
                    />
                    <button
                      type="submit"
                      disabled={!chatInput.trim() || chatLoading}
                      className="bg-indigo-600 text-white px-6 py-2 rounded-lg hover:bg-indigo-700 disabled:bg-gray-400 transition"
                    >
                      Send
                    </button>
                  </form>
                </div>

              </motion.div>
            ) : (
              <div className="glass-card p-12 text-center">
                <FaUser className="text-6xl text-gray-300 mx-auto mb-4" />
                <p className="text-gray-500 text-lg">Fill in the form and submit to get your personalized career roadmap</p>
              </div>
            )}
          </div>
        </div>
      </motion.div>
    </div>
  );
};

export default IndividualPrediction;
