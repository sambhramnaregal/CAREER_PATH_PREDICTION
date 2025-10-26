"""
Create a sample Excel template for batch prediction
This helps users understand the required format
"""
import pandas as pd

# Create sample data with correct column names
sample_data = {
    'Name': ['Student_1', 'Student_2', 'Student_3'],
    'USN': ['1RV21CS001', '1RV21CS002', '1RV21CS003'],
    'Gender': ['Male', 'Female', 'Male'],
    'Age': [22, 21, 23],
    'CGPA': [8.5, 7.8, 9.0],
    'Branch_Department': ['CSE', 'ISE', 'AIML'],
    'Number_of_Backlogs': [0, 1, 0],
    'Number_of_Internships': [2, 1, 3],
    'Type_of_Internships': ['Corporate', 'Research', 'Corporate'],
    'Number_of_Publications': [0, 1, 2],
    'Number_of_Projects': [3, 2, 4],
    'Number_of_Certification_Courses': [5, 3, 4],
    'Technical_Skills_Score': [4, 3, 5],
    'Number_of_Hackathons': [2, 1, 3],
    'Soft_Skills_Score': [4, 4, 3],
    'Co_curricular_Activities': ['Yes', 'Yes', 'No'],
    'Leadership_Roles': ['Yes', 'No', 'Yes'],
    'Entrepreneur_Cell_Member': ['No', 'No', 'Yes'],
    'Family_Business_Background': ['No', 'No', 'No']
}

# Create DataFrame
df = pd.DataFrame(sample_data)

# Save to Excel
output_file = 'sample_batch_template.xlsx'
df.to_excel(output_file, index=False, sheet_name='Student Data')

print(f"✅ Sample Excel template created: {output_file}")
print("\n📋 Column descriptions:")
print("- Name: Student name")
print("- USN: University Seat Number")
print("- Gender: Male/Female")
print("- Age: Student age (18-30)")
print("- CGPA: Cumulative GPA (0-10)")
print("- Branch_Department: Engineering branch")
print("- Number_of_Backlogs: Count of backlogs")
print("- Number_of_Internships: Count of internships")
print("- Type_of_Internships: Research/Corporate/Startup/Other")
print("- Number_of_Publications: Research papers published")
print("- Number_of_Projects: Count of projects")
print("- Number_of_Certification_Courses: Count of certifications")
print("- Technical_Skills_Score: Rating 1-5 (1=Poor, 5=Excellent)")
print("- Number_of_Hackathons: Count of hackathons")
print("- Soft_Skills_Score: Rating 1-5 (1=Poor, 5=Excellent)")
print("- Co_curricular_Activities: Yes/No")
print("- Leadership_Roles: Yes/No")
print("- Entrepreneur_Cell_Member: Yes/No")
print("- Family_Business_Background: Yes/No")
print("\n⚠️  Do NOT include 'Status_after_Graduation' column!")
print("    This column will be predicted by the ML model.")
