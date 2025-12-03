import pandas as pd
try:
    df = pd.read_excel(r"C:\Users\sambh\Downloads\unseen_student_datan.xlsx")
    with open("columns.txt", "w") as f:
        for col in df.columns:
            f.write(repr(col) + "\n")
except Exception as e:
    print(e)
