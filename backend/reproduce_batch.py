import requests
import pandas as pd
import io

url = 'http://localhost:5001/predict/batch'

# Create sample dataframe
data = {
    'Age': [22, 23],
    'CGPA': [8.5, 7.2],
    'Number_of_Backlogs': [0, 1],
    'Number_of_Internships': [1, 0],
    'Number_of_Publications': [0, 0],
    'Number_of_Projects': [2, 1],
    'Number_of_Certification_Courses': [1, 0],
    'Technical_Skills_Score': [4, 3],
    'Number_of_Hackathons': [1, 0],
    'Soft_Skills_Score': [4, 3],
    'Gender': ['Male', 'Female'],
    'Branch_Department': ['CSE', 'ECE'],
    'Type_of_Internships': ['Web Development', 'None'],
    'Co_curricular_Activities': ['Yes', 'No'],
    'Leadership_Roles': ['Yes', 'No'],
    'Entrepreneur_Cell_Member': ['No', 'No'],
    'Family_Business_Background': ['No', 'Yes']
}

df = pd.DataFrame(data)
output = io.BytesIO()
with pd.ExcelWriter(output, engine='openpyxl') as writer:
    df.to_excel(writer, index=False)
output.seek(0)

files = {'file': ('test.xlsx', output, 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')}

try:
    print(f"Sending batch request to {url}...")
    response = requests.post(url, files=files)
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        if data.get('success'):
            print("Success! JSON response matches new format.")
            print("Distribution:", data.get('distribution'))
        else:
            print("Warning: Success flag missing or false", data)
    else:
        print("Response:", response.text)
except Exception as e:
    print(f"Request failed: {e}")
