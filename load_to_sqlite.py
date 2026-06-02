import os
import pandas as pd
from sqlalchemy import create_engine, text

db_path = "bluestock_mf.db"

# Agar purani kharab wali db file bani ho toh use remove kar dete hain fresh start ke liye
if os.path.exists(db_path):
    os.remove(db_path)

engine = create_engine(f"sqlite:///{db_path}")

print("==== STARTING DATABASE DESIGN & LOADING (FIXED) ====\n")

# 1. CREATE TABLES (STAR SCHEMA) WITH PRIMARY AND FOREIGN KEYS
with engine.connect() as conn:
    print("Designing Schema & Creating Tables...")
    
    # Enable foreign keys in SQLite
    conn.execute(text("PRAGMA foreign_keys = ON;"))
    
    # dim_fund Table
    conn.execute(text("""
    CREATE TABLE IF NOT EXISTS dim_fund (
        amfi_code INTEGER PRIMARY KEY,
        scheme_name TEXT,
        category TEXT,
        sub_category TEXT
    );
    """))
    
    # fact_nav Table
    conn.execute(text("""
    CREATE TABLE IF NOT EXISTS fact_nav (
        nav_id INTEGER PRIMARY KEY AUTOINCREMENT,
        amfi_code INTEGER,
        date TEXT,
        nav REAL,
        FOREIGN KEY (amfi_code) REFERENCES dim_fund(amfi_code)
    );
    """))
    
    # fact_transactions Table (Schema keeps 'amount' as standard)
    conn.execute(text("""
    CREATE TABLE IF NOT EXISTS fact_transactions (
        transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
        amfi_code INTEGER,
        investor_id INTEGER,
        transaction_type TEXT,
        amount REAL,
        transaction_date TEXT,
        kyc_status TEXT,
        state TEXT,
        FOREIGN KEY (amfi_code) REFERENCES dim_fund(amfi_code)
    );
    """))

    # fact_performance Table
    conn.execute(text("""
    CREATE TABLE IF NOT EXISTS fact_performance (
        amfi_code INTEGER PRIMARY KEY,
        one_year_return REAL,
        three_year_return REAL,
        five_year_return REAL,
        expense_ratio REAL,
        aum REAL,
        FOREIGN KEY (amfi_code) REFERENCES dim_fund(amfi_code)
    );
    """))
    print("   Success: Database schema defined with Primary & Foreign keys.\n")

# 2. LOADING DATA USING SQLALCHEMY
print("Loading Cleaned Datasets into SQLite...")

# Load Cleaned CSVs
df_nav = pd.read_csv('data/processed/cleaned_nav_history.csv')
df_tx = pd.read_csv('data/processed/cleaned_investor_transactions.csv')
df_perf = pd.read_csv('data/processed/cleaned_scheme_performance.csv')

# --- FIXING TRANSACTION COLUMNS DYNAMICALLY ---
# Agar CSV me amount_inr hai toh use standard 'amount' me rename karenge
if 'amount_inr' in df_tx.columns:
    df_tx = df_tx.rename(columns={'amount_inr': 'amount'})

# Baaki columns ko bhi safe side cross-check kar lete hain
rename_dict = {
    'date': 'transaction_date',
    'cust_id': 'investor_id',
    'customer_id': 'investor_id',
    'tx_id': 'transaction_id'
}
df_tx = df_tx.rename(columns={k: v for k, v in rename_dict.items() if k in df_tx.columns})

# Keep only columns that match the SQL schema for fact_transactions
tx_schema_cols = ['transaction_id', 'amfi_code', 'investor_id', 'transaction_type', 'amount', 'transaction_date', 'kyc_status', 'state']
# Filter out only those columns which actually exist in df_tx
final_tx_cols = [col for col in tx_schema_cols if col in df_tx.columns]
df_tx_final = df_tx[final_tx_cols]

# --- FIXING PERFORMANCE COLUMNS DYNAMICALLY ---
df_perf_db = pd.DataFrame()
df_perf_db['amfi_code'] = df_perf['amfi_code'] if 'amfi_code' in df_perf.columns else df_perf.iloc[:, 0]

# Dynamic checks for return columns
r1 = [c for c in df_perf.columns if '1' in c and 'return' in c.lower()]
r3 = [c for c in df_perf.columns if '3' in c and 'return' in c.lower()]
r5 = [c for c in df_perf.columns if '5' in c and 'return' in c.lower()]
exp = [c for c in df_perf.columns if 'expense' in c.lower()]
aum_col = [c for c in df_perf.columns if 'aum' in c.lower()]

df_perf_db['one_year_return'] = df_perf[r1[0]] if r1 else 0
df_perf_db['three_year_return'] = df_perf[r3[0]] if r3 else 0
df_perf_db['five_year_return'] = df_perf[r5[0]] if r5 else 0
df_perf_db['expense_ratio'] = df_perf[exp[0]] if exp else 0
df_perf_db['aum'] = df_perf[aum_col[0]] if aum_col else 500000000  # Default mock value if missing

# Dynamic unique funds extraction for dim_fund
unique_amfi = pd.concat([df_nav['amfi_code'], df_tx_final['amfi_code']]).unique()
unique_funds = pd.DataFrame({'amfi_code': unique_amfi})
unique_funds['scheme_name'] = "Scheme " + unique_funds['amfi_code'].astype(str)
unique_funds['category'] = "Equity"
unique_funds['sub_category'] = "Large Cap"

# Populating Tables into Database
print("   Writing to dim_fund...")
unique_funds.to_sql('dim_fund', con=engine, if_exists='append', index=False)

print("   Writing to fact_nav...")
df_nav.to_sql('fact_nav', con=engine, if_exists='append', index=False)

print("   Writing to fact_transactions...")
df_tx_final.to_sql('fact_transactions', con=engine, if_exists='append', index=False)

print("   Writing to fact_performance...")
df_perf_db.to_sql('fact_performance', con=engine, if_exists='append', index=False)

print("   Success: All data loaded into SQLite database successfully.\n")

# 3. VERIFICATION OF ROW COUNTS
print("==== VERIFICATION REPORT ====")
with engine.connect() as conn:
    for table in ['dim_fund', 'fact_nav', 'fact_transactions', 'fact_performance']:
        res = conn.execute(text(f"SELECT COUNT(*) FROM {table}")).fetchone()[0]
        print(f"   Table '{table}' Row Count: {res}")

print("\n==== LOADING & VERIFICATION COMPLETE! ====")