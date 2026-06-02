import os
import pandas as pd
import numpy as np

# Ensure processed directory exists
os.makedirs('data/processed', exist_ok=True)

print("==== STARTING DATA CLEANING (DAY 2) ====\n")

# ----------------------------------------------------
# 1. CLEANING: nav_history.csv
# ----------------------------------------------------
print("1. Cleaning 02_nav_history.csv...")
nav_path = 'data/raw/02_nav_history.csv'

if os.path.exists(nav_path):
    df_nav = pd.read_csv(nav_path)
    
    # Check column names from terminal earlier: ['amfi_code', 'date', 'nav']
    # Parse date to datetime
    df_nav['date'] = pd.to_datetime(df_nav['date'], errors='coerce')
    
    # Drop rows where critical info like date or amfi_code or nav is null
    df_nav = df_nav.dropna(subset=['amfi_code', 'date', 'nav'])
    
    # Filter valid NAV (NAV > 0)
    df_nav = df_nav[df_nav['nav'] > 0]
    
    # Sort by amfi_code and date for proper forward fill
    df_nav = df_nav.sort_values(by=['amfi_code', 'date'])
    
    # Drop duplicates
    df_nav = df_nav.drop_duplicates(subset=['amfi_code', 'date'])
    
    # Forward-fill missing dates for weekends/holidays per AMFI code
    # Setting date as index to use resample or reindex if needed, or simple ffill if dates are missing rows
    # A robust way for simple sequence ffill:
    df_nav['nav'] = df_nav.groupby('amfi_code')['nav'].ffill()
    
    df_nav.to_csv('data/processed/cleaned_nav_history.csv', index=False)
    print(f"   Success: Cleaned NAV rows -> {df_nav.shape[0]}")
else:
    print("   Error: 02_nav_history.csv not found!")


# ----------------------------------------------------
# 2. CLEANING: investor_transactions.csv
# ----------------------------------------------------
print("\n2. Cleaning 08_investor_transactions.csv...")
tx_path = 'data/raw/08_investor_transactions.csv'

if os.path.exists(tx_path):
    df_tx = pd.read_csv(tx_path)
    
    # Standardize transaction_type (Trim spaces and uppercase)
    # Target: SIP, Lumpsum, Redemption
    if 'transaction_type' in df_tx.columns:
        df_tx['transaction_type'] = df_tx['transaction_type'].astype(str).str.strip().str.capitalize()
        # Mapping variations just in case (e.g. 'Sip' -> 'SIP', 'Redeem' -> 'Redemption')
        type_map = {'Sip': 'SIP', 'Lumpsum': 'Lumpsum', 'Redemption': 'Redemption', 'Redeem': 'Redemption'}
        df_tx['transaction_type'] = df_tx['transaction_type'].map(type_map).fillna(df_tx['transaction_type'])
    
    # Validate amount > 0
    if 'amount' in df_tx.columns:
        df_tx = df_tx[df_tx['amount'] > 0]
        
    # Standardize transaction date if exists
    if 'transaction_date' in df_tx.columns:
        df_tx['transaction_date'] = pd.to_datetime(df_tx['transaction_date'], errors='coerce')
    elif 'date' in df_tx.columns:
        df_tx['date'] = pd.to_datetime(df_tx['date'], errors='coerce')

    # Drop duplicates if any
    df_tx = df_tx.drop_duplicates()
    
    df_tx.to_csv('data/processed/cleaned_investor_transactions.csv', index=False)
    print(f"   Success: Cleaned Transactions rows -> {df_tx.shape[0]}")
else:
    print("   Error: 08_investor_transactions.csv not found!")


# ----------------------------------------------------
# 3. CLEANING: scheme_performance.csv
# ----------------------------------------------------
print("\n3. Cleaning 07_scheme_performance.csv...")
perf_path = 'data/raw/07_scheme_performance.csv'

if os.path.exists(perf_path):
    df_perf = pd.read_csv(perf_path)
    
    # Convert return columns to numeric, turn strings like '12.5%' or anomalies into NaN first, then fill or drop
    return_cols = [col for col in df_perf.columns if 'return' in col or 'yr' in col or 'cagr' in col.lower()]
    
    for col in return_cols:
        if df_perf[col].dtype == 'object':
            df_perf[col] = df_perf[col].astype(str).str.replace('%', '').str.strip()
        df_perf[col] = pd.to_numeric(df_perf[col], errors='coerce')
    
    # Clean Expense Ratio (Should be numeric and between 0.1% and 2.5%, meaning 0.1 to 2.5 or 0.001 to 0.025)
    # Let's check or handle both standard percentages (e.g. 1.5 meaning 1.5%)
    expense_col = [col for col in df_perf.columns if 'expense' in col.lower()]
    if expense_col:
        col = expense_col[0]
        if df_perf[col].dtype == 'object':
            df_perf[col] = df_perf[col].astype(str).str.replace('%', '').str.strip()
        df_perf[col] = pd.to_numeric(df_perf[col], errors='coerce')
        
        # Flags anomalies instead of deleting, or clips them. Let's filter or log anomalies:
        anomalies = df_perf[(df_perf[col] < 0.1) | (df_perf[col] > 2.5)]
        print(f"   Found {anomalies.shape[0]} expense ratio anomalies (outside 0.1% - 2.5%)")
        
    df_perf = df_perf.drop_duplicates()
    df_perf.to_csv('data/processed/cleaned_scheme_performance.csv', index=False)
    print(f"   Success: Cleaned Performance rows -> {df_perf.shape[0]}")
else:
    print("   Error: 07_scheme_performance.csv not found!")

print("\n==== DATA CLEANING COMPLETE! COMPLETED PROCESSING PHASE ====")