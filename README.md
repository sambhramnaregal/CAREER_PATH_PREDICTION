# Career Path Prediction System

A full-stack web application for predicting career paths of engineering students using Machine Learning. Built with **React + Tailwind CSS** frontend and **Flask** backend.

## 🚀 Features

- **Batch Prediction**: Upload Excel files with student data and get predictions for entire batches
- **Individual Prediction**: Get personalized career path predictions with detailed analysis
- **API Score Calculator**: Calculate Academic Performance Index based on various parameters
- **ML-Powered**: Uses trained Random Forest models for accurate predictions
- **Beautiful UI**: Modern, responsive design with animations and charts
- **Real-time Results**: Instant predictions with confidence scores and visualizations

## 📋 Career Paths

The system predicts one of three career paths:

1. **Higher Studies** - Master's, PhD programs
2. **Placement** - Corporate job placements
3. **Startup** - Entrepreneurship path

## 🛠️ Technology Stack

### Frontend
- React 18
- Tailwind CSS
- Recharts (for data visualization)
- Framer Motion (animations)
- Axios (HTTP client)

### Backend
- Flask
- Scikit-learn
- Pandas
- NumPy
- OpenPyXL (Excel processing)

## 📁 Project Structure

```
Career Path Prediction/
├── backend/
│   ├── app.py                 # Flask API
│   └── requirements.txt       # Python dependencies
├── frontend/
│   ├── public/
│   │   └── index.html
│   ├── src/
│   │   ├── components/
│   │   │   └── Navbar.js
│   │   ├── pages/
│   │   │   ├── Home.js
│   │   │   ├── BatchPrediction.js
│   │   │   ├── IndividualPrediction.js
│   │   │   └── APICalculator.js
│   │   ├── App.js
│   │   ├── index.js
│   │   └── index.css
│   ├── package.json
│   ├── tailwind.config.js
│   └── postcss.config.js
├── models/
│   ├── career_model.pkl       # YOUR TRAINED ML MODEL
│   ├── career_scaler.pkl      # YOUR TRAINED SCALER
│   └── create_sample_models.py
└── README.md
```

## ⚙️ Setup Instructions

### Prerequisites

- **Node.js** (v16 or higher)
- **Python** (v3.8 or higher)
- **npm** or **yarn**

### 1. Clone or Navigate to Project

```powershell
cd "C:\Career Path Prediction"
```

### 2. Place Your ML Models

**IMPORTANT**: Place your trained ML model files in the `models/` directory:
- `career_model.pkl` - Your trained classification model
- `career_scaler.pkl` - Your trained feature scaler

If you don't have models yet, you can create sample models:

```powershell
cd models
python create_sample_models.py
cd ..
```

### 3. Backend Setup

```powershell
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Start Flask server
python app.py
```

The backend will run on `http://localhost:5000`

### 4. Frontend Setup

Open a **NEW** PowerShell window:

```powershell
# Navigate to frontend
cd "C:\Career Path Prediction\frontend"

# Install dependencies
npm install

# Start React development server
npm start
```

The frontend will run on `http://localhost:3000`

## 🎯 Usage

### Batch Prediction

1. Navigate to **Batch Prediction** page
2. Upload an Excel file with the following columns (must match exactly):
   - Name
   - USN
   - Gender
   - Age
   - CGPA (0-10)
   - Branch_Department
   - Number_of_Backlogs
   - Number_of_Internships
   - Type_of_Internships
   - Number_of_Publications
   - Number_of_Projects
   - Number_of_Certification_Courses
   - Technical_Skills_Score (1-5)
   - Number_of_Hackathons
   - Soft_Skills_Score (1-5)
   - Co_curricular_Activities (Yes/No)
   - Leadership_Roles (Yes/No)
   - Entrepreneur_Cell_Member (Yes/No)
   - Family_Business_Background (Yes/No)
3. **Do NOT include** `Status_after_Graduation` column - this will be predicted!
4. Click **Generate Predictions**
5. Download the Excel file with predictions

### Individual Prediction

1. Navigate to **Individual Prediction** page
2. Fill in all 17 fields:
   - Basic info (Name, USN, Gender, Age, CGPA)
   - Academic (Branch, Backlogs)
   - Experience (Internships, Projects, Research Papers, Certifications)
   - Skills (Technical, Soft, Hackathons)
   - Activities (Co-curricular, Leadership, Entrepreneur Cell, Family Business)
3. Click **Get Career Prediction**
4. View results with:
   - Predicted career path
   - Probability distribution
   - Feature importance
   - Personalized recommendations

### API Score Calculator

1. Navigate to **API Calculator** page
2. Enter:
   - CGPA (out of 10)
   - Paid & Unpaid Internships
   - Courses (IIT, NIT, Industry, Other)
   - Certificates
3. Click **Calculate API Score**
4. View score breakdown and analysis

## 📊 ML Model Requirements

Your ML model files should:

- **career_model.pkl**: Trained classification model with:
  - `predict()` method
  - `predict_proba()` method
  - `classes_` attribute
  - `feature_importances_` attribute (optional, for Random Forest)

- **career_scaler.pkl**: Trained StandardScaler or similar with:
  - `transform()` method

### Expected Features (12 features in order):

1. CGPA
2. Technical_Skills
3. Communication_Skills
4. Internships
5. Projects
6. Extracurricular
7. Leadership
8. Creativity
9. Analytics
10. Research_Interest
11. Business_Interest
12. Technical_Interest

## 🔧 API Endpoints

### Backend API

- `GET /health` - Health check
- `POST /predict/batch` - Batch prediction from Excel
- `POST /predict/individual` - Individual student prediction
- `POST /calculate/api` - Calculate API score

## 🎨 Customization

### Update ML Model Path

Edit `backend/app.py`:

```python
MODEL_PATH = os.path.join(os.path.dirname(__file__), '..', 'models')
```

### Update API URL

Edit frontend files:

```javascript
const API_URL = 'http://localhost:5000';
```

### Customize Colors

Edit `frontend/tailwind.config.js` to change color schemes.

## 🐛 Troubleshooting

### Backend Issues

- **Models not loading**: Ensure `.pkl` files are in `models/` directory
- **CORS errors**: Flask-CORS is configured to allow all origins in development
- **Port 5000 in use**: Change port in `app.py`: `app.run(port=5001)`

### Frontend Issues

- **Port 3000 in use**: React will prompt to use another port
- **npm install fails**: Try `npm install --legacy-peer-deps`
- **API connection fails**: Check backend is running on port 5000

## 📝 Notes

- The system uses **synthetic data** for training by default
- Replace with **real student data** for production use
- Ensure data privacy and compliance when using real student information
- The frontend displays predictions from your trained ML models
- All predictions are made by the backend ML models, not hardcoded

## 📄 License

This project is for educational purposes.

## 👤 Author

Built for career path prediction system for engineering students.
