import pickle
import os
import numpy as np
import pandas as pd

MODEL_PATH = '../models'

def load_models():
    print("Loading models...")
    with open(os.path.join(MODEL_PATH, 'kmeans_model.pkl'), 'rb') as f:
        kmeans = pickle.load(f)
        
    with open(os.path.join(MODEL_PATH, 'scaler.pkl'), 'rb') as f:
        scaler = pickle.load(f)
        
    return kmeans, scaler

def inspect():
    kmeans, scaler = load_models()
    
    print("\n--- Scaler Info ---")
    print(f"Mean: {scaler.mean_}")
    print(f"Scale: {scaler.scale_}")
    
    print("\n--- KMeans Info ---")
    print(f"Cluster Centers Shape: {kmeans.cluster_centers_.shape}")
    print("Cluster Centers:")
    print(kmeans.cluster_centers_)
    
    # Test Points (from debug logs)
    # Profile 1 (Researcher)
    p1 = np.array([-0.49060655, 1.72619125, -1.46637046, -0.32288868, 1.20397073, -0.66477351,
                   -1.52566896, 0.55611978, -1.66348443, 0., 0., 12., 2., 0., 0., 0., 0.])
                   
    # Profile 3 (Entrepreneur)
    p3 = np.array([-0.49060655, -0.03035309, -1.46637046, -0.32288868, -1.27844315, -0.66477351,
                   -1.52566896, -0.1661137, -0.91752729, 1.38675049, 1., 12., 3., 1., 1., 1., 1.])
                   
    points = {'Researcher': p1, 'Entrepreneur': p3}
    
    print("\n--- Distances to Centroids ---")
    for name, p in points.items():
        print(f"\n{name}:")
        dists = kmeans.transform([p])
        print(f"Distances: {dists}")
        print(f"Predicted Cluster: {kmeans.predict([p])[0]}")

if __name__ == "__main__":
    inspect()
