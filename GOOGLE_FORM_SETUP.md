# Google Form Setup Instructions for Batch Prediction

## Steps to Create the Form

1. Go to [Google Forms](https://forms.google.com/)
2. Click "+ Blank" to create a new form
3. Title: **Student Career Path Prediction Data Collection**
4. Description: *Please fill out this form accurately. Your responses will be used for career path prediction analysis.*

## Form Questions (Copy these exactly)

### Question 1: Name
- **Type:** Short answer
- **Required:** Yes

### Question 2: USN
- **Type:** Short answer
- **Required:** Yes

### Question 3: Gender
- **Type:** Multiple choice
- **Required:** Yes
- **Options:**
  - Male
  - Female

### Question 4: Age
- **Type:** Short answer
- **Required:** Yes
- **Validation:** Number, Greater than 15, Less than 50

### Question 5: CGPA (Average of all Semesters)
- **Type:** Short answer
- **Required:** Yes
- **Validation:** Number, Greater than or equal to 0, Less than or equal to 10
- **Description:** Enter CGPA on a scale of 0-10

### Question 6: Branch/Department
- **Type:** Dropdown
- **Required:** Yes
- **Options:**
  - CSE
  - ISE
  - AIML
  - CSDS
  - CSD
  - CSBS
  - CSCY
  - CS IOT
  - ECE
  - MECHANICAL
  - CIVIL
  - EEE
  - CHEMICAL
  - AUTOMOBILE
  - AERONAUTICAL
  - AI and ROBOTICS
  - EIE
  - ETE
  - Medical Electronics
  - Bio Technology
  - Other

### Question 7: Number of Backlogs
- **Type:** Short answer
- **Required:** Yes
- **Validation:** Number, Greater than or equal to 0

### Question 8: Number of internships
- **Type:** Short answer
- **Required:** Yes
- **Validation:** Number, Greater than or equal to 0

### Question 9: Type of Internships (Research, Corporate, Startup)
- **Type:** Checkboxes
- **Required:** Yes
- **Options:**
  - Research
  - Corporate
  - Startup
  - Other

### Question 10: Number of research papers published / Publications
- **Type:** Short answer
- **Required:** Yes
- **Validation:** Number, Greater than or equal to 0

### Question 11: Number of Projects
- **Type:** Short answer
- **Required:** Yes
- **Validation:** Number, Greater than or equal to 0

### Question 12: Number of Certification Courses
- **Type:** Short answer
- **Required:** Yes
- **Validation:** Number, Greater than or equal to 0

### Question 13: Technical skills (scale of 1 to 5)
- **Type:** Multiple choice
- **Required:** Yes
- **Description:** 1-Poor to 5-Excellent
- **Options:**
  - 1
  - 2
  - 3
  - 4
  - 5

### Question 14: Number of Hackathons Participated
- **Type:** Short answer
- **Required:** Yes
- **Validation:** Number, Greater than or equal to 0

### Question 15: Soft skills level (scale of 1 to 5)
- **Type:** Multiple choice
- **Required:** Yes
- **Description:** 1-Poor to 5-Excellent
- **Options:**
  - 1
  - 2
  - 3
  - 4
  - 5

### Question 16: Co-curricular & Extra-curricular Activities
- **Type:** Multiple choice
- **Required:** Yes
- **Options:**
  - Yes
  - No

### Question 17: Leadership Roles
- **Type:** Multiple choice
- **Required:** Yes
- **Options:**
  - Yes
  - No

### Question 18: Entrepreneur Cell Member (Ex: IEDC)
- **Type:** Multiple choice
- **Required:** Yes
- **Options:**
  - Yes
  - No

### Question 19: Family Business Background
- **Type:** Multiple choice
- **Required:** Yes
- **Options:**
  - Yes
  - No

---

## After Creating the Form

1. Click **Send** button (top right)
2. Copy the form link
3. Share with students

## Downloading Responses as Excel

1. Go to **Responses** tab in your Google Form
2. Click the green **Excel icon** (📊) at the top right
3. This will create a Google Sheet with all responses
4. In Google Sheets, go to **File → Download → Microsoft Excel (.xlsx)**
5. Upload this Excel file to the Career Path Prediction system

## Important Column Name Mapping

The downloaded Excel will have column names based on your questions. You'll need to rename them to match the system requirements:

| Google Form Column | Required System Column Name |
|-------------------|----------------------------|
| Name | Name |
| USN | USN |
| Gender | Gender |
| Age | Age |
| CGPA (Average of all Semesters) | CGPA |
| Branch/Department | Branch_Department |
| Number of Backlogs | Number_of_Backlogs |
| Number of internships | Number_of_Internships |
| Type of Internships... | Type_of_Internships |
| Number of research papers... | Number_of_Publications |
| Number of Projects | Number_of_Projects |
| Number of Certification Courses | Number_of_Certification_Courses |
| Technical skills... | Technical_Skills_Score |
| Number of Hackathons... | Number_of_Hackathons |
| Soft skills level... | Soft_Skills_Score |
| Co-curricular & Extra-curricular... | Co_curricular_Activities |
| Leadership Roles | Leadership_Roles |
| Entrepreneur Cell Member... | Entrepreneur_Cell_Member |
| Family Business Background | Family_Business_Background |

### Quick Column Rename Script (Optional)

After downloading, you can use this Python script to automatically rename columns:

```python
import pandas as pd

# Load the downloaded Excel file
df = pd.read_excel('downloaded_responses.xlsx')

# Rename columns
column_mapping = {
    'Timestamp': 'Timestamp',  # Keep timestamp if present
    'Name': 'Name',
    'USN': 'USN',
    'Gender': 'Gender',
    'Age': 'Age',
    'CGPA (Average of all Semesters)': 'CGPA',
    'Branch/Department': 'Branch_Department',
    'Number of Backlogs': 'Number_of_Backlogs',
    'Number of internships': 'Number_of_Internships',
    'Type of Internships (Research, Corporate, Startup)': 'Type_of_Internships',
    'Number of research papers published / Publications': 'Number_of_Publications',
    'Number of Projects': 'Number_of_Projects',
    'Number of Certification Courses': 'Number_of_Certification_Courses',
    'Technical skills (scale of 1 to 5)': 'Technical_Skills_Score',
    'Number of Hackathons Participated': 'Number_of_Hackathons',
    'Soft skills level (scale of 1 to 5)': 'Soft_Skills_Score',
    'Co-curricular & Extra-curricular Activities': 'Co_curricular_Activities',
    'Leadership Roles': 'Leadership_Roles',
    'Entrepreneur Cell Member (Ex: IEDC)': 'Entrepreneur_Cell_Member',
    'Family Business Background': 'Family_Business_Background'
}

df = df.rename(columns=column_mapping)

# Remove Timestamp column if present
if 'Timestamp' in df.columns:
    df = df.drop('Timestamp', axis=1)

# Save the processed file
df.to_excel('student_data_for_prediction.xlsx', index=False)
print("File processed successfully!")
```

---

## Update the Frontend Code

After creating your Google Form, update the link in:
**File:** `frontend/src/pages/BatchPrediction.js`

Find this line:
```javascript
const GOOGLE_FORM_LINK = 'YOUR_GOOGLE_FORM_LINK_HERE';
```

Replace with your actual Google Form link:
```javascript
const GOOGLE_FORM_LINK = 'https://forms.gle/YOUR_ACTUAL_FORM_ID';
```

---

## Testing

1. Fill out the form yourself with test data
2. Download the Excel file
3. Rename columns as needed (or use the Python script)
4. Upload to the batch prediction system
5. Verify predictions are generated correctly
