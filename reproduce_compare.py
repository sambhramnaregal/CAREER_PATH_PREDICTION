import pandas as pd
import numpy as np

# Mocking the functions from app.py to isolate logic

def test_compare_logic():
    print("--- Starting Test ---")
    
    # 1. Mock Data
    # Pred has "Cluster X: Name" format sometimes? Or just Name?
    # Based on app.py: 
    # df['Profile_Name'] = [cluster_info.get(int(c), {}).get('name', f'Cluster {c}') ... ]
    
    # Scenario D: Both have "Profile_Name" - Test Suffix Logic
    print("\n--- Scenario D: Profile_Name Collision ---")
    data_pred_d = {
        'USN': ['1', '2'],
        'Profile_Name': ['Cluster 0: Dev', 'Profile 1: QA'] 
    }
    data_truth_d = {
        'USN': ['1', '2'],
        'Profile_Name': ['Dev', 'QA'] # SAME HEADER NAME
    }
    
    df_p = pd.DataFrame(data_pred_d)
    df_t = pd.DataFrame(data_truth_d)

    # 1. Detect Columns BEFORE Merge
    def find_profile_col(df):
        for c in df.columns:
            if 'profile_name' in c.lower(): return c
        return None

    col_p = find_profile_col(df_p)
    col_t = find_profile_col(df_t)
    print(f"Detected Pre-Merge: Pred='{col_p}', Truth='{col_t}'")

    # 2. Merge
    merged = pd.merge(df_p, df_t, on='USN', suffixes=('_pred', '_truth'))
    print(f"Merged Cols: {merged.columns.tolist()}")

    # 3. Resolve Post-Merge Columns
    final_p = f"{col_p}_pred" if col_p in df_p.columns and col_p in df_t.columns else col_p
    final_t = f"{col_t}_truth" if col_t in df_p.columns and col_t in df_t.columns else col_t
    
    # Verify existence
    print(f"Searching for: '{final_p}' and '{final_t}'")
    if final_p in merged.columns and final_t in merged.columns:
        print("SUCCESS: Target columns found correctly.")
    else:
        print("FAILURE: Columns not found.")
        
    # Check values
    print(f"Pred Value: {merged[final_p].iloc[0]}")
    print(f"Truth Value: {merged[final_t].iloc[0]}")
    
    # Scenario B: "Cluster" prefix issue?
    # What if prediction is "Cluster 0: Technical Innovator"?
    print("\n--- Scenario B: Prefix Issue ---")
    data_pred_b = {
        'USN': ['1'],
        'Profile_Name': ['Cluster 0: Technical Innovator'] 
    }
    data_truth_b = {
        'USN': ['1'],
        'Actual_Career': ['Technical Innovator']
    }
    
    # ... (simplified logic check)
    p_val = "Cluster 0: Technical Innovator".lower().strip()
    t_val = "Technical Innovator".lower().strip()
    print(f"'{p_val}' == '{t_val}' -> {p_val == t_val}")
    
    # Scenario C: Whitespace/Case
    print("\n--- Scenario C: Whitespace ---")
    p_val = "Technical  Innovator" # double space
    t_val = "Technical Innovator"
    print(f"'{p_val}' == '{t_val}' -> {p_val == t_val}")

test_compare_logic()
