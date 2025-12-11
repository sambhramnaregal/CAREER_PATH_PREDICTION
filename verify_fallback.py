import requests
import pandas as pd
import io

# Create dummy data WITHOUT USN to force fallback
df_pred = pd.DataFrame({
    'Name': ['Alice', 'Bob'],
    'Profile': ['Data Scientist', 'Web Developer']
})

df_truth = pd.DataFrame({
    'Name': ['Alice', 'Bob'],
    'Profile': ['Data Scientist', 'AI Specialist']
})

pred_io = io.BytesIO()
df_pred.to_excel(pred_io, index=False)
pred_io.seek(0)

truth_io = io.BytesIO()
df_truth.to_excel(truth_io, index=False)
truth_io.seek(0)

url = 'http://localhost:5001/predict/batch-compare'
files = {
    'predicted_file': ('pred.xlsx', pred_io.getvalue(), 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'),
    'truth_file': ('truth.xlsx', truth_io.getvalue(), 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
}

try:
    print("Testing fallback alignment with duplicate column names...")
    response = requests.post(url, files=files)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"Error: {e}")
