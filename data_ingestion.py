import pandas as pd
import os

files = os.listdir('data/raw')
csv_files = [f for f in files if f.endswith('.csv')]

for file in csv_files:
    df = pd.read_csv(f'data/raw/{file}')
    print(f"\n📁 {file}")
    print(f"Shape: {df.shape}")
    print(f"Dtypes:\n{df.dtypes}")
    print(f"Head:\n{df.head(3)}")
    print(f"Nulls: {df.isnull().sum().sum()}")

print("\n✅ Data ingestion complete!")