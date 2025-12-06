import pickle

# Update this dictionary based on your cluster insights
cluster_info = {
    0: {
        "name": "Technical Innovators",
        "roles": ["Software Engineer", "Backend Developer", "AI Engineer"],
        "description": "Strong coding ability, technical inclination and analytical thinking."
    },
    1: {
        "name": "Research & Data Learners",
        "roles": ["Data Analyst", "Research Intern"],
        "description": "Good academic mindset, research interest and analytical thinking."
    },
    2: {
        "name": "Career Growth Oriented Learners",
        "roles": ["Associate Engineer", "Junior Developer"],
        "description": "Growing skillset, quick learning mindset, consistent improvement focus."
    }
}

with open("cluster_info.pkl", "wb") as f:
    pickle.dump(cluster_info, f)

print("cluster_info.pkl created successfully!")
