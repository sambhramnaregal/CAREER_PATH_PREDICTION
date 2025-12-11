import requests
import pandas as pd
import io

# Create dummy data with duplicate columns
data = {
    'USN': ['1', '2'],
    'Col1': ['A', 'B']
}
df = pd.DataFrame(data)
# Force duplicate column
df['Extra'] = ['X', 'Y']
df.columns = ['USN', 'Col1', 'USN'] # Duplicate USN

pred_io = io.BytesIO()
df.to_excel(pred_io, index=False)
pred_io.seek(0)

# Truth data (normal)
df_truth = pd.DataFrame({
    'USN': ['1', '2'],
    'Actual': ['A', 'B']
})
truth_io = io.BytesIO()
df_truth.to_excel(truth_io, index=False)
truth_io.seek(0)

url = 'http://localhost:5001/predict/batch-compare'
files = {
    'predicted_file': ('pred.xlsx', pred_io.getvalue(), 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'),
    'truth_file': ('truth.xlsx', truth_io.getvalue(), 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
}

try:
    print("Testing duplicate columns...")
    response = requests.post(url, files=files)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"Error: {e}")
