import requests
import json

url = 'http://localhost:5001/predict/individual'

profiles = [
    {
        "name": "Researcher",
        "cgpa": 9.5,
        "technical_skills": 4,
        "soft_skills": 3,
        "research_papers": 2,
        "internships": 1,
        "internship_type": "Research",
        "projects": 2,
        "hackathons": 0,
        "cocurricular": "No",
        "leadership": "No",
        "entrepreneur_cell": "No",
        "family_business": "No",
        "gender": "Female",
        "branch": "CSE"
    },
    {
        "name": "Developer",
        "cgpa": 8.0,
        "technical_skills": 5,
        "soft_skills": 3,
        "research_papers": 0,
        "internships": 2,
        "internship_type": "Corporate",
        "projects": 4,
        "hackathons": 3,
        "cocurricular": "No",
        "leadership": "No",
        "entrepreneur_cell": "No",
        "family_business": "No",
        "gender": "Male",
        "branch": "CSE"
    },
    {
        "name": "Entrepreneur",
        "cgpa": 7.0,
        "technical_skills": 3,
        "soft_skills": 5,
        "research_papers": 0,
        "internships": 1,
        "internship_type": "Startup",
        "projects": 2,
        "hackathons": 1,
        "cocurricular": "Yes",
        "leadership": "Yes",
        "entrepreneur_cell": "Yes",
        "family_business": "Yes",
        "gender": "Male",
        "branch": "CSE"
    }
]

for p in profiles:
    print(f"\nTesting profile: {p['name']}")
    try:
        response = requests.post(url, json=p)
        if response.status_code == 200:
            data = response.json()
            print(f"Cluster ID: {data.get('cluster_id')}")
            print(f"Profile Name: {data.get('profile_name')}")
        else:
            print(f"Error: {response.status_code} - {response.text}")
            with open("reproduction_error.txt", "a") as f:
                f.write(f"{p['name']} Error: {response.text}\n")
    except Exception as e:
        print(f"Request failed: {e}")
