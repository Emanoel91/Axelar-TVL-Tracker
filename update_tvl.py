import pandas as pd
import requests

CSV_FILE = "tvl_data.csv"
API_URL = "https://api.dune.com/api/v1/query/5535180/results?api_key=kmCBMTxWKBxn6CVgCXhwDvcFL1fBp6rO"

try:
    df = pd.read_csv(CSV_FILE)

    if not df.empty:
        df["date"] = pd.to_datetime(df["date"]).dt.date

except FileNotFoundError:
    df = pd.DataFrame(columns=["date", "tvl", "asset_type"])

last_saved_date = None

if not df.empty:
    last_saved_date = df["date"].max()

try:
    response = requests.get(API_URL, timeout=30)
    response.raise_for_status()

    data = response.json()

    if (
        "result" not in data
        or "rows" not in data["result"]
        or len(data["result"]["rows"]) == 0
    ):
        print("Error: API data structure is invalid or no rows returned.")
        exit()

    api_df = pd.DataFrame(data["result"]["rows"])

    api_df["date"] = pd.to_datetime(api_df["date"]).dt.date

    latest_api_date = api_df["date"].max()

    latest_rows = api_df[api_df["date"] == latest_api_date]

    print(f"Latest date in API: {latest_api_date}")
    print(f"Latest date in CSV: {last_saved_date}")

    if last_saved_date is None or latest_api_date > last_saved_date:

        df = pd.concat([df, latest_rows], ignore_index=True)

        df.to_csv(CSV_FILE, index=False)

        print(
            f"Added {len(latest_rows)} new row(s) for date {latest_api_date}."
        )

    else:
        print("CSV file is already up to date.")

except requests.exceptions.RequestException as e:
    print(f"API request error: {e}")

except Exception as e:
    print(f"Unexpected error: {e}")
