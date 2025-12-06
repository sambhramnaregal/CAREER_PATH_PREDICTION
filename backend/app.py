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

# Load .env from parent directory
dotenv_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(dotenv_path)

app = Flask(__name__)
CORS(app)

# --- Configuration ---
MODEL_PATH = os.path.join(os.path.dirname(__file__), '..', 'models')
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL_NAME = os.getenv("GEMINI_MODEL_NAME", "models/gemma-3-1b-it")

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
pca_model = None
cluster_info = None


def load_models():
    global kmeans_model, scaler, pca_model, cluster_info, label_encoders
    try:
        print("Loading updated models...")

        with open(os.path.join(MODEL_PATH, 'kmeans_model.pkl'), 'rb') as f:
            kmeans_model = pickle.load(f)

        with open(os.path.join(MODEL_PATH, 'scaler.pkl'), 'rb') as f:
            scaler = pickle.load(f)

        with open(os.path.join(MODEL_PATH, 'pca.pkl'), 'rb') as f:
            pca_model = pickle.load(f)

        with open(os.path.join(MODEL_PATH, 'cluster_info.pkl'), 'rb') as f:
            cluster_info = pickle.load(f)

        # label encoders were optional but now forced
        label_path = os.path.join(MODEL_PATH, 'label_encoders.pkl')
        if os.path.exists(label_path):
            with open(label_path, 'rb') as f:
                label_encoders = pickle.load(f)
        else:
            label_encoders = {}

        print("Models loaded successfully!")

    except Exception as e:
        print(f"Error loading models: {e}")
        cluster_info = {}

        with open('backend_error.log', 'a') as f:
            f.write(f"Model Load Error: {str(e)}\n")


load_models()


@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'healthy',
        'models_loaded': {
            'kmeans': kmeans_model is not None,
            'pca': pca_model is not None,
            'scaler': scaler is not None
        }
    })


def preprocess_features(df):
    """Preprocess dataframe to match PCA model input"""

    df.columns = [c.strip() for c in df.columns]

    # Ensure ALL required columns exist even for missing keys
    for col in NUMERICAL_COLS:
        if col not in df.columns:
            df[col] = 0
        df[col] = df[col].fillna(0)

    for col in CATEGORICAL_COLS:
        if col not in df.columns:
            df[col] = "Unknown"
        df[col] = df[col].fillna("Unknown")

        # Apply encoders if available
        if label_encoders and col in label_encoders:
            le = label_encoders[col]
            df[col] = df[col].astype(str).apply(
                lambda x: x if x in le.classes_ else le.classes_[0]
            )
            df[col] = le.transform(df[col])
        else:
            df[col] = df[col].astype(str).astype("category").cat.codes

    # 🔥 VERY IMPORTANT FIX:
    # Convert df[NUMERICAL_COLS] to numeric before scaling
    df[NUMERICAL_COLS] = df[NUMERICAL_COLS].apply(pd.to_numeric, errors='coerce').fillna(0)

    # 🔥 Now scale safely (scaler expects 2D numeric array)
    df[NUMERICAL_COLS] = scaler.transform(df[NUMERICAL_COLS].values)

    # Construct final array
    final_df = df[NUMERICAL_COLS + CATEGORICAL_COLS]

    # Final sanity check
    final_df = final_df.fillna(0)

    return final_df


def get_embeddings(X):
    global pca_model

    try:
        if pca_model is None:
            print("WARNING: PCA model missing — returning original X")
            return X.astype(np.float64)

        # Ensure input is 2D and float64
        if X.ndim == 1:
            X = X.reshape(1, -1)
        
        # Enforce float64 for sklearn compatibility
        X_float = X.astype(np.float64)

        transformed = pca_model.transform(X_float)

        if transformed is None:
            print("WARNING: PCA returned None — fallback")
            return X_float

        transformed = np.nan_to_num(transformed)

        return transformed.astype(np.float64)

    except Exception as e:
        print(f"PCA Transform Error: {e} — using fallback")
        return X.astype(np.float64)



