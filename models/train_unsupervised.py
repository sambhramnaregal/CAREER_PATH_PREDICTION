import pandas as pd
import numpy as np
import pickle
import os
import google.generativeai as genai
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.mixture import GaussianMixture
from sklearn.metrics import silhouette_score
import json
from dotenv import load_dotenv

load_dotenv() # Load environment variables from .env file

# --- Configuration ---
# GAP FOR INPUT FILE PATH
DATA_PATH = r"C:\Users\sambh\Downloads\student_career_path_synthetic.csv" 
MODEL_DIR = os.path.dirname(os.path.abspath(__file__))
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

def configure_gemini():
    if not GEMINI_API_KEY:
        print("⚠️ Warning: GEMINI_API_KEY not found in environment variables.")
        print("   Cluster naming and roadmap generation will be skipped or use placeholders.")
        return False
    genai.configure(api_key=GEMINI_API_KEY)
    return True

def load_and_preprocess_data(filepath):
    print(f"📂 Loading data from: {filepath}")
    df = pd.read_csv(filepath)
    
    # Feature Extraction (Same as original to maintain consistency)
    # We need to convert raw data into numerical features for clustering
    X = []
    for _, row in df.iterrows():
        # Calculate extracurricular score
        extracurricular = 0
        if row.get('Co_curricular_Activities') == 'Yes': extracurricular += 50
        extracurricular += row.get('Number_of_Hackathons', 0) * 8
        extracurricular += row.get('Number_of_Certification_Courses', 0) * 3
        extracurricular = min(extracurricular, 100)
        
        # Calculate creativity score
        creativity = 0
        creativity += row.get('Number_of_Projects', 0) * 15
        if row.get('Entrepreneur_Cell_Member') == 'Yes': creativity += 40
        creativity += row.get('Number_of_Hackathons', 0) * 5
        creativity = min(creativity, 100)
        
        # Calculate analytics score
        analytics = (row.get('CGPA', 0) / 10) * 60
        analytics += row.get('Number_of_Publications', 0) * 10
        analytics += row.get('Technical_Skills_Score', 0) * 8
        analytics = min(analytics, 100)
        
        # Business interest
        business_interest = 100 if (row.get('Family_Business_Background') == 'Yes' or 
                                      row.get('Entrepreneur_Cell_Member') == 'Yes') else 50

        features = [
            row.get('CGPA', 0),                                    
            row.get('Technical_Skills_Score', 0) * 20,             
            row.get('Soft_Skills_Score', 0) * 20,                  
            row.get('Number_of_Internships', 0),                   
            row.get('Number_of_Projects', 0),                      
            extracurricular,                                
            100 if row.get('Leadership_Roles') == 'Yes' else 0, 
            creativity,                                     
            analytics,                                      
            row.get('Number_of_Publications', 0) * 15,             
            business_interest,                              
            row.get('Technical_Skills_Score', 0) * 20              
        ]
        X.append(features)
    
    return np.array(X), df

def train_unsupervised_models(X):
    print("🔄 Scaling features...")
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # 1. K-Means Clustering
    # We'll try a wider range of k values to find more specific/granular roles
    print("🤖 Training K-Means...")
    best_kmeans = None
    best_score = -1
    
    # Expanded range to capture diverse roles (e.g., AI Engineer, Product Manager, etc.)
    for k in range(5, 15): 
        kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
        labels = kmeans.fit_predict(X_scaled)
        score = silhouette_score(X_scaled, labels)
        print(f"   k={k}: Silhouette Score = {score:.4f}")
        
        if score > best_score:
            best_score = score
            best_kmeans = kmeans
            
    print(f"✅ Best K-Means k={best_kmeans.n_clusters}")

    # 2. Gaussian Mixture Model (Validation)
    print("🤖 Validating with GMM...")
    gmm = GaussianMixture(n_components=best_kmeans.n_clusters, random_state=42)
    gmm.fit(X_scaled)
    gmm_aic = gmm.aic(X_scaled)
    print(f"   GMM AIC: {gmm_aic:.2f}")
    
    return best_kmeans, scaler, X_scaled

