import requests
import pandas as pd

# Fetch all mutual funds list from AMFI
url = "https://api.mfapi.in/mf"
response = requests.get(url)
data = response.json()

df = pd.DataFrame(data)
print(f"Total funds: {df.shape}")
print(f"\nColumns: {df.columns.tolist()}")
print(f"\nHead:\n{df.head()}")

# Save as fund master
df.to_csv('data/raw/fund_master.csv', index=False)
print("\n✅ Fund master saved!")

# Unique fund houses
print(f"\nUnique Fund Houses: {df['fundHouse'].nunique()}")
print(df['fundHouse'].unique()[:10])