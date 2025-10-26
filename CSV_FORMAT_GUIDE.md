# CSV Format Guide for Batch Prediction

## ✅ Correct Column Names

Your Excel/CSV file **MUST** have these exact column names (case-sensitive):

### Student Information (19 columns)

| Column Name | Description | Valid Values |
|------------|-------------|--------------|
| `Name` | Student name | Any string |
| `USN` | University Seat Number | Any string |
| `Gender` | Student gender | Male, Female |
| `Age` | Student age | 18-30 (number) |
| `CGPA` | Cumulative GPA | 0-10 (decimal) |
| `Branch_Department` | Engineering branch | CSE, ISE, AIML, ECE, etc. |
| `Number_of_Backlogs` | Count of backlogs | 0 or more (number) |
| `Number_of_Internships` | Count of internships | 0 or more (number) |
| `Type_of_Internships` | Internship type | Research, Corporate, Startup, Other |
| `Number_of_Publications` | Research papers | 0 or more (number) |
| `Number_of_Projects` | Count of projects | 0 or more (number) |
| `Number_of_Certification_Courses` | Count of certifications | 0 or more (number) |
| `Technical_Skills_Score` | Technical skills rating | 1-5 (1=Poor, 5=Excellent) |
| `Number_of_Hackathons` | Count of hackathons | 0 or more (number) |
| `Soft_Skills_Score` | Communication skills | 1-5 (1=Poor, 5=Excellent) |
| `Co_curricular_Activities` | Participates in activities | Yes, No |
| `Leadership_Roles` | Has leadership roles | Yes, No |
| `Entrepreneur_Cell_Member` | Member of E-Cell | Yes, No |
| `Family_Business_Background` | Has family business | Yes, No |

## ⚠️ IMPORTANT

**DO NOT include** `Status_after_Graduation` column in your upload file!

This is the **target column** that the ML model will predict. The system will add this column along with probability columns.

## 📊 Example Row

```csv
Name,USN,Gender,Age,CGPA,Branch_Department,Number_of_Backlogs,Number_of_Internships,Type_of_Internships,Number_of_Publications,Number_of_Projects,Number_of_Certification_Courses,Technical_Skills_Score,Number_of_Hackathons,Soft_Skills_Score,Co_curricular_Activities,Leadership_Roles,Entrepreneur_Cell_Member,Family_Business_Background
Student_1,1RV21CS001,Male,22,8.5,CSE,0,2,Corporate,1,3,4,4,2,4,Yes,Yes,No,No
```

## 🔄 How Data is Transformed for ML Model

The system transforms your 19 input columns into 12 ML features:

1. **CGPA** → CGPA (direct)
2. **Technical_Skills_Score** × 20 → Technical_Skills (0-100)
3. **Soft_Skills_Score** × 20 → Communication_Skills (0-100)
4. **Number_of_Internships** → Internships (direct)
5. **Number_of_Projects** → Projects (direct)
6. **Calculated** → Extracurricular (from Co_curricular, Hackathons, Certifications)
7. **Leadership_Roles** → Leadership (Yes=100, No=0)
8. **Calculated** → Creativity (from Projects, Entrepreneur, Hackathons)
9. **Calculated** → Analytics (from CGPA, Publications, Technical Skills)
10. **Number_of_Publications** × 15 → Research_Interest (0-100)
11. **Family_Business/Entrepreneur** → Business_Interest (100 or 50)
12. **Technical_Skills_Score** × 20 → Technical_Interest (0-100)

## 🎯 Output

After prediction, your file will have additional columns:

- `Predicted_Career_Path` - Higher Studies / Placement / Startup
- `Probability_Higher Studies` - Probability (0-1)
- `Probability_Placement` - Probability (0-1)
- `Probability_Startup` - Probability (0-1)

## 📝 Generate Sample Template

Run this command to create a sample Excel template:

```powershell
python create_sample_excel.py
```

This creates `sample_batch_template.xlsx` with the correct format.

## 🧪 Test with Your Dataset

Your file: `C:\Users\sambh\Downloads\student_career_path_synthetic.csv`

✅ This file has the correct format!

To use it for testing:
1. Remove the `Status_after_Graduation` column (or the system will ignore it)
2. Upload the modified file
3. Download predictions

## 🆘 Common Errors

### "Column not found"
- Check column names match exactly (case-sensitive)
- Check for extra spaces in column names
- Use underscore `_` not space

### "Invalid value"
- CGPA must be 0-10
- Skills must be 1-5
- Yes/No values must be exactly "Yes" or "No"

### "Model error"
- Ensure all required columns are present
- Check data types (numbers where expected)
