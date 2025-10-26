"""
Train Career Path Prediction Model using real synthetic data
This creates models with all 3 classes: Higher Studies, Placement, Startup
"""
import pandas as pd
import numpy as np
import pickle
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix

# Load the CSV data
csv_path = r"C:\Users\sambh\Downloads\student_career_path_synthetic.csv"
print(f"📂 Loading data from: {csv_path}")
df = pd.read_csv(csv_path)

print(f"✅ Loaded {len(df)} student records")
print(f"📊 Target distribution:")
print(df['Status_after_Graduation'].value_counts())
print()

# Feature engineering - transform raw CSV columns into ML features
def extract_features(row):
    """Extract 12 ML features from CSV row"""
    
    # Calculate extracurricular score
    extracurricular = 0
    if row['Co_curricular_Activities'] == 'Yes':
        extracurricular += 50
    extracurricular += row['Number_of_Hackathons'] * 8
    extracurricular += row['Number_of_Certification_Courses'] * 3
    extracurricular = min(extracurricular, 100)
    
    # Calculate creativity score
    creativity = 0
    creativity += row['Number_of_Projects'] * 15
    if row['Entrepreneur_Cell_Member'] == 'Yes':
        creativity += 40
    creativity += row['Number_of_Hackathons'] * 5
    creativity = min(creativity, 100)
    
    # Calculate analytics score
    analytics = (row['CGPA'] / 10) * 60
    analytics += row['Number_of_Publications'] * 10
    analytics += row['Technical_Skills_Score'] * 8
    analytics = min(analytics, 100)
    
    # Business interest
    business_interest = 100 if (row['Family_Business_Background'] == 'Yes' or 
                                  row['Entrepreneur_Cell_Member'] == 'Yes') else 50
    
    # Return 12 features
    return [
        row['CGPA'],                                    # 1. CGPA
        row['Technical_Skills_Score'] * 20,             # 2. Technical Skills (scaled to 0-100)
        row['Soft_Skills_Score'] * 20,                  # 3. Communication Skills (scaled to 0-100)
        row['Number_of_Internships'],                   # 4. Internships
        row['Number_of_Projects'],                      # 5. Projects
        extracurricular,                                # 6. Extracurricular (calculated)
        100 if row['Leadership_Roles'] == 'Yes' else 0, # 7. Leadership
        creativity,                                     # 8. Creativity (calculated)
        analytics,                                      # 9. Analytics (calculated)
        row['Number_of_Publications'] * 15,             # 10. Research Interest
        business_interest,                              # 11. Business Interest
        row['Technical_Skills_Score'] * 20              # 12. Technical Interest
    ]

# Extract features for all rows
print("🔄 Extracting features...")
X = []
y = []

for idx, row in df.iterrows():
    features = extract_features(row)
    X.append(features)
    y.append(row['Status_after_Graduation'])

X = np.array(X)
y = np.array(y)

print(f"✅ Feature extraction complete")
print(f"   Features shape: {X.shape}")
print(f"   Targets shape: {y.shape}")
print()

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

print(f"📊 Train/Test Split:")
print(f"   Training samples: {len(X_train)}")
print(f"   Testing samples: {len(X_test)}")
print()

# Create and fit scaler
print("🔄 Scaling features...")
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Train Random Forest Classifier
print("🤖 Training Random Forest model...")
model = RandomForestClassifier(
    n_estimators=200,
    max_depth=15,
    min_samples_split=5,
    min_samples_leaf=2,
    random_state=42,
    n_jobs=-1
)

model.fit(X_train_scaled, y_train)

# Evaluate model
print("✅ Training complete!")
print()

train_score = model.score(X_train_scaled, y_train)
test_score = model.score(X_test_scaled, y_test)

print(f"📈 Model Performance:")
print(f"   Training accuracy: {train_score:.2%}")
print(f"   Testing accuracy: {test_score:.2%}")
print()

# Make predictions
y_pred = model.predict(X_test_scaled)

print("📋 Classification Report:")
print(classification_report(y_test, y_pred))
print()

print("🔢 Confusion Matrix:")
print(confusion_matrix(y_test, y_pred))
print()

# Feature importance
feature_names = [
    'CGPA', 'Technical_Skills', 'Communication_Skills',
    'Internships', 'Projects', 'Extracurricular',
    'Leadership', 'Creativity', 'Analytics',
    'Research_Interest', 'Business_Interest', 'Technical_Interest'
]

print("🎯 Top 5 Most Important Features:")
importances = model.feature_importances_
indices = np.argsort(importances)[::-1][:5]
for i, idx in enumerate(indices, 1):
    print(f"   {i}. {feature_names[idx]}: {importances[idx]:.3f}")
print()

# Save models
print("💾 Saving models...")
with open('career_model.pkl', 'wb') as f:
    pickle.dump(model, f)
    
with open('career_scaler.pkl', 'wb') as f:
    pickle.dump(scaler, f)

print("✅ Models saved successfully!")
print("   - career_model.pkl")
print("   - career_scaler.pkl")
print()

print(f"🎓 Model classes: {model.classes_}")
print(f"📊 Number of features: {scaler.n_features_in_}")
print()

# Test with a sample prediction
print("🧪 Testing sample prediction...")
sample_features = X_test_scaled[0:1]
sample_pred = model.predict(sample_features)[0]
sample_proba = model.predict_proba(sample_features)[0]

print(f"   Predicted: {sample_pred}")
print(f"   Probabilities:")
for class_name, prob in zip(model.classes_, sample_proba):
    print(f"      {class_name}: {prob:.1%}")

print()
print("🎉 All done! Your models are ready to use!")
print("   Restart the Flask backend to load the new models.")
