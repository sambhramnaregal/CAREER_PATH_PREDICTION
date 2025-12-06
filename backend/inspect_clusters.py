import pickle
import os

MODEL_PATH = '../models'

try:
    with open(os.path.join(MODEL_PATH, 'cluster_info.pkl'), 'rb') as f:
        cluster_info = pickle.load(f)
        
    with open('cluster_info.txt', 'w') as out:
        for cid, info in cluster_info.items():
            out.write(f"Cluster {cid}: {info.get('name')}\n")
            out.write(f"Roles: {info.get('roles')}\n")
            out.write("-" * 20 + "\n")
            
except Exception as e:
    with open('cluster_info.txt', 'w') as out:
        out.write(f"Error: {e}")
