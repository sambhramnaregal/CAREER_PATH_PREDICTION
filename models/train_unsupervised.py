import pandas as pd
import numpy as np
import pickle
import os
import google.generativeai as genai
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import json
from dotenv import load_dotenv
import torch
from pytorch_tabnet.pretraining import TabNetPretrainer
import hdbscan
import warnings

warnings.filterwarnings("ignore")
load_dotenv()

# --- Configuration ---
DATA_PATH = r"C:\Users\sambh\Downloads\unseen_student_datan.xlsx"
MODEL_DIR = os.path.dirname(os.path.abspath(__file__))
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Define columns based on user request (Mapped to Excel file)
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

def configure_gemini():
    if not GEMINI_API_KEY:
        print("Warning: GEMINI_API_KEY not found.")
        return False
    genai.configure(api_key=GEMINI_API_KEY)
    return True

def load_and_preprocess_data(filepath):
    print(f"Loading data from: {filepath}")
    try:
        df = pd.read_excel(filepath)
    except Exception as e:
        print(f"Error loading Excel: {e}")
        return None, None, None, None

    # Normalize column names
    df.columns = [c.strip() for c in df.columns]
    
    # Handle missing columns or map them if names slightly differ
    # For now, assuming exact matches or close enough to be found manually if needed
    # Let's print columns to be sure during run
    print("Columns found:", df.columns.tolist())

    # Fill missing values
    for col in NUMERICAL_COLS:
        if col in df.columns:
            df[col] = df[col].fillna(df[col].median())
    
    for col in CATEGORICAL_COLS:
        if col in df.columns:
            df[col] = df[col].fillna('Unknown')

    # Encoders
    label_encoders = {}
    for col in CATEGORICAL_COLS:
        if col in df.columns:
            le = LabelEncoder()
            df[col] = le.fit_transform(df[col].astype(str))
            label_encoders[col] = le
            
    # Scaling
    scaler = StandardScaler()
    if all(c in df.columns for c in NUMERICAL_COLS):
        df[NUMERICAL_COLS] = scaler.fit_transform(df[NUMERICAL_COLS])
    else:
        print("Missing some numerical columns!")
        
    # Prepare X for TabNet
    # TabNet expects all features. We'll combine cat and num.
    # For Pretrainer, we usually pass raw features (but numerical scaled is good).
    # Categorical features need to be passed as indices for embeddings if using supervised TabNet,
    # but for Unsupervised Pretraining, it reconstructs the input.
    
    feature_cols = NUMERICAL_COLS + CATEGORICAL_COLS
    X = df[feature_cols].values
    
    return X, df, label_encoders, scaler

def train_tabnet(X):
    print("Training TabNet Pretrainer...")
    # TabNet Pretrainer
    unsupervised_model = TabNetPretrainer(
        optimizer_fn=torch.optim.Adam,
        optimizer_params=dict(lr=2e-2),
        mask_type='entmax' # "sparsemax"
    )
    
    unsupervised_model.fit(
        X_train=X,
        eval_set=[X],
        pretraining_ratio=0.8,
        max_epochs=100, # Adjust based on time/performance
        patience=10,
        batch_size=256, 
        virtual_batch_size=128,
        num_workers=0,
        drop_last=False
    )
    
    return unsupervised_model

def get_embeddings(model, X):
    print("Extracting Embeddings...")
    # Get latent embeddings from the model
    # predict_latent returns (output, embedded_x) - we want the latent representation
    # Actually for TabNetPretrainer, predict returns the reconstruction.
    # We need to hook into the network to get embeddings or use the encoder.
    # The `predict` method of Pretrainer returns the reconstructed output.
    # To get embeddings, we can use `predict_latent` if available or access the network.
    
    try:
        res = model.predict_latent(X)
        print(f"predict_latent res type: {type(res)}")
        if isinstance(res, tuple): 
            print(f"len: {len(res)}")
            # If tuple, assume embedding is the second element (standard) or last?
            # TabNetPretrainer: (output, latent)
            if len(res) >= 2:
                return res[1]
            elif len(res) == 1:
                return res[0]
        return res
    except Exception as e:
        print(f"predict_latent failed: {e}")
        
    # Fallback: Access network directly
    try:
        print("Trying direct network access...")
        device = model.device
        model.network.eval()
        with torch.no_grad():
            X_tensor = torch.from_numpy(X).float().to(device)
            res = model.network(X_tensor)
            
            if isinstance(res, tuple):
                if len(res) >= 2:
                    return res[1].cpu().numpy()
                return res[0].cpu().numpy()
            return res.cpu().numpy()
    except Exception as e:
        print(f"Direct network access failed: {e}")
        return None

