# API Calculator - Updated with Research Work

## ✅ New Calculation (Out of 10 Points)

| Component | Weight | Max Points | Calculation |
|-----------|--------|------------|-------------|
| **CGPA** | 20% | **2 points** | (CGPA/10) × 2 |
| **Internships** | 40% | **4 points** | Paid×2 + Unpaid×1 |
| **Research Work** | 20% | **2 points** | Papers × 0.5 |
| **Certifications** | 20% | **2 points** | Certificates × 0.1 |
| **TOTAL** | 100% | **10 points** | Sum of all |

## 📊 Changes Made

### 1. **CGPA Reduced**
   - **Before:** 30% (3 points)
   - **After:** 20% (2 points)
   - Formula: (CGPA/10) × 2

### 2. **Research Work Added** ✨
   - **NEW:** 20% (2 points)
   - 0.5 points per research paper/publication
   - Maximum: 4 papers = 2 points

### 3. **Internships** (unchanged)
   - 40% (4 points)
   - Paid: 2 points each
   - Unpaid: 1 point each

### 4. **Certifications** (unchanged)
   - 20% (2 points)
   - 0.1 points per certification

## 🎯 New Feedback Thresholds

| Score Range | Rating | Feedback |
|------------|--------|----------|
| ≥ 8.5 | **Excellent** | Well-prepared for placements or higher studies |
| 7.0 - 8.4 | **Good** | Keep boosting your experience and skillset |
| 5.0 - 6.9 | **Fair** | Focus on internships, research, and certifications |
| < 5.0 | **Needs Work** | Work on all areas: academics, experience, research |

## 💡 Example Calculation

**Student Profile:**
- CGPA: 9.5/10
- Paid Internships: 2
- Unpaid Internships: 1
- Research Papers: 3
- Certifications: 10

**Calculation:**
```
CGPA:          (9.5/10) × 2 = 1.90 points
Internships:   (2×2 + 1×1) = 5 → capped at 4.00 points
Research:      3 × 0.5 = 1.50 points
Certifications: 10 × 0.1 = 1.00 points
────────────────────────────────────────
TOTAL:                     8.40 / 10 ✅ Good!
```

## 📝 Form Fields

The API Calculator now has **5 input fields:**

1. **CGPA** (0-10)
2. **Paid Internships** (0-5)
3. **Unpaid Internships** (0-5)
4. **Research Papers / Publications** (0-10)
5. **Certifications Completed** (0-20)

## 🎨 Visual Updates

### Score Breakdown Display:
```
CGPA (20%)                    1.90 / 2
Academic performance
[███████████████████░] 95%

Internships (40%)             4.00 / 4
Work experience
[████████████████████] 100%

Research Work (20%)           1.50 / 2
Publications & papers
[███████████████░░░░] 75%

Certifications (20%)          1.00 / 2
Skills & courses
[██████████░░░░░░░░░] 50%
```

### Pie Chart:
- 4 slices now (was 3)
- Blue: CGPA
- Green: Internships
- Purple: Research Work ✨
- Orange: Certifications

## 🚀 To Apply Changes

**Restart Flask backend:**
```powershell
cd "C:\Career Path Prediction\backend"
python app.py
```

**Refresh browser** and go to API Calculator page.

## 📌 Key Points

1. **Total remains 10 points** (easier to understand)
2. **Research work recognized** (important for higher studies)
3. **CGPA reduced** (not the only factor)
4. **Balanced scoring** across 4 key areas
5. **Clear visual breakdown** with percentages

## 🎓 Why Research Work Matters

Including research work (20% weightage) is important because:
- Shows academic depth and curiosity
- Critical for students pursuing higher studies
- Demonstrates analytical and writing skills
- Publications add significant value to profile
- Balanced against practical experience (internships)

---

**Total Calculation:** CGPA (20%) + Internships (40%) + Research (20%) + Certifications (20%) = **100%** (10 points)
