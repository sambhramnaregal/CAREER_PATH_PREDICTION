import pickle
import os

MODEL_PATH = '../models'

try:
    with open(os.path.join(MODEL_PATH, 'label_encoders.pkl'), 'rb') as f:
        label_encoders = pickle.load(f)
        
    with open('encoder_classes.txt', 'w') as out:
        for col, le in label_encoders.items():
            out.write(f"Column: {col}\n")
            out.write(f"Classes: {le.classes_}\n")
            out.write("-" * 20 + "\n")
            
except Exception as e:
    with open('encoder_classes.txt', 'w') as out:
        out.write(f"Error: {e}")