def cluster_embeddings(embeddings):
    print("Clustering Embeddings...")
    
    # 1. HDBSCAN
    print("   Running HDBSCAN...")
    hdb = hdbscan.HDBSCAN(min_cluster_size=5, min_samples=2, metric='euclidean')
    hdb_labels = hdb.fit_predict(embeddings)
    n_hdb = len(set(hdb_labels)) - (1 if -1 in hdb_labels else 0)
    print(f"   HDBSCAN found {n_hdb} clusters (excluding noise).")
    
    if n_hdb > 1:
        sil_hdb = silhouette_score(embeddings, hdb_labels) if len(set(hdb_labels)) > 1 else -1
        print(f"   HDBSCAN Silhouette: {sil_hdb:.4f}")
    
    # 2. KMeans (User requested fixed 5 categories)
    print("   Running KMeans with K=5...")
    best_k = 5
    best_kmeans = KMeans(n_clusters=best_k, random_state=42, n_init=10)
    best_kmeans.fit(embeddings)
            
    return best_kmeans, best_k

def map_clusters_to_categories(kmeans, df_orig):
    print("Mapping clusters to 5 fixed categories...")
    labels = kmeans.labels_
    df_orig['Cluster'] = labels
    
    # Calculate centroids/means for mapping
    cluster_stats = []
    for c_id in range(5):
        cluster_data = df_orig[df_orig['Cluster'] == c_id]
        stats = {
            'id': c_id,
            'cgpa': cluster_data['CGPA'].mean(),
            'tech_score': cluster_data['Technical_Skills_Score'].mean(),
            'projects': cluster_data['Number_of_Projects'].mean(),
            'publications': cluster_data['Number_of_Publications'].mean(),
            'leadership': cluster_data['Leadership_Roles'].apply(lambda x: 1 if x == 'Yes' else 0).mean(),
            'entrepreneur': cluster_data['Entrepreneur_Cell_Member'].apply(lambda x: 1 if x == 'Yes' else 0).mean(),
            'backlogs': cluster_data['Number_of_Backlogs'].mean()
        }
        cluster_stats.append(stats)
        
    # Define Categories
    categories = [
        "Tech-Oriented Dev Track",
        "Research & Higher Studies",
        "Corporate/Management Oriented",
        "Entrepreneurial Track",
        "Low-skill / Needs Intervention"
    ]
    
    # Heuristic Mapping
    # We will assign each cluster to the best fitting category
    # This is a simple greedy assignment or scoring
    
    mapping = {} # cluster_id -> category_name
    assigned_cats = set()
    
    # 1. Low-skill (Highest backlogs or lowest CGPA/Tech)
    low_skill_cluster = max(cluster_stats, key=lambda x: x['backlogs'] - x['cgpa'] - x['tech_score'])
    mapping[low_skill_cluster['id']] = "Low-skill / Needs Intervention"
    assigned_cats.add("Low-skill / Needs Intervention")
    
    remaining_clusters = [c for c in cluster_stats if c['id'] not in mapping]
    
    # 2. Research (Highest Publications + CGPA)
    if remaining_clusters:
        research_cluster = max(remaining_clusters, key=lambda x: x['publications'] * 2 + x['cgpa'])
        mapping[research_cluster['id']] = "Research & Higher Studies"
        assigned_cats.add("Research & Higher Studies")
        remaining_clusters = [c for c in remaining_clusters if c['id'] not in mapping]
        
    # 3. Entrepreneur (Highest Entrepreneurship + Leadership)
    if remaining_clusters:
        ent_cluster = max(remaining_clusters, key=lambda x: x['entrepreneur'] * 3 + x['leadership'])
        mapping[ent_cluster['id']] = "Entrepreneurial Track"
        assigned_cats.add("Entrepreneurial Track")
        remaining_clusters = [c for c in remaining_clusters if c['id'] not in mapping]
        
    # 4. Tech (Highest Tech Score + Projects)
    if remaining_clusters:
        tech_cluster = max(remaining_clusters, key=lambda x: x['tech_score'] * 2 + x['projects'])
        mapping[tech_cluster['id']] = "Tech-Oriented Dev Track"
        assigned_cats.add("Tech-Oriented Dev Track")
        remaining_clusters = [c for c in remaining_clusters if c['id'] not in mapping]
        
    # 5. Corporate (Remaining, usually balanced or high leadership)
    if remaining_clusters:
        corp_cluster = remaining_clusters[0]
        mapping[corp_cluster['id']] = "Corporate/Management Oriented"
        assigned_cats.add("Corporate/Management Oriented")
        
    # Create Cluster Info
    cluster_info = {}
    
    # Predefined roles and descriptions
    category_details = {
        "Tech-Oriented Dev Track": {
            "roles": ["Software Engineer", "Full Stack Developer", "DevOps Engineer", "System Architect"],
            "description": "Strong technical skills and project experience, suitable for core development roles."
        },
        "Research & Higher Studies": {
            "roles": ["Data Scientist", "Research Associate", "PhD Candidate", "R&D Engineer"],
            "description": "High academic performance and research interest, ideal for higher education or R&D."
        },
        "Corporate/Management Oriented": {
            "roles": ["Product Manager", "Business Analyst", "Consultant", "Project Manager"],
            "description": "Balanced profile with leadership qualities, suitable for management and corporate roles."
        },
        "Entrepreneurial Track": {
            "roles": ["Startup Founder", "Product Owner", "Innovation Manager", "Business Development"],
            "description": "High initiative and entrepreneurial spirit, suited for starting or leading new ventures."
        },
        "Low-skill / Needs Intervention": {
            "roles": ["Junior Developer", "IT Support", "QA Tester", "Intern"],
            "description": "Needs to focus on skill development and clearing backlogs to improve career prospects."
        }
    }
    
    for c_id, cat_name in mapping.items():
        details = category_details[cat_name]
        cluster_info[c_id] = {
            "name": cat_name,
            "roles": details["roles"],
            "description": details["description"]
        }
        print(f"   Cluster {c_id} -> {cat_name}")
        
    return cluster_info

