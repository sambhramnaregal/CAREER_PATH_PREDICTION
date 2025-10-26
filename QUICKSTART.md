# Quick Start Guide

## 🎯 What You Need to Do

### Step 1: Copy Your ML Models

**IMPORTANT**: Copy your trained model files (`career_model.pkl` and `career_scaler.pkl`) into the `models/` folder.

```
C:\Career Path Prediction\models\
  ├── career_model.pkl    ← YOUR MODEL HERE
  ├── career_scaler.pkl   ← YOUR SCALER HERE
  └── create_sample_models.py
```

### Step 2: Install Backend Dependencies

Open PowerShell in the project directory:

```powershell
cd "C:\Career Path Prediction\backend"
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### Step 3: Install Frontend Dependencies

Open a NEW PowerShell window:

```powershell
cd "C:\Career Path Prediction\frontend"
npm install
```

### Step 4: Start Backend Server

In the backend PowerShell window:

```powershell
python app.py
```

✅ Backend running at `http://localhost:5000`

### Step 5: Start Frontend Server

In the frontend PowerShell window:

```powershell
npm start
```

✅ Frontend will open at `http://localhost:3000`

## 🎉 You're Done!

The application is now running. Open your browser to `http://localhost:3000`

## 📊 Features to Test

1. **Home Page** - Overview of the system
2. **Batch Prediction** - Upload Excel file with student data
3. **Individual Prediction** - Enter student details for prediction
4. **API Calculator** - Calculate academic performance score

## ❓ If You Don't Have Models Yet

Run this in the `models/` directory:

```powershell
cd "C:\Career Path Prediction\models"
python create_sample_models.py
```

This creates sample models for testing (replace with your actual models later).

## 🐛 Common Issues

### Backend won't start
- Make sure Python 3.8+ is installed
- Activate virtual environment first
- Check if port 5000 is available

### Frontend won't start
- Make sure Node.js 16+ is installed
- Delete `node_modules` and run `npm install` again
- Check if port 3000 is available

### Models not loading
- Ensure `.pkl` files are in `models/` directory
- Check file names match exactly: `career_model.pkl` and `career_scaler.pkl`
