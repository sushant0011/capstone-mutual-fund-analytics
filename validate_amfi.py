import pandas as pd

print("==== AMFI CODE VALIDATION ====")

# Asli official files load karo
fund_master = pd.read_csv('data/raw/01_fund_master.csv')
nav_history = pd.read_csv('data/raw/02_nav_history.csv')

# Column names check karne ke liye dono ka head print kar rahe hain
print("Fund Master Columns:", fund_master.columns.tolist())
print("NAV History Columns:", nav_history.columns.tolist())

# NOTE: Agar column ka naam 'scheme_code' ya 'amfi_code' hai, toh neeche badal lena.
# Maan lete hain column ka naam 'scheme_code' hai dono mein:
try:
    # Tum columns ke naam dekh kar yahan 'scheme_code' badal sakte ho agar kuch aur ho toh
    col_name = 'amfi_code'
    
    master_codes = set(fund_master[col_name].unique())
    history_codes = set(nav_history[col_name].unique())

    print(f"\nUnique Codes in Fund Master: {len(master_codes)}")
    print(f"Unique Codes in Nav History: {len(history_codes)}")

    # Validation logic: Check master codes missing in history
    missing_codes = master_codes - history_codes

    if len(missing_codes) == 0:
        print("\n Success: Every AMFI code from fund_master exists in nav_history!")
    else:
        print(f"\n Alert: {len(missing_codes)} codes are missing in nav_history!")
        print(f"Missing Codes Sample: {list(missing_codes)[:5]}")
        
except KeyError:
    print("\n Error: Column name match nahi hua. Ek baar dono files ke columns upar terminal mein check karo aur col_name update karo.")