def generate_cluster_profiles(kmeans, scaler, X_scaled, feature_names):
    print("📊 Generating Cluster Profiles...")
    profiles = {}
    centers = kmeans.cluster_centers_
    
    # Inverse transform to get original scale values for interpretation
    centers_original = scaler.inverse_transform(centers)
    
    for i in range(len(centers)):
        profile = {name: val for name, val in zip(feature_names, centers_original[i])}
        profiles[i] = profile
        
    return profiles

def name_clusters_with_gemini(profiles):
    print("✨ Naming clusters using Gemini...")
    # Reverting to gemini-pro as per user request/availability
    try:
        model = genai.GenerativeModel('gemini-pro')
    except:
        print("⚠️ gemini-pro not found, trying default")
        model = genai.GenerativeModel('gemini-pro')
    
    cluster_info = {}
    
    for cluster_id, profile in profiles.items():
        prompt = f"""
        Analyze the following average feature values for a group of computer science students:
        {json.dumps(profile, indent=2)}
        
        Based on these characteristics, suggest:
        1. A HIGHLY SPECIFIC "Career Profile Name" (e.g., "AI Research Scientist", "Full Stack Developer", "Product Manager", "Data Analyst", "Cybersecurity Specialist"). Avoid generic names like "Student" or "Techie".
        2. A list of 4-5 specific job roles or opportunities they are best suited for. Include niche roles if applicable.
        3. A brief 1-sentence description of this persona.
        
        Format the output as JSON with keys: "name", "roles" (list), "description".
        """
        
        try:
            response = model.generate_content(prompt)
            # Clean up json string if needed
            text = response.text.replace('```json', '').replace('```', '').strip()
            info = json.loads(text)
            cluster_info[cluster_id] = info
            print(f"   Cluster {cluster_id}: {info['name']}")
        except Exception as e:
            print(f"   ❌ Error naming cluster {cluster_id}: {e}")
            # Improved Fallback - No more "Cluster X"
            # We assign a generic but professional title based on the ID to ensure variety if API fails
            fallback_roles = [
                "Software Development Engineer", "Data Science Professional", 
                "Network & Systems Engineer", "Product Management Associate",
                "Research & Development Specialist"
            ]
            role_name = fallback_roles[cluster_id % len(fallback_roles)]
            
            cluster_info[cluster_id] = {
                "name": role_name,
                "roles": [role_name, "Technical Consultant", "Project Associate"], 
                "description": "A professional profile with strong technical foundations."
            }
            
    return cluster_info

def main():
    has_gemini = configure_gemini()
    
    X, df = load_and_preprocess_data(DATA_PATH)
    
    kmeans, scaler, X_scaled = train_unsupervised_models(X)
    
    feature_names = [
        'CGPA', 'Technical_Skills', 'Communication_Skills', 
        'Internships', 'Projects', 'Extracurricular',
        'Leadership', 'Creativity', 'Analytics', 
        'Research_Interest', 'Business_Interest', 'Technical_Interest'
    ]
    
    profiles = generate_cluster_profiles(kmeans, scaler, X_scaled, feature_names)
    
    cluster_info = {}
    if has_gemini:
        cluster_info = name_clusters_with_gemini(profiles)
    else:
        # Manual fallback if no API key
        print("⚠️ Using default names (No API Key)")
        for i in profiles:
            cluster_info[i] = {
                "name": f"Profile Type {i+1}", 
                "roles": ["Software Engineer", "Data Analyst"], 
                "description": "Auto-generated profile."
            }
            
    # Save everything
    print("💾 Saving models and cluster info...")
    with open(os.path.join(MODEL_DIR, 'kmeans_model.pkl'), 'wb') as f:
        pickle.dump(kmeans, f)
        
    with open(os.path.join(MODEL_DIR, 'scaler.pkl'), 'wb') as f:
        pickle.dump(scaler, f)
        
    with open(os.path.join(MODEL_DIR, 'cluster_info.pkl'), 'wb') as f:
        pickle.dump(cluster_info, f)
        
    print("✅ Done! Models saved to models/ directory.")

if __name__ == "__main__":
    main()
