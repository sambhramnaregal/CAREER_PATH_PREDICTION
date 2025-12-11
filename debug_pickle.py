import pickle
import os

MODEL_PATH = 'models'
try:
    with open(os.path.join(MODEL_PATH, 'cluster_info.pkl'), 'rb') as f:
        cluster_info = pickle.load(f)
        print("Keys:", list(cluster_info.keys()))
        print("Key Type:", type(list(cluster_info.keys())[0]))
except Exception as e:
    print(f"Error: {e}")
