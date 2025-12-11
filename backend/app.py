print("Starting app.py...")
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
import re

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
        },
        'version': 'multi-year-v1'
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
    try:
        df[NUMERICAL_COLS] = scaler.transform(df[NUMERICAL_COLS].values)
    except Exception as e:
        # Fallback if scaler fails (e.g. wrong shape), though it shouldn't if cols match
        print(f"Scaler Error: {e}")
        pass

    # Construct final array (ensure correct column order)
    final_df = df[NUMERICAL_COLS + CATEGORICAL_COLS]
    final_df = final_df.fillna(0)

    return final_df


def process_student_dataframe(df):
    """Core logic to process a dataframe and add predictions"""
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
    
    return df, clusters


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
                df = pd.read_excel(file, engine='openpyxl')
            else:
                return jsonify({'error': 'Invalid file format. Use CSV or Excel'}), 400

            # Process
            df, clusters = process_student_dataframe(df)
            
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


@app.route('/predict/multi-year', methods=['POST'])
def predict_multi_year():
    try:
        years = ['year1', 'year2', 'year3', 'year4']
        results = {}
        combined_stats = {} # Profile -> {year1: count, year2: count...}
        
        # We need at least one file
        if not any(y in request.files for y in years):
             return jsonify({'error': 'No files uploaded. Please upload at least one year file.'}), 400

        # Collect all unique profiles encountered
        all_profiles = set()

        for year in years:
            if year in request.files:
                file = request.files[year]
                if file.filename:
                     # Read
                    if file.filename.endswith('.csv'):
                        df = pd.read_csv(file)
                    elif file.filename.endswith('.xlsx'):
                        df = pd.read_excel(file, engine='openpyxl')
                    else:
                        df = pd.read_excel(file)
                    
                    # Process
                    df, _ = process_student_dataframe(df)
                    
                    # Get Count
                    counts = df['Profile_Name'].value_counts().to_dict()
                    results[year] = counts
                    
                    # Add to set
                    all_profiles.update(counts.keys())
        
        # Prepare Chart Data
        # format: [ { name: "Data Scientist", year1: 10, year2: 5 ... }, ... ]
        chart_data = []
        for profile in sorted(list(all_profiles)):
            row = {'name': profile}
            for year in years: # Ensure all years are present even if 0
                row[year] = results.get(year, {}).get(profile, 0)
            chart_data.append(row)

        return jsonify({
            'success': True,
            'results': results, # raw counts per year
            'chart_data': chart_data
        })

    except Exception as e:
        print(f"Multi-Year Error: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/calculate/api', methods=['POST'])
def calculate_api():
    try:
        data = request.json
        
        # Extract inputs
        cgpa = float(data.get('cgpa', 0))
        paid_intern = int(data.get('paid_internships', 0))
        unpaid_intern = int(data.get('unpaid_internships', 0))
        research = int(data.get('research_papers', 0))
        certs = int(data.get('certificates', 0))
        
        # Calculate Points
        # 1. CGPA (Max 2.0) - Weight 20%
        # Assumption: CGPA is scaled to 2.0. If CGPA is 10, points = 2.0
        cgpa_points = min(2.0, (cgpa / 10.0) * 2.0)
        
        # 2. Internships (Max 4.0) - Weight 40%
        # Paid = 2 pts, Unpaid = 1 pt
        intern_raw = (paid_intern * 2.0) + (unpaid_intern * 1.0)
        intern_points = min(4.0, intern_raw)
        
        # 3. Research (Max 2.0) - Weight 20%
        # 0.5 pts each
        research_points = min(2.0, research * 0.5)
        
        # 4. Certificates (Max 2.0) - Weight 20%
        # 0.1 pts each
        cert_points = min(2.0, certs * 0.1)
        
        # Total
        total_score = round(cgpa_points + intern_points + research_points + cert_points, 2)
        
        # Determine Level
        if total_score >= 9.0:
            level = 'excellent'
            feedback = "Outstanding profile! You have a competitive edge for top-tier roles and research positions."
        elif total_score >= 7.0:
            level = 'good'
            feedback = "Strong profile. You are well-prepared, but a few more projects or publications could boost your standing."
        elif total_score >= 5.0:
            level = 'fair'
            feedback = "Decent start. Focus on gaining more practical experience (internships) and improving academic performance."
        else:
            level = 'needs_improvement'
            feedback = "Needs improvement. Prioritize improving your CGPA and actively seeking internships or skill certifications."

        return jsonify({
            'success': True,
            'total_score': total_score,
            'max_score': 10.0,
            'level': level,
            'feedback': feedback,
            'breakdown': {
                'cgpa_points': round(cgpa_points, 2),
                'internship_points': round(intern_points, 2),
                'research_points': round(research_points, 2),
                'cert_points': round(cert_points, 2)
            }
        })

    except Exception as e:
        print(f"API Calc Error: {e}")
        return jsonify({'error': str(e)}), 500



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


@app.route('/predict/batch-compare', methods=['POST'])
def predict_batch_compare():
    try:
        if 'predicted_file' not in request.files or 'truth_file' not in request.files:
            return jsonify({'error': 'Both predicted_file and truth_file are required'}), 400

        pred_file = request.files['predicted_file']
        truth_file = request.files['truth_file']

        if pred_file.filename == '' or truth_file.filename == '':
            return jsonify({'error': 'No selected file'}), 400

        # Read files
        def read_df(f):
            if f.filename.endswith('.csv'):
                return pd.read_csv(f)
            elif f.filename.endswith('.xlsx'):
                return pd.read_excel(f, engine='openpyxl')
            else:
                return pd.read_excel(f)

        df_pred = read_df(pred_file)
        df_truth = read_df(truth_file)

        # Remove duplicate columns if any
        df_pred = df_pred.loc[:, ~df_pred.columns.duplicated()]
        df_truth = df_truth.loc[:, ~df_truth.columns.duplicated()]

        # 1. Align Data
        # Try to merge on USN if available (case insensitive check)
        pred_cols = {c.lower(): c for c in df_pred.columns}
        truth_cols = {c.lower(): c for c in df_truth.columns}
        
        usn_col_pred = pred_cols.get('usn')
        usn_col_truth = truth_cols.get('usn')

        if usn_col_pred and usn_col_truth:
            # Merge on USN
            # Ensure USNs are strings for reliable merging
            df_pred[usn_col_pred] = df_pred[usn_col_pred].astype(str).str.strip().str.lower()
            df_truth[usn_col_truth] = df_truth[usn_col_truth].astype(str).str.strip().str.lower()
            
            merged = pd.merge(df_pred, df_truth, left_on=usn_col_pred, right_on=usn_col_truth, suffixes=('_pred', '_truth'))
            print(f"Merged {len(merged)} records on USN")
        else:
            # Fallback to index
            print("USN column missing. Falling back to row index alignment.")
            min_len = min(len(df_pred), len(df_truth))
            
            # Ensure index alignment
            d1 = df_pred.iloc[:min_len].reset_index(drop=True)
            d2 = df_truth.iloc[:min_len].reset_index(drop=True)
            
            # Add suffix to truth columns to avoid duplicates
            d2 = d2.add_suffix('_truth')
            
            merged = pd.concat([d1, d2], axis=1)
            # Add suffixes concept manually if needed, but concat(axis=1) keeps original names unless duplicates
            # If duplicates exist, pandas adds suffixes but we need to identify them
            
        # 2. Identify Target Columns (UPDATED: Prioritize Profile_Name)
        
        # Helper to find "Profile_Name" case-insensitively
        def find_profile_col(df):
            for c in df.columns:
                if c.lower() == 'profile_name':
                    return c
            return None

        pred_profile_col = find_profile_col(df_pred)
        truth_profile_col = find_profile_col(df_truth)

        # Fallback Logic if not found
        if not pred_profile_col:
            possible_pred_names = ['Predicted_Profile', 'Cluster_Name', 'Predicted Role']
            for col in df_pred.columns:
                 if any(p in col for p in possible_pred_names):
                     pred_profile_col = col
                     break
        
        if not truth_profile_col:
             possible_truth_keywords = ['status', 'career', 'actual', 'verified', 'role', 'domain']
             for col in df_truth.columns:
                 if any(k in col.lower() for k in possible_truth_keywords):
                     truth_profile_col = col
                     break
             if not truth_profile_col:
                 truth_profile_col = df_truth.columns[-1] # Absolute fallback

        if not pred_profile_col or not truth_profile_col:
              return jsonify({'error': f"Could not identify columns. Found Pred: {pred_profile_col}, Truth: {truth_profile_col}"}), 400

        print(f"Pre-Merge Columns: Pred='{pred_profile_col}', Truth='{truth_profile_col}'")
        
        # Resolve Suffixes
        # If columns have same name, pandas adds suffixes
        if pred_profile_col == truth_profile_col:
            pred_target = f"{pred_profile_col}_pred"
            truth_target = f"{truth_profile_col}_truth"
        else:
            # If names are different, they might persist or collide with others?
            # Safest checks:
            pred_target = pred_profile_col
            truth_target = truth_profile_col
             
            # If they collide with other cols, we trust pandas suffixes logic, but here we manually passed suffixes
            # If pred_profile_col was 'Name' and truth had 'Name', they become Name_pred/Name_truth.
            # We need to check if they exist in merged.
            
            # Since we manually handle collisions for specific targets above, let's just dynamic check
            pass

        # ... merge happened before this block, wait. Correct logic: identify -> merge -> resolve.


        pass
        if pred_target not in merged.columns:
            # Maybe suffixed?
            if f"{pred_target}_pred" in merged.columns:
                pred_target = f"{pred_target}_pred"
        
        if truth_target not in merged.columns:
            if f"{truth_target}_truth" in merged.columns:
                truth_target = f"{truth_target}_truth"
                
        # Double check existence
        if pred_target not in merged.columns or truth_target not in merged.columns:
             return jsonify({'error': f"Column resolution failed after merge. Targets: {pred_target}, {truth_target}"}), 400

        if not pred_target or not truth_target:
             return jsonify({'error': f"Could not identify columns. Found Pred: {pred_target}, Truth: {truth_target}"}), 400

        print(f"Comparing Pred: {pred_target} vs Truth: {truth_target}")

        # 3. Calculate Accuracy
        def clean_label(val):
            val = str(val).lower().strip()
            # Remove "cluster X" or "profile X" prefix (e.g. "Cluster 0: Technical")
            val = re.sub(r'^(cluster|profile)\s*\d+\s*[:\-]?\s*', '', val)
            # Remove extra whitespace
            val = re.sub(r'\s+', ' ', val)
            return val.strip()

        y_pred = merged[pred_target].apply(clean_label)
        y_true = merged[truth_target].apply(clean_label)
        
        # Clean up labels (remove "cluster X" prefixes if they exist in one but not other? 
        # For now assume mostly direct string match)
        
        total = len(merged)
        matches = (y_pred == y_true)
        correct_count = matches.sum()
        accuracy = (correct_count / total) * 100 if total > 0 else 0
        
        # 4. Generate Confusion Matrix Data
        # We need unique labels from both
        labels = sorted(list(set(y_pred.unique()) | set(y_true.unique())))
        
        cm_data = []
        for actual in labels:
            row = {'name': actual} # The actual label
            # Get subset where truth is this label
            subset = merged[y_true == actual]
            row['total'] = len(subset)
            
            # Count predictions for this actual label
            # e.g. { "Data Scientist": 10, "Web Dev": 2 }
            pred_counts = subset[pred_target].astype(str).str.lower().str.strip().value_counts()
            
            for predicted_label, count in pred_counts.items():
                row[predicted_label] = int(count)
                
            cm_data.append(row)

        return jsonify({
            'success': True,
            'accuracy': round(accuracy, 2),
            'correct': int(correct_count),
            'total': int(total),
            'pred_column': pred_target,
            'truth_column': truth_target,
            'matrix_data': cm_data,
            'labels': labels
        })

    except Exception as e:
        print(f"Compare Error: {e}")
        return jsonify({'error': f"Comparison failed: {str(e)}"}), 500


if __name__ == '__main__':
    app.run(debug=False, port=5001)
#cd frontend
#npm start

#cd backend
#python app.py