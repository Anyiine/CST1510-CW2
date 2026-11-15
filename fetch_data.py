
from pathlib import Path
import pandas as pd
import requests

# This sets the API information.
URL = "https://disease.sh/v3/covid-19/countries"
PARAMS = {}
RECORDS_KEY = None

# This selects the columns needed.
RENAME = {}
KEEP = [
    "country",
    "continent",
    "cases",
    "deaths",
    "recovered",
    "tests",
    "population",
    "active"
]
MUST_HAVE = ["cases", "continent"]

# This sets the CSV file location.
RAW_FILE = Path(__file__).parent / "DATA" / "raw.csv"


def get_data(url, params):
    # This gets data from the API.
    try:
        response = requests.get(url, params=params, timeout=15)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as error:
        print("Could not get the data:", error)
        return None


def make_table(data, records_key):
    # This converts the data into a table.
    records = data[records_key] if records_key else data
    return pd.json_normalize(records, sep="_")


def tidy_data(df):
    # This cleans and selects the columns.
    df = df.rename(columns=RENAME)
    df = df[KEEP]
    df = df.dropna(subset=MUST_HAVE)
    return df


def save_data(df, path):
    # This saves the data as a CSV file.
    path.parent.mkdir(exist_ok=True)
    df.to_csv(path, index=False)
    print(f"Saved {len(df)} rows to {path}")


if __name__ == "__main__":
    # This runs the program.
    data = get_data(URL, PARAMS)
    if data is not None:
        table = make_table(data, RECORDS_KEY)
        table = tidy_data(table)
        print(table.head())
        save_data(table, RAW_FILE)
