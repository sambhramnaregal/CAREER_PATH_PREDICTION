from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import pandas as pd
import numpy as np
import pickle
import os
from io import BytesIO
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Load ML models
MODEL_PATH = os.path.join(os.path.dirname(__file__), '..', 'models')

def load_model(model_name):
    """Load pickle model file"""
    try:
        model_path = os.path.join(MODEL_PATH, model_name)
        with open(model_path, 'rb') as f:
            return pickle.load(f)
    except Exception as e:
        print(f"Error loading model {model_name}: {e}")
        return None

# Load models at startup
career_model = load_model('career_model.pkl')
career_scaler = load_model('career_scaler.pkl')

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'models_loaded': {
            'career_model': career_model is not None,
            'career_scaler': career_scaler is not None
        }
    })

@app.route('/predict/batch', methods=['POST'])
def predict_batch():
    """Batch prediction from Excel file"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Read Excel file
        df = pd.read_excel(file)
        
        # Preprocess the dataframe
        features = preprocess_batch_data(df)
        features_scaled = career_scaler.transform(features)
        predictions = career_model.predict(features_scaled)
        probabilities = career_model.predict_proba(features_scaled)
        
        # Add predictions to dataframe
        df['Predicted_Career_Path'] = predictions
        
        # Add probability columns
        for idx, class_name in enumerate(career_model.classes_):
            df[f'Probability_{class_name}'] = probabilities[:, idx]
        
        # Save to BytesIO
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Predictions')
        output.seek(0)
        
        # Generate filename with timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'career_predictions_{timestamp}.xlsx'
        
        return send_file(
            output,
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            as_attachment=True,
            download_name=filename
        )
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def preprocess_batch_data(df):
    """Preprocess batch data for prediction"""
    # Map CSV columns to model features
    # CSV has raw data, we need to transform it into model features
    
    # Extract features from CSV
    features = []
    for _, row in df.iterrows():
        feature_row = [
            float(row.get('CGPA', 0)),
            float(row.get('Technical_Skills_Score', 3)) * 20,  # Scale 1-5 to 0-100
            float(row.get('Soft_Skills_Score', 3)) * 20,  # Scale 1-5 to 0-100
            float(row.get('Number_of_Internships', 0)),
            float(row.get('Number_of_Projects', 0)),
            calculate_extracurricular_score_batch(row),
            100.0 if row.get('Leadership_Roles') == 'Yes' else 0.0,
            calculate_creativity_score_batch(row),
            calculate_analytics_score_batch(row),
            float(row.get('Number_of_Publications', 0)) * 15,
            100.0 if row.get('Family_Business_Background') == 'Yes' or row.get('Entrepreneur_Cell_Member') == 'Yes' else 50.0,
            float(row.get('Technical_Skills_Score', 3)) * 20
        ]
        features.append(feature_row)
    
    return np.array(features)

def calculate_extracurricular_score_batch(row):
    """Calculate extracurricular score for batch data"""
    score = 0
    if row.get('Co_curricular_Activities') == 'Yes':
        score += 50
    score += float(row.get('Number_of_Hackathons', 0)) * 8
    score += float(row.get('Number_of_Certification_Courses', 0)) * 3
    return min(score, 100)

def calculate_creativity_score_batch(row):
    """Calculate creativity score for batch data"""
    score = 0
    score += float(row.get('Number_of_Projects', 0)) * 15
    if row.get('Entrepreneur_Cell_Member') == 'Yes':
        score += 40
    score += float(row.get('Number_of_Hackathons', 0)) * 5
    return min(score, 100)

def calculate_analytics_score_batch(row):
    """Calculate analytics score for batch data"""
    score = (float(row.get('CGPA', 0)) / 10) * 60
    score += float(row.get('Number_of_Publications', 0)) * 10
    score += float(row.get('Technical_Skills_Score', 3)) * 8
    return min(score, 100)

@app.route('/predict/individual', methods=['POST'])
def predict_individual():
    """Individual student prediction"""
    try:
        data = request.json
        
        # Extract and preprocess features
        features = extract_individual_features(data)
        
        # Scale features
        features_scaled = career_scaler.transform([features])
        
        # Make prediction
        prediction = career_model.predict(features_scaled)[0]
        probabilities = career_model.predict_proba(features_scaled)[0]
        
        # Get feature importance
        feature_importance = None
        if hasattr(career_model, 'feature_importances_'):
            feature_names = [
                'CGPA', 'Technical Skills', 'Communication Skills', 
                'Internships', 'Projects', 'Extracurricular',
                'Leadership', 'Creativity', 'Analytics', 
                'Research Interest', 'Business Interest', 'Technical Interest'
            ]
            importance_list = career_model.feature_importances_.tolist()
            feature_importance = [
                {'feature': name, 'importance': imp} 
                for name, imp in zip(feature_names, importance_list)
            ]
            feature_importance.sort(key=lambda x: x['importance'], reverse=True)
        
        # Create probability dictionary
        prob_dict = {}
        for idx, class_name in enumerate(career_model.classes_):
            prob_dict[class_name] = float(probabilities[idx])
        
        return jsonify({
            'prediction': prediction,
            'probabilities': prob_dict,
            'feature_importance': feature_importance,
            'confidence': float(max(probabilities))
        })
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def extract_individual_features(data):
    """Extract and encode features from individual student data"""
    # Frontend sends: name, usn, gender, age, cgpa, branch, backlogs, internships, 
    # internship_type, research_papers, projects, certifications, technical_skills,
    # hackathons, soft_skills, cocurricular_activities, leadership_roles, 
    # entrepreneur_cell, family_business
    
    features = [
        float(data.get('cgpa', 0)),
        float(data.get('technical_skills', 3)) * 20,  # Scale 1-5 to 0-100
        float(data.get('soft_skills', 3)) * 20,  # Scale 1-5 to 0-100
        float(data.get('internships', 0)),
        float(data.get('projects', 0)),
        calculate_extracurricular_score(data),
        100.0 if data.get('leadership_roles') == 'Yes' else 0.0,
        calculate_creativity_score(data),
        calculate_analytics_score(data),
        float(data.get('research_papers', 0)) * 15,  # Research interest proxy
        100.0 if data.get('family_business') == 'Yes' or data.get('entrepreneur_cell') == 'Yes' else 50.0,
        float(data.get('technical_skills', 3)) * 20  # Technical interest
    ]
    return features

def calculate_extracurricular_score(data):
    """Calculate extracurricular score"""
    score = 0
    if data.get('cocurricular_activities') == 'Yes':
        score += 50
    score += float(data.get('hackathons', 0)) * 8
    score += float(data.get('certifications', 0)) * 3
    return min(score, 100)

def calculate_creativity_score(data):
    """Calculate creativity score"""
    score = 0
    score += float(data.get('projects', 0)) * 15
    if data.get('entrepreneur_cell') == 'Yes':
        score += 40
    score += float(data.get('hackathons', 0)) * 5
    return min(score, 100)

def calculate_analytics_score(data):
    """Calculate analytics score"""
    score = (float(data.get('cgpa', 0)) / 10) * 60
    score += float(data.get('research_papers', 0)) * 10
    score += float(data.get('technical_skills', 3)) * 8
    return min(score, 100)

@app.route('/calculate/api', methods=['POST'])
def calculate_api():
    """Calculate API (Academic Performance Index) Score"""
    try:
        data = request.json
        
        # Extract inputs
        cgpa = float(data.get('cgpa', 0))
        paid_internships = int(data.get('paid_internships', 0))
        unpaid_internships = int(data.get('unpaid_internships', 0))
        research_papers = int(data.get('research_papers', 0))
        certificates = int(data.get('certificates', 0))
        
        # Calculate scores based on weights
        # CGPA: 20% weight (max 2 points)
        cgpa_points = min((cgpa / 10) * 2, 2)
        
        # Internships: 40% weight (max 4 points)
        # Paid: 2 points each, Unpaid: 1 point each
        internship_points = min(paid_internships * 2 + unpaid_internships, 4)
        
        # Research Work: 20% weight (max 2 points)
        # 0.5 points per publication
        research_points = min(research_papers * 0.5, 2)
        
        # Certifications: 20% weight (max 2 points)
        # 0.1 points per certification
        cert_points = min(certificates * 0.1, 2)
        
        total_score = round(cgpa_points + internship_points + research_points + cert_points, 2)
        
        # Determine feedback (out of 10 now)
        if total_score >= 8.5:
            feedback = "Excellent Profile! You're well-prepared for placements or higher studies."
            level = "excellent"
        elif total_score >= 7.0:
            feedback = "Good Job! Keep boosting your experience and skillset."
            level = "good"
        elif total_score >= 5.0:
            feedback = "Fair. Focus on enhancing your profile with more internships, research, and certifications."
            level = "fair"
        else:
            feedback = "Needs Improvement. Work on academics, internships, research, and certifications."
            level = "needs_improvement"
        
        return jsonify({
            'total_score': total_score,
            'max_score': 10,
            'breakdown': {
                'cgpa_points': round(cgpa_points, 2),
                'internship_points': round(internship_points, 2),
                'research_points': round(research_points, 2),
                'cert_points': round(cert_points, 2)
            },
            'feedback': feedback,
            'level': level
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    os.makedirs(MODEL_PATH, exist_ok=True)
    app.run(debug=True, host='0.0.0.0', port=5000)
