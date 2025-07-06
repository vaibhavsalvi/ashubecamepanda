import pandas as pd

csv_path = 'sample.csv'  # Use the sample CSV file in the current folder

try:
    df = pd.read_csv(csv_path)
    print(f"\nLoaded '{csv_path}' successfully!")
    print(f"Rows: {df.shape[0]}, Columns: {df.shape[1]}")
    print(f"\nColumn names: {list(df.columns)}")
    print("\nSummary statistics:")
    print(df.describe(include='all'))
except Exception as e:
    print(f"Error loading CSV file: {e}")
