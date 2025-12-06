import pickle
import os

MODEL_PATH = r'c:\Career Path Prediction\models'
cluster_path = os.path.join(MODEL_PATH, 'cluster_info.pkl')

try:
    with open(cluster_path, 'rb') as f:
        cluster_info = pickle.load(f)
    
    print("Cluster Info Content:")
    for k, v in cluster_info.items():
        print(f"Key: {k} (Type: {type(k)}) -> Name: {v.get('name', 'MISSING')}")

except Exception as e:
    print(f"Error loading cluster_info: {e}")
