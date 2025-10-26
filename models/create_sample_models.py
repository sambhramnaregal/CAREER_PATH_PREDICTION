"""
Script to create sample ML models for testing
This should be replaced with your actual trained models
"""
import pickle
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler

# Create sample data
np.random.seed(42)
n_samples = 1000

# Generate synthetic training data
# Features: CGPA, Technical_Skills, Communication_Skills, Internships, Projects, 
#           Extracurricular, Leadership, Creativity, Analytics, Research_Interest, 
#           Business_Interest, Technical_Interest
X = np.random.rand(n_samples, 12) * 100

# Create realistic targets based on feature combinations
y = []
for i in range(n_samples):
    cgpa, tech, comm, intern, proj, extra, lead, creat, anal, research, business, tech_int = X[i]
    
    # Higher Studies: High CGPA + High Research + High Analytics
    higher_studies_score = cgpa * 0.4 + research * 0.3 + anal * 0.3
    
    # Placement: High Tech Skills + High Communication + Internships
    placement_score = tech * 0.3 + comm * 0.3 + intern * 5 + proj * 3
    
    # Startup: High Business + High Leadership + High Creativity
    startup_score = business * 0.4 + lead * 0.3 + creat * 0.3
    
    scores = [higher_studies_score, placement_score, startup_score]
    labels = ['Higher Studies', 'Placement', 'Startup']
    y.append(labels[np.argmax(scores)])

y = np.array(y)

# Train model
model = RandomForestClassifier(n_estimators=100, random_state=42, max_depth=10)
model.fit(X, y)

# Create scaler
scaler = StandardScaler()
scaler.fit(X)

# Save models
with open('career_model.pkl', 'wb') as f:
    pickle.dump(model, f)
    
with open('career_scaler.pkl', 'wb') as f:
    pickle.dump(scaler, f)

print("✅ Sample models created successfully!")
print(f"   - career_model.pkl")
print(f"   - career_scaler.pkl")
print(f"\n📊 Model accuracy: {model.score(X, y):.2%}")
print(f"📋 Classes: {model.classes_}")
print(f"\n⚠️  Note: Replace these with your actual trained models!")