@app.route('/predict/individual', methods=['POST'])
def predict_individual():
    with open("verify_execution.txt", "a") as f:
        f.write(f"Executing predict_individual at {datetime.now()}\n")
    
    try:
        data = request.json

        # Prepare consistent input dictionary
        input_data = {
            'Age': data.get('age', 0),
            'CGPA': data.get('cgpa', 0),
            'Number_of_Backlogs': data.get('backlogs', 0),
            'Number_of_Internships': data.get('internships', 0),
            'Number_of_Publications': data.get('research_papers', 0),
            'Number_of_Projects': data.get('projects', 0),
            'Number_of_Certification_Courses': data.get('certifications', 0),
            'Technical_Skills_Score': data.get('technical_skills', 1),
            'Number_of_Hackathons': data.get('hackathons', 0),
            'Soft_Skills_Score': data.get('soft_skills', 1),

            'Gender': data.get('gender', 'Unknown'),
            'Branch_Department': data.get('branch', 'Unknown'),
            'Type_of_Internships': data.get('internship_type', 'Unknown'),
            'Co_curricular_Activities': data.get('cocurricular', 'Unknown'),
            'Leadership_Roles': data.get('leadership', 'Unknown'),
            'Entrepreneur_Cell_Member': data.get('entrepreneur_cell', 'Unknown'),
            'Family_Business_Background': data.get('family_business', 'Unknown')
        }

        # Convert into DF
        df_input = pd.DataFrame([input_data])

        # Preprocess - now returns DataFrame with correct columns
        df_processed = preprocess_features(df_input)
        
        # Extract ONLY numerical columns for PCA (first 10 cols)
        # Extract ONLY numerical columns for PCA (first 10 cols)
        X_numerical = df_processed[NUMERICAL_COLS].values
        
        # PCA embeddings (Optional/Unused for prediction if KMeans expects full features)
        # We still calculate it if needed, but for KMeans we use full X if it expects 17.
        # Based on error "KMeans expecting 17", we must use the full 17 features.
        # Use ascontiguousarray to ensure memory layout matches expectation. 
        # Float64 failed. Float32 succeeded in dummy test. Model likely expects Float32.
        X_full = np.ascontiguousarray(df_processed.values, dtype=np.float32)
        
        try:
             # Try predicting with full features
             cluster_id = int(kmeans_model.predict(X_full)[0])
        except Exception as e:
             print(f"KMeans Full Feature Error: {e}")
             # Detailed error for debugging
             raise ValueError(f"KMeans prediction failed: {str(e)}. Input shape: {X_full.shape}, dtype: {X_full.dtype}")

        print("Predicted cluster:", cluster_id)

        # Cluster info safety check
        info = {}
        if cluster_info and isinstance(cluster_info, dict):
            info = cluster_info.get(cluster_id, {})

        # Generate roadmap
        if GEMINI_API_KEY:
            roadmap = generate_roadmap(data, info.get('name', ''), info.get('roles'))
        else:
            roadmap = "Gemini API Key missing."

        return jsonify({
            'cluster_id': cluster_id,
            'profile_name': info.get('name', f'Cluster {cluster_id}'),
            'suggested_roles': info.get('roles', []),
            'description': info.get('description', ""),
            'roadmap': roadmap
        })


    except Exception as e:
        print(f"Individual Error: {e}")
        return jsonify({'error': f"An error occurred: {str(e)}"}), 500


@app.route('/predict/batch', methods=['POST'])
def predict_batch():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file part'}), 400

        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400

        if file:
            # Read file
            if file.filename.endswith('.csv'):
                df = pd.read_csv(file)
            elif file.filename.endswith(('.xls', '.xlsx')):
                df = pd.read_excel(file)
            else:
                return jsonify({'error': 'Invalid file format. Use CSV or Excel'}), 400

            # Preprocess
            df_processed = preprocess_features(df.copy())
            
            # Predict
            # Apply same fix: Use ascontiguousarray with float32 for KMeans
            X_full = np.ascontiguousarray(df_processed.values, dtype=np.float32)
            
            clusters = kmeans_model.predict(X_full)
            
            # Enrich DataFrame
            df['Cluster_ID'] = clusters
            df['Profile_Name'] = [
                cluster_info.get(int(c), {}).get('name', f'Cluster {c}') 
                for c in clusters
            ]
            df['Suggested_Roles'] = [
                ", ".join(cluster_info.get(int(c), {}).get('roles', [])) 
                for c in clusters
            ]
            
            # Calculate Distribution
            distribution = df['Profile_Name'].value_counts().to_dict()

            # Convert back to CSV/Excel
            output = BytesIO()
            df.to_csv(output, index=False)
            output.seek(0)
            
            # Encode to base64
            file_base64 = base64.b64encode(output.getvalue()).decode('utf-8')
            
            return jsonify({
                'success': True,
                'file_base64': file_base64,
                'filename': 'career_predictions.csv',
                'distribution': distribution
            })

    except Exception as e:
        print(f"Batch Error: {e}")
        return jsonify({'error': f"Batch processing failed: {str(e)}"}), 500



def generate_roadmap(data, profile, roles):
    try:
        model = genai.GenerativeModel(GEMINI_MODEL_NAME)

        prompt = f"""
        Create a career roadmap for student aiming for: {profile}
        Target roles: {roles}

        Student details:
        CGPA: {data.get('cgpa')}
        Projects: {data.get('projects')}

        Provide a 6 month plan.
        """

        response = model.generate_content(prompt)
        return response.text

    except:
        return "Could not generate roadmap."


@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        user_message = data.get('message', '')
        history = data.get('history', [])
        context = data.get('context', {})

        if not user_message:
            return jsonify({'error': 'Message is required'}), 400

        # Construct System Prompt with Context
        system_prompt = f"""
        You are a helpful Career Counselor AI.
        Context about the student:
        - Profile: {context.get('profile_name', 'Student')}
        - Suggested Roles: {context.get('roles', 'N/A')}
        - Technical Skill Score: {context.get('technical_score', 'N/A')}/5
        
        Answer the student's question based on this profile. Be encouraging and practical.
        """

        # Initialize Chat
        model = genai.GenerativeModel(GEMINI_MODEL_NAME)
        chat_session = model.start_chat(history=[])
        
        # Add limited history context if needed, but for simplicity we send a composed prompt
        # or just the latest message with system instruction.
        # Gemini API supports system_instruction on model creation in newer versions, 
        # but here we'll just prepend it to the message or assume stateless content generation for simplicity 
        # due to unknown library version features.
        
        full_prompt = f"{system_prompt}\n\nStudent: {user_message}"
        
        response = model.generate_content(full_prompt)
        
        return jsonify({
            'response': response.text
        })

    except Exception as e:
        print(f"Chat Error: {e}")
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=False, port=5001)
