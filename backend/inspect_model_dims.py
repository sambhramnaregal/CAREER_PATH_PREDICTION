import pickle
import os
import numpy as np

MODEL_PATH = '../models'

def inspect_models():
    with open("inspect_models.log", "w") as log:
        def log_print(msg):
            print(msg)
            log.write(msg + "\n")
            
        try:
            with open(os.path.join(MODEL_PATH, 'pca.pkl'), 'rb') as f:
                pca_model = pickle.load(f)
            
            log_print(f"PCA Model - Expected Features: {getattr(pca_model, 'n_features_in_', 'Unknown')}")
            if hasattr(pca_model, 'feature_names_in_'):
                log_print(f"PCA Model - Feature Names: {pca_model.feature_names_in_}")
            
        except Exception as e:
            log_print(f"Error inspecting PCA model: {e}")

        try:
            with open(os.path.join(MODEL_PATH, 'scaler.pkl'), 'rb') as f:
                scaler = pickle.load(f)
            
            log_print(f"Scaler - Expected Features: {getattr(scaler, 'n_features_in_', 'Unknown')}")
            if hasattr(scaler, 'feature_names_in_'):
                log_print(f"Scaler - Feature Names: {scaler.feature_names_in_}")
                
        except Exception as e:
            log_print(f"Error inspecting Scaler: {e}")

        try:
            with open(os.path.join(MODEL_PATH, 'kmeans_model.pkl'), 'rb') as f:
                kmeans = pickle.load(f)
            
            log_print(f"KMeans Type: {type(kmeans)}")
            if hasattr(kmeans, 'steps'):
                log_print("KMeans is a Pipeline. Steps:")
                for name, step in kmeans.steps:
                    log_print(f"  Step {name}: {type(step)}")
                    if hasattr(step, 'n_features_in_'):
                        log_print(f"    Expected Features: {step.n_features_in_}")
                    if hasattr(step, 'n_components'):
                        log_print(f"    Components: {step.n_components}")
            
            log_print(f"KMeans - Expected Features (Root): {getattr(kmeans, 'n_features_in_', 'Unknown')}")
            if hasattr(kmeans, 'feature_names_in_'):
                log_print(f"KMeans - Feature Names: {kmeans.feature_names_in_}")
                
        except Exception as e:
            log_print(f"Error inspecting KMeans: {e}")

if __name__ == "__main__":
    inspect_models()
