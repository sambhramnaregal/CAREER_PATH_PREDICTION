# Career Path Prediction System - Project Summary

## ✅ What Has Been Built

A complete full-stack web application with:

### Backend (Flask API)
- **Location**: `backend/app.py`
- **Features**:
  - ✅ Batch prediction endpoint (`/predict/batch`)
  - ✅ Individual prediction endpoint (`/predict/individual`)
  - ✅ API score calculator endpoint (`/calculate/api`)
  - ✅ Health check endpoint
  - ✅ Loads your ML models from `models/` directory
  - ✅ Excel file processing for batch predictions
  - ✅ Feature extraction from 17 input fields
  - ✅ CORS enabled for frontend communication

### Frontend (React + Tailwind)
- **Location**: `frontend/src/`
- **Pages**:
  1. ✅ **Home Page** - Beautiful landing page with features
  2. ✅ **Batch Prediction** - Excel upload/download functionality
  3. ✅ **Individual Prediction** - 17-field form with all required inputs
  4. ✅ **API Calculator** - Academic performance score calculator

### UI Features
- ✅ Modern gradient design with glass-morphism effects
- ✅ Smooth animations with Framer Motion
- ✅ Interactive charts with Recharts (Bar, Pie, Progress bars)
- ✅ Responsive design (mobile, tablet, desktop)
- ✅ Beautiful color schemes and icons
- ✅ Loading states and error handling

## 📋 Required From You

### 1. **Your ML Models** (CRITICAL)
Place these files in `models/` directory:
- `career_model.pkl` - Your trained classification model
- `career_scaler.pkl` - Your trained feature scaler

**Model Requirements**:
- Must have `predict()` and `predict_proba()` methods
- Must accept 12 features in this order:
  1. CGPA (0-100)
  2. Technical_Skills (0-100)
  3. Communication_Skills (0-100)
  4. Internships (count)
  5. Projects (count)
  6. Extracurricular (0-100)
  7. Leadership (0-100)
  8. Creativity (0-100)
  9. Analytics (0-100)
  10. Research_Interest (0-100)
  11. Business_Interest (0-100)
  12. Technical_Interest (0-100)

### 2. **Install Dependencies**

#### Backend:
```powershell
cd "C:\Career Path Prediction\backend"
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

#### Frontend:
```powershell
cd "C:\Career Path Prediction\frontend"
npm install
```

## 🚀 How to Run

### Start Backend:
```powershell
cd "C:\Career Path Prediction\backend"
.\venv\Scripts\Activate.ps1
python app.py
```

### Start Frontend (new window):
```powershell
cd "C:\Career Path Prediction\frontend"
npm start
```

## 🎯 How It Works

### Individual Prediction Flow:
1. User fills 17 fields in the form (Name, USN, CGPA, etc.)
2. Frontend sends POST request to `/predict/individual`
3. Backend extracts and transforms features into 12 ML features
4. Your ML model predicts: Higher Studies / Placement / Startup
5. Frontend displays:
   - Predicted career path with confidence
   - Probability distribution (bar + pie chart)
   - Feature importance (bar chart)
   - Personalized recommendations

### Batch Prediction Flow:
1. User uploads Excel file with required columns
2. Frontend sends file to `/predict/batch`
3. Backend processes each row through ML model
4. Adds `Predicted_Career_Path` column + probability columns
5. Returns Excel file for download

### API Calculator Flow:
1. User enters CGPA, internships, courses, certificates
2. Frontend sends to `/calculate/api`
3. Backend calculates weighted score (out of 10)
4. Frontend displays score with breakdown and visualization

## 📊 Feature Mapping (Individual → ML)

The backend automatically converts 17 form fields into 12 ML features:

| Form Input | ML Feature | Transformation |
|------------|-----------|----------------|
| CGPA | CGPA | Direct (0-10 scale) |
| Technical Skills (1-5) | Technical_Skills | × 20 (0-100) |
| Soft Skills (1-5) | Communication_Skills | × 20 (0-100) |
| Internships | Internships | Direct count |
| Projects | Projects | Direct count |
| Co-curricular + Hackathons + Certs | Extracurricular | Calculated score |
| Leadership Roles (Yes/No) | Leadership | 100 or 0 |
| Projects + Entrepreneur Cell | Creativity | Calculated score |
| CGPA + Research Papers | Analytics | Calculated score |
| Research Papers | Research_Interest | × 15 |
| Family Business + Entrepreneur | Business_Interest | 100 or 50 |
| Technical Skills | Technical_Interest | × 20 (0-100) |

## 🎨 UI Screenshots (What Users Will See)

### Home Page
- Hero section with gradient text
- 3 feature cards (Batch, Individual, API Calculator)
- Stats section with icons
- Career paths overview

### Batch Prediction
- Drag-and-drop Excel upload area
- Instructions for required columns
- Download button for predictions
- Success/error messages

### Individual Prediction
- **Left side**: Comprehensive form with 17 fields
- **Right side**: 
  - Large prediction card with emoji and gradient
  - Probability bars for all 3 career paths
  - Pie chart distribution
  - Feature importance bar chart
  - Personalized recommendations

### API Calculator
- **Left side**: Input form with CGPA, internships, courses
- **Right side**:
  - Large score display with color coding
  - Feedback message
  - Score breakdown with progress bars
  - Pie chart distribution

## 📁 Project Files

```
C:\Career Path Prediction\
├── backend/
│   ├── app.py                    # Flask API (250 lines)
│   └── requirements.txt          # Python dependencies
├── frontend/
│   ├── src/
│   │   ├── pages/
│   │   │   ├── Home.js           # Landing page
│   │   │   ├── BatchPrediction.js        # Excel upload/download
│   │   │   ├── IndividualPrediction.js   # 17-field form
│   │   │   └── APICalculator.js          # Score calculator
│   │   ├── components/
│   │   │   └── Navbar.js         # Navigation bar
│   │   ├── App.js                # Routing
│   │   ├── index.js              # Entry point
│   │   └── index.css             # Tailwind + custom styles
│   ├── public/
│   │   └── index.html
│   ├── package.json              # Dependencies
│   ├── tailwind.config.js        # Tailwind config
│   └── postcss.config.js
├── models/
│   └── create_sample_models.py   # Sample model generator
├── README.md                     # Full documentation
├── QUICKSTART.md                 # Quick start guide
└── .gitignore                    # Git ignore rules
```

## 🔧 Customization Options

### Change Colors:
Edit `frontend/tailwind.config.js` - modify primary/secondary colors

### Change API URL:
Edit all `frontend/src/pages/*.js` files:
```javascript
const API_URL = 'http://localhost:5000';
```

### Modify Feature Weights:
Edit `backend/app.py` - functions like `calculate_extracurricular_score()`

## ✨ Key Technologies Used

- **React 18** - UI framework
- **Tailwind CSS** - Styling
- **Framer Motion** - Animations
- **Recharts** - Charts and graphs
- **Flask** - Backend API
- **Scikit-learn** - ML model loading
- **Pandas** - Excel processing
- **Axios** - HTTP requests

## 🎉 What's Ready

Everything is ready to run! Just:
1. Place your ML models in `models/`
2. Install dependencies
3. Start both servers
4. Open browser to `http://localhost:3000`

The system will use YOUR trained ML models for all predictions!
