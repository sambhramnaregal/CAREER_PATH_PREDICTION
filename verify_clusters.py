import pickle
import os
import pprint

MODEL_PATH = 'models'

try:
    with open(os.path.join(MODEL_PATH, 'kmeans_model.pkl'), 'rb') as f:
        kmeans = pickle.load(f)
    n_clusters = kmeans.n_clusters
except Exception as e:
    n_clusters = f"Error: {e}"

try:
    with open(os.path.join(MODEL_PATH, 'cluster_info.pkl'), 'rb') as f:
        info = pickle.load(f)
except Exception as e:
    info = f"Error: {e}"

with open("cluster_details.txt", "w") as f:
    f.write(f"KMeans n_clusters: {n_clusters}\n")
    f.write("Cluster Info Content:\n")
    f.write(pprint.pformat(info))
