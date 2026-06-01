import requests
import pandas as pd
import os

os.makedirs('data/raw', exist_ok=True)

schemes = {
    "HDFC_Top100": 125497,
    "SBI_Bluechip": 119551,
    "ICICI_Bluechip": 120503,
    "Nippon_LargeCap": 118632,
    "Axis_Bluechip": 119092,
    "Kotak_Bluechip": 120841
}

for name, code in schemes.items():
    r = requests.get(f"https://api.mfapi.in/mf/{code}")
    d = r.json()
    df = pd.DataFrame(d['data'])
    df.to_csv(f'data/raw/{name}_nav.csv', index=False)
    print(f"✅ {name} saved! Shape: {df.shape}")

print("\n🎉 All NAV data fetched!")