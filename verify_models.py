import pickle
import os
import numpy as np
import pandas as pd
from pytorch_tabnet.pretraining import TabNetPretrainer
import torch

MODEL_PATH = r"c:\Career Path Prediction\models"

def verify():
    print("Loading models...")
    try:
        with open(os.path.join(MODEL_PATH, 'kmeans_model.pkl'), 'rb') as f:
            kmeans = pickle.load(f)
        with open(os.path.join(MODEL_PATH, 'scaler.pkl'), 'rb') as f:
            scaler = pickle.load(f)
        with open(os.path.join(MODEL_PATH, 'label_encoders.pkl'), 'rb') as f:
            encoders = pickle.load(f)
        with open(os.path.join(MODEL_PATH, 'cluster_info.pkl'), 'rb') as f:
            info = pickle.load(f)
            
        tabnet = TabNetPretrainer()
        tabnet.load_model(os.path.join(MODEL_PATH, 'tabnet_model.zip'))
        print("✅ Models loaded.")
        
        # Create dummy input
        # We need to match the feature columns used in training
        # NUMERICAL_COLS + CATEGORICAL_COLS
        # 10 Numerical + 7 Categorical = 17 features
        
        # Dummy data (already scaled/encoded assumption for simplicity, or raw?)
        # The app does preprocessing. Let's try to pass raw-ish data but manually preprocessed
        # or just random noise of correct shape to test pipeline.
        
        # TabNet expects 2D array
        X_dummy = np.random.randn(1, 17)
        
        print("Predicting with TabNet...")
        
        # Robust embedding extraction
        embeddings = None
        try:
            res = tabnet.predict_latent(X_dummy)
            if isinstance(res, tuple):
                if len(res) >= 2: embeddings = res[1]
                elif len(res) == 1: embeddings = res[0]
            else:
                embeddings = res
        except Exception as e:
            print(f"predict_latent failed: {e}")
            
        if embeddings is None:
            try:
                device = tabnet.device
                tabnet.network.eval()
                with torch.no_grad():
                    X_tensor = torch.from_numpy(X_dummy).float().to(device)
                    res = tabnet.network(X_tensor)
                    if isinstance(res, tuple):
                        if len(res) >= 2: embeddings = res[1].cpu().numpy()
                        else: embeddings = res[0].cpu().numpy()
                    else:
                        embeddings = res.cpu().numpy()
            except Exception as e:
                print(f"Direct network failed: {e}")
                
        if embeddings is None:
            print("❌ Failed to get embeddings")
            return

        print(f"Embeddings shape: {embeddings.shape}")
        
        cluster = kmeans.predict(embeddings)
        print(f"Predicted Cluster: {cluster[0]}")
        
        c_info = info.get(cluster[0], {})
        print(f"Cluster Info: {c_info}")
        
        print("✅ Verification Successful!")
            

    except Exception as e:
        print(f"❌ Verification failed: {e}")

if __name__ == "__main__":
    verify()
