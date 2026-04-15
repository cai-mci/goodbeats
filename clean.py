import pandas as pd

# Load CSV
df = pd.read_csv('feature_stats_final.csv')
# Fill NaN/null values with 0
df.fillna(0, inplace=True)
# Save as new CSV
df.to_csv('clean_data.csv', index=False)