from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import pandas as pd
import numpy as np
import pickle
import os
from io import BytesIO
from datetime import datetime
import google.generativeai as genai
import json
from dotenv import load_dotenv
import base64

load_dotenv() # Load environment variables from .env file

app = Flask(__name__)
CORS(app)

# --- Configuration ---
MODEL_PATH = os.path.join(os.path.dirname(__file__), '..', 'models')
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

# --- Load Models ---
def load_model(model_name):
    """Load pickle model file"""
    try:
        model_path = os.path.join(MODEL_PATH, model_name)
        if not os.path.exists(model_path):
            print(f"⚠️ Model {model_name} not found.")
            return None
        with open(model_path, 'rb') as f:
            return pickle.load(f)
    except Exception as e:
        print(f"Error loading model {model_name}: {e}")
        return None

# Load models at startup
kmeans_model = load_model('kmeans_model.pkl')
scaler = load_model('scaler.pkl')
cluster_info = load_model('cluster_info.pkl')

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'models_loaded': {
            'kmeans_model': kmeans_model is not None,
            'scaler': scaler is not None,
            'cluster_info': cluster_info is not None
        },
        'gemini_configured': GEMINI_API_KEY is not None
    })

@app.route('/predict/batch', methods=['POST'])
def predict_batch():
    """Batch prediction from Excel file using Unsupervised Learning"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Read Excel file
        df = pd.read_excel(file)
        
        # Preprocess
        features = preprocess_batch_data(df)
        
        if scaler and kmeans_model:
            features_scaled = scaler.transform(features)
            clusters = kmeans_model.predict(features_scaled)
            
            # Map clusters to names/roles
            df['Cluster_ID'] = clusters
            
            if cluster_info:
                df['Predicted_Profile'] = [cluster_info.get(c, {}).get('name', f'Cluster {c}') for c in clusters]
                df['Suggested_Roles'] = [", ".join(cluster_info.get(c, {}).get('roles', [])) for c in clusters]
            else:
                df['Predicted_Profile'] = [f'Cluster {c}' for c in clusters]
        else:
            return jsonify({'error': 'Models not loaded'}), 500
        
        # Calculate Distribution for Pie Chart
        distribution = df['Predicted_Profile'].value_counts().to_dict()
        
        # Save to BytesIO
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Predictions')
        output.seek(0)
        
        # Encode to base64
        file_base64 = base64.b64encode(output.getvalue()).decode('utf-8')
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'career_profiles_{timestamp}.xlsx'
        
        return jsonify({
            'success': True,
            'filename': filename,
            'file_base64': file_base64,
            'distribution': distribution
        })
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def preprocess_batch_data(df):
    """Preprocess batch data for prediction (Must match training logic)"""
    features = []
    for _, row in df.iterrows():
        # Calculate extracurricular score
        extracurricular = 0
        if row.get('Co_curricular_Activities') == 'Yes': extracurricular += 50
        extracurricular += float(row.get('Number_of_Hackathons', 0)) * 8
        extracurricular += float(row.get('Number_of_Certification_Courses', 0)) * 3
        extracurricular = min(extracurricular, 100)
        
        # Calculate creativity score
        creativity = 0
        creativity += float(row.get('Number_of_Projects', 0)) * 15
        if row.get('Entrepreneur_Cell_Member') == 'Yes': creativity += 40
        creativity += float(row.get('Number_of_Hackathons', 0)) * 5
        creativity = min(creativity, 100)
        
        # Calculate analytics score
        analytics = (float(row.get('CGPA', 0)) / 10) * 60
        analytics += float(row.get('Number_of_Publications', 0)) * 10
        analytics += float(row.get('Technical_Skills_Score', 0)) * 8
        analytics = min(analytics, 100)
        
        # Business interest
        business_interest = 100.0 if (row.get('Family_Business_Background') == 'Yes' or 
                                      row.get('Entrepreneur_Cell_Member') == 'Yes') else 50.0

        feature_row = [
            float(row.get('CGPA', 0)),                                    
            float(row.get('Technical_Skills_Score', 0)) * 20,             
            float(row.get('Soft_Skills_Score', 0)) * 20,                  
            float(row.get('Number_of_Internships', 0)),                   
            float(row.get('Number_of_Projects', 0)),                      
            extracurricular,                                
            100.0 if row.get('Leadership_Roles') == 'Yes' else 0.0, 
            creativity,                                     
            analytics,                                      
            float(row.get('Number_of_Publications', 0)) * 15,             
            business_interest,                              
            float(row.get('Technical_Skills_Score', 0)) * 20              
        ]
        features.append(feature_row)
    
    return np.array(features)

@app.route('/predict/individual', methods=['POST'])
def predict_individual():
    """Individual student prediction + Gemini Roadmap"""
    try:
        data = request.json
        
        # Extract features
        features = extract_individual_features(data)
        
        if not (scaler and kmeans_model):
             return jsonify({'error': 'Models not loaded'}), 500

        # Scale and Predict
        features_scaled = scaler.transform([features])
        cluster_id = int(kmeans_model.predict(features_scaled)[0])
        
        # Get Cluster Info
        info = cluster_info.get(cluster_id, {}) if cluster_info else {}
        profile_name = info.get('name', f'Cluster {cluster_id}')
        roles = info.get('roles', [])
        description = info.get('description', '')
        
        # Generate Personalized Roadmap with Gemini
        roadmap = "Gemini API Key not configured."
        if GEMINI_API_KEY:
            roadmap = generate_roadmap(data, profile_name, roles)
        
        return jsonify({
            'cluster_id': cluster_id,
            'profile_name': profile_name,
            'suggested_roles': roles,
            'description': description,
            'roadmap': roadmap
        })
            
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': str(e)}), 500

def generate_roadmap(data, profile_name, roles):
    """Generate personalized roadmap using Gemini"""
    try:
        # Reverted to gemini-pro
        model = genai.GenerativeModel('gemini-pro')
        prompt = f"""
        Create a personalized career roadmap for a Computer Science student.
        
        PROFILE: {profile_name}
        SUGGESTED ROLES: {roles}
        
        STUDENT DATA:
        - CGPA: {data.get('cgpa')}
        - Skills Score: {data.get('technical_skills')}/5
        - Internships: {data.get('internships')}
        - Projects: {data.get('projects')}
        
        Please provide a month-by-month roadmap for the next 6 months to help them achieve these roles.
        Format as Markdown.
        """
        
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error generating roadmap: {str(e)}"

@app.route('/chat', methods=['POST'])
def chat():
    """Interactive chat with Gemini about career guidance"""
    try:
        data = request.json
        message = data.get('message')
        history = data.get('history', [])
        context = data.get('context', {}) # Student data/profile context
        
        if not message:
            return jsonify({'error': 'Message is required'}), 400

        model = genai.GenerativeModel('gemini-pro')
        
        # Construct a system prompt with context
        system_prompt = f"""
        You are a helpful Career Counselor AI. 
        The student you are talking to has the following profile:
        - Predicted Profile: {context.get('profile_name', 'Unknown')}
        - Suggested Roles: {context.get('roles', 'Unknown')}
        - Technical Skills: {context.get('technical_score', 'N/A')}/5
        
        Answer their questions specifically about their career path, skills, and opportunities.
        Keep answers concise and encouraging.
        """
        
        full_prompt = f"{system_prompt}\n\nUser: {message}"
        
        response = model.generate_content(full_prompt)
        
        return jsonify({
            'response': response.text
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def extract_individual_features(data):
    """Extract features from individual request (Must match training logic)"""
    # Calculate derived scores
    
    # Extracurricular
    extracurricular = 0
    if data.get('cocurricular_activities') == 'Yes': extracurricular += 50
    extracurricular += float(data.get('hackathons', 0)) * 8
    extracurricular += float(data.get('certifications', 0)) * 3
    extracurricular = min(extracurricular, 100)
    
    # Creativity
    creativity = 0
    creativity += float(data.get('projects', 0)) * 15
    if data.get('entrepreneur_cell') == 'Yes': creativity += 40
    creativity += float(data.get('hackathons', 0)) * 5
    creativity = min(creativity, 100)
    
    # Analytics
    analytics = (float(data.get('cgpa', 0)) / 10) * 60
    analytics += float(data.get('research_papers', 0)) * 10
    analytics += float(data.get('technical_skills', 3)) * 8
    analytics = min(analytics, 100)
    
    # Business Interest
    business_interest = 100.0 if (data.get('family_business') == 'Yes' or 
                                  data.get('entrepreneur_cell') == 'Yes') else 50.0

    features = [
        float(data.get('cgpa', 0)),
        float(data.get('technical_skills', 3)) * 20,
        float(data.get('soft_skills', 3)) * 20,
        float(data.get('internships', 0)),
        float(data.get('projects', 0)),
        extracurricular,
        100.0 if data.get('leadership_roles') == 'Yes' else 0.0,
        creativity,
        analytics,
        float(data.get('research_papers', 0)) * 15,
        business_interest,
        float(data.get('technical_skills', 3)) * 20
    ]
    return features

@app.route('/calculate/api', methods=['POST'])
def calculate_api():
    """Calculate API (Academic Performance Index) Score - Unchanged"""
    try:
        data = request.json
        cgpa = float(data.get('cgpa', 0))
        paid_internships = int(data.get('paid_internships', 0))
        unpaid_internships = int(data.get('unpaid_internships', 0))
        research_papers = int(data.get('research_papers', 0))
        certificates = int(data.get('certificates', 0))
        
        cgpa_points = min((cgpa / 10) * 2, 2)
        internship_points = min(paid_internships * 2 + unpaid_internships, 4)
        research_points = min(research_papers * 0.5, 2)
        cert_points = min(certificates * 0.1, 2)
        
        total_score = round(cgpa_points + internship_points + research_points + cert_points, 2)
        
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
