import pandas as pd
import requests
from datetime import date

CSV_FILE = "tvl_data.csv"

# بارگذاری داده‌های قبلی
try:
    df = pd.read_csv(CSV_FILE, parse_dates=["date"])
except FileNotFoundError:
    df = pd.DataFrame(columns=["date", "tvl", "asset_type"])

# بررسی آخرین تاریخ
last_date = df["date"].max() if not df.empty else None

# اگر داده امروز ثبت نشده، از API بگیر
if last_date is None or pd.to_datetime(last_date).date() < date.today():
    response = requests.get("https://api.dune.com/api/v1/query/5535180/results?api_key=kmCBMTxWKBxn6CVgCXhwDvcFL1fBp6rO")  # ← آدرس API واقعی
    if response.status_code == 200:
        data = response.json()  # فرض: {'tvl': ..., 'asset_type': ...}
        new_row = pd.DataFrame([{
            "date": date.today(),
            "tvl": data["tvl"],
            "asset_type": data["asset_type"]
        }])
        df = pd.concat([df, new_row], ignore_index=True)
        df.to_csv(CSV_FILE, index=False)
        print("داده جدید ذخیره شد.")
    else:
        print("خطا در دریافت داده از API")
else:
    print("داده امروز قبلاً ثبت شده است.")
