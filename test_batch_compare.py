import requests
import pandas as pd
import io

# Create dummy data
data = {
    'USN': ['1', '2', '3'],
    'Profile_Name': ['Data Scientist', 'Web Developer', 'AI Specialist']
}
df_pred = pd.DataFrame(data)

data_truth = {
    'USN': ['1', '2', '3'],
    'Actual_Role': ['Data Scientist', 'Web Developer', 'Web Developer'] # 1 mismatch
}
df_truth = pd.DataFrame(data_truth)

# Save to bytes
pred_io = io.BytesIO()
df_pred.to_excel(pred_io, index=False)
pred_io.seek(0)

truth_io = io.BytesIO()
df_truth.to_excel(truth_io, index=False)
truth_io.seek(0)

# Send request
url = 'http://localhost:5001/predict/batch-compare'
files = {
    'predicted_file': ('pred.xlsx', pred_io.getvalue(), 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'),
    'truth_file': ('truth.xlsx', truth_io.getvalue(), 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
}

try:
    print("Sending batch compare request...")
    response = requests.post(url, files=files)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"Request Error: {e}")