def name_clusters(kmeans, df, original_df_path):
    # Wrapper to maintain signature but use new logic
    df_orig = pd.read_excel(original_df_path)
    df_orig.columns = [c.strip() for c in df_orig.columns]
    return map_clusters_to_categories(kmeans, df_orig)

def main():
    configure_gemini()
    
    # 1. Load & Preprocess
    X, df, encoders, scaler = load_and_preprocess_data(DATA_PATH)
    if X is None: return
    
    # 2. Train TabNet
    tabnet = train_tabnet(X)
    
    # 3. Get Embeddings
    embeddings = get_embeddings(tabnet, X)
    if embeddings is None:
        print("Failed to extract embeddings. Exiting.")
        return
    
    # 4. Cluster
    kmeans, best_k = cluster_embeddings(embeddings)
    
    # 5. Name Clusters
    cluster_info = name_clusters(kmeans, df, DATA_PATH)
    
    # 6. Save
    print("Saving artifacts...")
    
    # Save TabNet
    tabnet.save_model(os.path.join(MODEL_DIR, 'tabnet_model'))
    
    # Save KMeans
    with open(os.path.join(MODEL_DIR, 'kmeans_model.pkl'), 'wb') as f:
        pickle.dump(kmeans, f)
        
    # Save Scaler & Encoders
    with open(os.path.join(MODEL_DIR, 'scaler.pkl'), 'wb') as f:
        pickle.dump(scaler, f)
        
    with open(os.path.join(MODEL_DIR, 'label_encoders.pkl'), 'wb') as f:
        pickle.dump(encoders, f)
        
    # Save Cluster Info
    with open(os.path.join(MODEL_DIR, 'cluster_info.pkl'), 'wb') as f:
        pickle.dump(cluster_info, f)
        
    # Save Embeddings (optional, for viz)
    np.save(os.path.join(MODEL_DIR, 'embeddings.npy'), embeddings)
    
    print("Training Complete!")

if __name__ == "__main__":
    main()
