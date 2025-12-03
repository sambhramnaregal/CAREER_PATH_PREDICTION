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
import torch
from pytorch_tabnet.pretraining import TabNetPretrainer

load_dotenv()

app = Flask(__name__)
CORS(app)

# --- Configuration ---
MODEL_PATH = os.path.join(os.path.dirname(__file__), '..', 'models')
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

# --- Constants (Must match training) ---
CATEGORICAL_COLS = [
    'Gender', 'Branch_Department', 'Type_of_Internships', 
    'Co_curricular_Activities', 'Leadership_Roles', 
    'Entrepreneur_Cell_Member', 'Family_Business_Background'
]

NUMERICAL_COLS = [
    'Age', 'CGPA', 'Number_of_Backlogs', 'Number_of_Internships', 
    'Number_of_Publications', 'Number_of_Projects', 
    'Number_of_Certification_Courses', 'Technical_Skills_Score', 
    'Number_of_Hackathons', 'Soft_Skills_Score'
]

# --- Load Models ---
kmeans_model = None
scaler = None
label_encoders = None
tabnet_model = None
cluster_info = None

def load_models():
    global kmeans_model, scaler, label_encoders, tabnet_model, cluster_info
    try:
        print("Loading models...")
        with open(os.path.join(MODEL_PATH, 'kmeans_model.pkl'), 'rb') as f:
            kmeans_model = pickle.load(f)
            
        with open(os.path.join(MODEL_PATH, 'scaler.pkl'), 'rb') as f:
            scaler = pickle.load(f)
            
        with open(os.path.join(MODEL_PATH, 'label_encoders.pkl'), 'rb') as f:
            label_encoders = pickle.load(f)
            
        with open(os.path.join(MODEL_PATH, 'cluster_info.pkl'), 'rb') as f:
            cluster_info = pickle.load(f)
            
        # Load TabNet
        tabnet_model = TabNetPretrainer()
        tabnet_model.load_model(os.path.join(MODEL_PATH, 'tabnet_model.zip'))
        
        print("Models loaded successfully.")
    except Exception as e:
        print(f"Error loading models: {e}")
        with open('backend_error.log', 'a') as f:
            f.write(f"Model Load Error: {str(e)}\n")

load_models()

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'healthy',
        'models_loaded': {
            'kmeans': kmeans_model is not None,
            'tabnet': tabnet_model is not None,
            'scaler': scaler is not None
        }
    })

def preprocess_features(df):
    """Preprocess dataframe to match TabNet input"""
    # 1. Normalize columns
    df.columns = [c.strip() for c in df.columns]
    
    # 2. Fill missing
    for col in NUMERICAL_COLS:
        if col in df.columns:
            df[col] = df[col].fillna(0) # Use 0 or median? 0 is safer for single rows
            
    for col in CATEGORICAL_COLS:
        if col in df.columns:
            df[col] = df[col].fillna('Unknown')
            
    # 3. Encode Categorical
    for col in CATEGORICAL_COLS:
        if col in df.columns and col in label_encoders:
            le = label_encoders[col]
            # Handle unseen labels
            df[col] = df[col].astype(str).map(lambda s: s if s in le.classes_ else 'Unknown')
            # If 'Unknown' not in classes, we might have an issue. 
            # Ideally we should have 'Unknown' in training or use a robust encoder.
            # For now, we'll try to transform, and if error, replace with 0 (assuming 0 is valid or first class)
            try:
                df[col] = le.transform(df[col])
            except:
                 # Fallback: assign to mode or 0
                 df[col] = 0
                 
    # 4. Scale Numerical
    if all(c in df.columns for c in NUMERICAL_COLS):
        df[NUMERICAL_COLS] = scaler.transform(df[NUMERICAL_COLS])
        
    # 5. Combine
    feature_cols = NUMERICAL_COLS + CATEGORICAL_COLS
    
    # Ensure all columns exist
    for col in feature_cols:
        if col not in df.columns:
            df[col] = 0
            
    return df[feature_cols].values

def get_embeddings(model, X):
    """Robust embedding extraction matching training script"""
    try:
        res = model.predict_latent(X)
        if isinstance(res, tuple): 
            if len(res) >= 2: return res[1]
            elif len(res) == 1: return res[0]
        return res
    except Exception as e:
        print(f"predict_latent failed: {e}")
        
    try:
        device = model.device
        model.network.eval()
        with torch.no_grad():
            X_tensor = torch.from_numpy(X).float().to(device)
            res = model.network(X_tensor)
            if isinstance(res, tuple):
                if len(res) >= 2: return res[1].cpu().numpy()
                return res[0].cpu().numpy()
            return res.cpu().numpy()
    except Exception as e:
        print(f"Direct network access failed: {e}")
        return None

