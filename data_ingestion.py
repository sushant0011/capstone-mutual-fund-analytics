import os
import pandas as pd

# 10 official files ki list
provided_files = [
    "01_fund_master.csv", "02_nav_history.csv", "03_aum_by_fund_house.csv",
    "04_monthly_sip_inflows.csv", "05_category_inflows.csv", "06_industry_folio_count.csv",
    "07_scheme_performance.csv", "08_investor_transactions.csv", "09_portfolio_holdings.csv",
    "10_benchmark_indices.csv"
]

print("==== DAY 1: OFFICIAL DATA INGESTION ====\n")

for file_name in provided_files:
    file_path = f"data/raw/{file_name}"
    
    if os.path.exists(file_path):
        print(f"📄 Analyzing File: {file_name}")
        df = pd.read_csv(file_path)
        
        print(f"Shape: {df.shape}")
        print("\nData Types:")
        print(df.dtypes)
        
        print("\nHead (First 2 rows):")
        print(df.head(2))
        
        print("\n" + "="*50 + "\n")
    else:
        print(f"⚠️ Warning: {file_name} missing in data/raw/ folder!")