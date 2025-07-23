import pandas as pd
import matplotlib.pyplot as plt

# Load the sample.csv file
df = pd.read_csv('sample.csv', parse_dates=['opened_at'])

print("=== Incident Data Overview ===")
print(f"Total incidents: {len(df)}")
print(f"Columns: {list(df.columns)}\n")

print("=== Incidents by State ===")
print(df['state'].value_counts(), "\n")

print("=== Incidents by Priority ===")
print(df['priority'].value_counts(), "\n")

print("=== Incidents by Category ===")
print(df['category'].value_counts(), "\n")

print("=== Incidents Opened Per Day ===")
print(df['opened_at'].dt.date.value_counts().sort_index(), "\n")

print("=== Incidents Assigned To ===")
print(df['assigned_to'].value_counts(), "\n")

# Correlation analysis (only for numeric columns)
print("=== Correlation Matrix (numeric columns) ===")
print(df.corr(numeric_only=True))

# Visualize incidents per day
incidents_per_day = df['opened_at'].dt.date.value_counts().sort_index()
plt.figure(figsize=(8,4))
plt.plot(incidents_per_day.index, incidents_per_day.values, marker='o')
plt.title('Incidents Opened Per Day')
plt.xlabel('Date')
plt.ylabel('Number of Incidents')
plt.grid(True)
plt.tight_layout()
plt.show()