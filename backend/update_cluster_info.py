import pickle
import os

MODEL_PATH = r'c:\Career Path Prediction\models'
cluster_path = os.path.join(MODEL_PATH, 'cluster_info.pkl')

default_updates = {
    3: {
        'name': 'Technical Specialist',
        'roles': ['DevOps Engineer', 'Cloud Architect', 'Cybersecurity Specialist'],
        'description': 'Focuses on specialized technical infrastructure and security.'
    },
    4: {
        'name': 'Research Innovator',
        'roles': ['R&D Scientist', 'AI Researcher', 'Data Scientist'],
        'description': 'Driven by innovation and deep technical research.'
    }
}

try:
    if os.path.exists(cluster_path):
        with open(cluster_path, 'rb') as f:
            cluster_info = pickle.load(f)
        print("Loaded existing cluster_info.")
    else:
        cluster_info = {}
        print("Created new cluster_info.")

    # Update missing keys
    for k, v in default_updates.items():
        if k not in cluster_info:
            print(f"Adding missing cluster {k}...")
            cluster_info[k] = v
        else:
            print(f"Cluster {k} already exists. Skipping.")

    # Save back
    with open(cluster_path, 'wb') as f:
        pickle.dump(cluster_info, f)
    
    print("cluster_info.pkl updated successfully!")

except Exception as e:
    print(f"Error updating cluster_info: {e}")
