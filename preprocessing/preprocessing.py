# preprocessing.py
# Simple log loader + aggregation for Phase-1 demo

import pandas as pd
from typing import Tuple

DEFAULT_PATH = "data/sample_logs.csv"

def load_raw(path: str = DEFAULT_PATH) -> pd.DataFrame:
    df = pd.read_csv(path, parse_dates=["timestamp"])
    return df

def clean_and_aggregate(path: str = DEFAULT_PATH) -> pd.DataFrame:
    """
    Load logs, add a 'failed' flag, aggregate per IP and return features.
    Output columns: ip, failed, count, failed_ratio
    """
    df = load_raw(path)
    # fill missing basic fields
    df = df.fillna({"result": "unknown", "count": 1})
    # simple feature
    df["failed"] = df["result"].apply(lambda x: 1 if str(x).lower() == "fail" else 0)
    # ensure count numeric
    df["count"] = pd.to_numeric(df["count"], errors="coerce").fillna(1).astype(int)
    # aggregate per IP
    agg = df.groupby("ip").agg({"failed": "sum", "count": "sum"}).reset_index()
    agg["failed_ratio"] = agg["failed"] / agg["count"].replace(0, 1)
    return agg

def quick_summary(path: str = DEFAULT_PATH) -> None:
    agg = clean_and_aggregate(path)
    print("=== Aggregated features per IP ===")
    print(agg)
    print("\n=== Basic stats ===")
    print(agg.describe().transpose())

if __name__ == "__main__":
    quick_summary()
