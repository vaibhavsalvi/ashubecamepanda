import pandas as pd

# Prompt user for CSV file path
csv_path = input('Enter the path to your CSV file: ')

try:
    df = pd.read_csv(csv_path)
    print(f"\nLoaded '{csv_path}' successfully!")
    print(f"Rows: {df.shape[0]}, Columns: {df.shape[1]}")
    print(f"\nColumn names: {list(df.columns)}")
    print("\nSummary statistics:")
    print(df.describe(include='all'))
except Exception as e:
    print(f"Error loading CSV file: {e}")
