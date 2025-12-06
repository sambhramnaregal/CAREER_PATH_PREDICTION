import React, { useState } from 'react';
import axios from 'axios';
import { FaUpload, FaDownload, FaFileExcel, FaCheck, FaSpinner, FaExternalLinkAlt, FaWpforms, FaChartPie } from 'react-icons/fa';
import { motion } from 'framer-motion';
import { PieChart, Pie, Cell, Tooltip, Legend, ResponsiveContainer } from 'recharts';

const API_URL = 'http://localhost:5001';

const BatchPrediction = () => {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState(false);
  const [distribution, setDistribution] = useState(null);

  // Updated Google Form link
  const GOOGLE_FORM_LINK = 'https://forms.gle/waq4HvbME4HVH1Ew7';

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    if (selectedFile) {
      if (selectedFile.name.endsWith('.xlsx') || selectedFile.name.endsWith('.xls')) {
        setFile(selectedFile);
        setError('');
        setSuccess(false);
        setDistribution(null);
      } else {
        setError('Please upload an Excel file (.xlsx or .xls)');
        setFile(null);
      }
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!file) {
      setError('Please select a file first');
      return;
    }

    setLoading(true);
    setError('');
    setSuccess(false);
    setDistribution(null);

    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await axios.post(`${API_URL}/predict/batch`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      if (response.data.success) {
        // Handle file download from base64
        const link = document.createElement('a');
        link.href = `data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,${response.data.file_base64}`;
        link.download = response.data.filename;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);

        setDistribution(response.data.distribution);
        setSuccess(true);
        setFile(null);
      }
    } catch (err) {
      setError(err.response?.data?.error || 'An error occurred during prediction');
    } finally {
      setLoading(false);
    }
  };

  const COLORS = ['#0ea5e9', '#10b981', '#f59e0b', '#8b5cf6', '#ec4899', '#6366f1', '#14b8a6', '#f43f5e'];

  return (
    <div className="max-w-4xl mx-auto px-4 py-8">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
      >
        <h1 className="text-4xl font-bold mb-2 gradient-text">Batch Prediction</h1>
        <p className="text-gray-600 mb-8">Upload Excel file with student data for batch career path predictions</p>

        {/* Google Form Collection Card */}
        <div className="glass-card p-6 mb-8 bg-gradient-to-r from-blue-50 to-indigo-50 border-2 border-blue-200">
          <div className="flex items-start gap-4">
            <div className="bg-blue-500 p-4 rounded-full text-white">
              <FaWpforms className="text-3xl" />
            </div>
            <div className="flex-1">
              <h2 className="text-2xl font-bold mb-2 text-gray-800 flex items-center gap-2">
                📝 Collect Student Data via Google Form
              </h2>
              <p className="text-gray-700 mb-4">
                Share this form with your students to collect their information in the correct format.
                Once responses are submitted, download the Excel file from Google Forms and upload it here for batch predictions.
              </p>
              <a
                href={GOOGLE_FORM_LINK}
                target="_blank"
                rel="noopener noreferrer"
                className="inline-flex items-center gap-2 bg-blue-600 hover:bg-blue-700 text-white font-semibold px-6 py-3 rounded-lg shadow-lg hover:shadow-xl transition-all duration-200 transform hover:scale-105"
              >
                <FaWpforms />
                Open Google Form
                <FaExternalLinkAlt className="text-sm" />
              </a>
              <div className="mt-4 bg-white p-3 rounded-lg border border-blue-200">
                <p className="text-sm text-gray-600">
                  <strong>💡 Tip:</strong> After collecting responses, go to Google Forms → Responses tab →
                  Click the green Excel icon to download responses as .xlsx file
                </p>
              </div>
            </div>
          </div>
        </div>

        {/* Instructions Card */}
        <div className="glass-card p-6 mb-8">
          <h2 className="text-2xl font-bold mb-4 text-gray-800">📋 Excel File Format</h2>
          <div className="bg-blue-50 border-l-4 border-blue-500 p-4 mb-4">
            <p className="font-semibold text-blue-800 mb-2">Required Columns (must match exactly):</p>
            <div className="grid grid-cols-2 gap-2">
              <ul className="list-disc list-inside text-gray-700 space-y-1">
                <li>Name</li>
                <li>USN</li>
                <li>Gender</li>
                <li>Age</li>
                <li>CGPA (0-10)</li>
                <li>Branch_Department</li>
                <li>Number_of_Backlogs</li>
                <li>Number_of_Internships</li>
                <li>Type_of_Internships</li>
                <li>Number_of_Publications</li>
              </ul>
              <ul className="list-disc list-inside text-gray-700 space-y-1">
                <li>Number_of_Projects</li>
                <li>Number_of_Certification_Courses</li>
                <li>Technical_Skills_Score (1-5)</li>
                <li>Number_of_Hackathons</li>
                <li>Soft_Skills_Score (1-5)</li>
                <li>Co_curricular_Activities (Yes/No)</li>
                <li>Leadership_Roles (Yes/No)</li>
                <li>Entrepreneur_Cell_Member (Yes/No)</li>
                <li>Family_Business_Background (Yes/No)</li>
              </ul>
            </div>
          </div>
          <p className="text-sm text-gray-600">
            💡 The system will add <strong>Predicted_Profile</strong> and <strong>Suggested_Roles</strong> columns to your file
          </p>
          <p className="text-sm text-gray-600 mt-2">
            ⚠️ Do NOT include <strong>Status_after_Graduation</strong> column - this will be predicted!
          </p>
        </div>

        {/* Upload Form */}
        <div className="glass-card p-8">
          <form onSubmit={handleSubmit} className="space-y-6">
            <div className="border-2 border-dashed border-gray-300 rounded-lg p-8 text-center hover:border-primary-500 transition-colors duration-200">
              <FaFileExcel className="text-6xl text-green-500 mx-auto mb-4" />
              <label className="cursor-pointer">
                <input
                  type="file"
                  onChange={handleFileChange}
                  accept=".xlsx,.xls"
                  className="hidden"
                />
                <span className="btn-primary inline-block">
                  <FaUpload className="inline mr-2" />
                  Choose Excel File
                </span>
              </label>
              {file && (
                <div className="mt-4 flex items-center justify-center text-green-600">
                  <FaCheck className="mr-2" />
                  <span className="font-medium">{file.name}</span>
                </div>
              )}
            </div>

            {error && (
              <div className="bg-red-50 border-l-4 border-red-500 p-4 rounded">
                <p className="text-red-700">{error}</p>
              </div>
            )}

            {success && (
              <div className="bg-green-50 border-l-4 border-green-500 p-4 rounded">
                <div className="flex items-center">
                  <FaDownload className="text-green-500 mr-2" />
                  <p className="text-green-700 font-medium">
                    Predictions generated successfully! File downloaded.
                  </p>
                </div>
              </div>
            )}

            <button
              type="submit"
              disabled={!file || loading}
              className={`w-full py-4 rounded-lg font-semibold text-white transition-all duration-200 ${!file || loading
                ? 'bg-gray-400 cursor-not-allowed'
                : 'bg-gradient-to-r from-primary-600 to-primary-700 hover:from-primary-700 hover:to-primary-800 shadow-lg hover:shadow-xl'
                }`}
            >
              {loading ? (
                <span className="flex items-center justify-center">
                  <FaSpinner className="animate-spin mr-2" />
                  Processing...
                </span>
              ) : (
                <span className="flex items-center justify-center">
                  <FaDownload className="mr-2" />
                  Generate Predictions
                </span>
              )}
            </button>
          </form>
        </div>

        {/* Distribution Chart */}
        {distribution && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
            className="glass-card p-8 mt-8"
          >
            <h2 className="text-2xl font-bold mb-6 text-gray-800 flex items-center justify-center">
              <FaChartPie className="mr-3 text-primary-600" />
              Predicted Profile Distribution
            </h2>
            <div className="h-[400px] w-full">
              <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                  <Pie
                    data={Object.entries(distribution).map(([name, value]) => ({ name, value }))}
                    cx="50%"
                    cy="50%"
                    labelLine={true}
                    label={({ name, percent }) => `${name} (${(percent * 100).toFixed(0)}%)`}
                    outerRadius={150}
                    fill="#8884d8"
                    dataKey="value"
                  >
                    {Object.entries(distribution).map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                    ))}
                  </Pie>
                  <Tooltip />
                  <Legend />
                </PieChart>
              </ResponsiveContainer>
            </div>
          </motion.div>
        )}

        {/* Features */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mt-8">
          <div className="glass-card p-6 text-center">
            <div className="text-4xl mb-3">⚡</div>
            <h3 className="font-bold text-gray-800 mb-2">Fast Processing</h3>
            <p className="text-sm text-gray-600">Instant predictions for hundreds of students</p>
          </div>
          <div className="glass-card p-6 text-center">
            <div className="text-4xl mb-3">🎯</div>
            <h3 className="font-bold text-gray-800 mb-2">Accurate Results</h3>
            <p className="text-sm text-gray-600">ML-powered predictions with confidence scores</p>
          </div>
          <div className="glass-card p-6 text-center">
            <div className="text-4xl mb-3">📊</div>
            <h3 className="font-bold text-gray-800 mb-2">Detailed Output</h3>
            <p className="text-sm text-gray-600">Includes probabilities for all career paths</p>
          </div>
        </div>
      </motion.div>
    </div>
  );
};

export default BatchPrediction;
