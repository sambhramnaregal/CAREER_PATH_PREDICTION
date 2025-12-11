import pandas as pd
try:
    # Create two dfs with same column name
    df1 = pd.DataFrame({'Profile': ['A', 'B']})
    df2 = pd.DataFrame({'Profile': ['A', 'B']})
    
    # Concat axis=1
    merged = pd.concat([df1, df2], axis=1)
    print("Columns:", merged.columns)
    
    # Try to access 'Profile' and use .str
    # This should return a DataFrame and fail .str
    print("Accessing 'Profile'...")
    col = merged['Profile']
    print("Type:", type(col))
    
    vals = col.astype(str).str.lower()
    print("Success:", vals)

except Exception as e:
    print(f"Caught expected error: {e}")