@app.route('/predict/batch', methods=['POST'])
def predict_batch():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400
        
        file = request.files['file']
        df = pd.read_excel(file)
        
        # Preprocess
        X = preprocess_features(df.copy())
        
        # TabNet Embeddings
        embeddings = get_embeddings(tabnet_model, X)
        if embeddings is None:
             return jsonify({'error': 'Failed to generate embeddings'}), 500
        
        # KMeans
        clusters = kmeans_model.predict(embeddings)
        
        df['Cluster_ID'] = clusters
        df['Predicted_Profile'] = [cluster_info.get(c, {}).get('name', f'Cluster {c}') for c in clusters]
        df['Suggested_Roles'] = [", ".join(cluster_info.get(c, {}).get('roles', [])) for c in clusters]
        
        # Distribution
        distribution = df['Predicted_Profile'].value_counts().to_dict()
        
        # Output
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False)
        output.seek(0)
        
        file_base64 = base64.b64encode(output.getvalue()).decode('utf-8')
        
        return jsonify({
            'success': True,
            'filename': f'predictions_{datetime.now().strftime("%Y%m%d")}.xlsx',
            'file_base64': file_base64,
            'distribution': distribution
        })
        
    except Exception as e:
        print(f"Batch Error: {e}")
        with open('backend_error.log', 'a') as f:
            f.write(f"Batch Error: {str(e)}\n")
        return jsonify({'error': str(e)}), 500

@app.route('/predict/individual', methods=['POST'])
def predict_individual():
    try:
        data = request.json
        
        # Convert JSON to DataFrame to reuse preprocessing
        # We need to map JSON keys to expected Excel columns
        # Mapping based on typical JSON keys sent from frontend vs Excel columns
        
        # Map frontend keys to backend columns
        input_data = {
            'Age': data.get('age', 20),
            'CGPA': data.get('cgpa', 0),
            'Number_of_Backlogs': data.get('backlogs', 0),
            'Number_of_Internships': data.get('internships', 0),
            'Number_of_Publications': data.get('research_papers', 0),
            'Number_of_Projects': data.get('projects', 0),
            'Number_of_Certification_Courses': data.get('certifications', 0),
            'Technical_Skills_Score': data.get('technical_skills', 1),
            'Number_of_Hackathons': data.get('hackathons', 0),
            'Soft_Skills_Score': data.get('soft_skills', 1),
            
            'Gender': data.get('gender', 'Male'),
            'Branch_Department': data.get('branch', 'CSE'),
            'Type_of_Internships': data.get('internship_type', 'None'),
            'Co_curricular_Activities': data.get('cocurricular', 'No'),
            'Leadership_Roles': data.get('leadership', 'No'),
            'Entrepreneur_Cell_Member': data.get('entrepreneur_cell', 'No'),
            'Family_Business_Background': data.get('family_business', 'No')
        }
        
        df_input = pd.DataFrame([input_data])
        
        X = preprocess_features(df_input)
        
        embeddings = get_embeddings(tabnet_model, X)
        if embeddings is None:
             return jsonify({'error': 'Failed to generate embeddings'}), 500
             
        cluster_id = int(kmeans_model.predict(embeddings)[0])
        
        info = cluster_info.get(cluster_id, {})
        
        # Roadmap
        roadmap = "Gemini API Key missing."
        if GEMINI_API_KEY:
            roadmap = generate_roadmap(data, info.get('name'), info.get('roles'))
            
        return jsonify({
            'cluster_id': cluster_id,
            'profile_name': info.get('name', f'Cluster {cluster_id}'),
            'suggested_roles': info.get('roles', []),
            'description': info.get('description', ''),
            'roadmap': roadmap
        })
        
    except Exception as e:
        print(f"Individual Error: {e}")
        with open('backend_error.log', 'a') as f:
            f.write(f"Individual Error: {str(e)}\n")
        return jsonify({'error': str(e)}), 500

def generate_roadmap(data, profile, roles):
    try:
        model = genai.GenerativeModel('models/gemma-3-1b-it')
        prompt = f"""
        Create a 6-month career roadmap for a student aiming for: {profile}
        Roles: {roles}
        
        Current Stats:
        CGPA: {data.get('cgpa')}
        Skills: {data.get('technical_skills')}/5
        
        Format as Markdown.
        """
        return model.generate_content(prompt).text
    except:
        return "Could not generate roadmap."

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        msg = data.get('message')
        context = data.get('context', {})
        
        model = genai.GenerativeModel('models/gemma-3-1b-it')
        prompt = f"""
        Context: Student Profile - {context.get('profile_name')}
        User: {msg}
        """
        return jsonify({'response': model.generate_content(prompt).text})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
