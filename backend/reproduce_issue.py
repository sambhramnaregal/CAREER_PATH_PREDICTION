import requests
import json

url = 'http://localhost:5001/predict/individual'
data = {
    "age": "22",
    "cgpa": "8.5",
    "backlogs": "0",
    "internships": "1",
    "research_papers": "0",
    "projects": "2",
    "certifications": "1",
    "technical_skills": "4",
    "hackathons": "1",
    "soft_skills": "4",
    "gender": "Male",
    "branch": "CSE",
    "internship_type": "Web Development",
    "cocurricular": "Yes",
    "leadership": "Yes",
    "entrepreneur_cell": "No",
    "family_business": "No"
}

try:
    print(f"Sending request to {url}...")
    response = requests.post(url, json=data)
    print(f"Status Code: {response.status_code}")
    print("Response:", response.text)
except Exception as e:
    print(f"Request failed: {e}")
