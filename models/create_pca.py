import pandas as pd
import pickle
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

print("Loading dataset...")

df = pd.read_excel("unseen_student_datan.xlsx")

# Columns used during preprocessing
NUMERICAL_COLS = [
    'Age', 'CGPA', 'Number_of_Backlogs', 'Number_of_Internships',
    'Number_of_Publications', 'Number_of_Projects',
    'Number_of_Certification_Courses', 'Technical_Skills_Score',
    'Number_of_Hackathons', 'Soft_Skills_Score'
]

# Select only numerical features
df = df[NUMERICAL_COLS]

print("Scaling...")

# Fit scaler on training dataset
scaler = StandardScaler().fit(df)
X_scaled = scaler.transform(df)

print("Training PCA model...")

# Use 8 components (same as earlier assumption)
pca_model = PCA(n_components=8)
pca_model.fit(X_scaled)

print("Saving PCA model and scaler...")

# Store PCA
pickle.dump(pca_model, open("pca.pkl", "wb"))

# Store scaler (new one that matches PCA)
pickle.dump(scaler, open("scaler.pkl", "wb"))

print("🎉 pca.pkl and scaler.pkl created successfully!")
