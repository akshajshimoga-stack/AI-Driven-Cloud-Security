# simulate_attack.py
# Create a small synthetic log file for demo/testing

import pandas as pd
from datetime import datetime, timedelta
import random
import os

OUT_PATH = "data/sample_logs.csv"

def make_logs(path: str = OUT_PATH, n: int = 40):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    base = datetime.now()
    ips = ["10.0.0.1", "10.0.0.2", "10.0.0.3"]
    rows = []
    for i in range(n):
        t = base + timedelta(seconds=i*2)
        ip = random.choice(ips)
        # induce failures for 10.0.0.1 more often (to simulate an attacker)
        if ip == "10.0.0.1":
            if random.random() < 0.6:
                rows.append([t.isoformat(), ip, "login", "fail", random.randint(1,6)])
            else:
                rows.append([t.isoformat(), ip, "request", "success", 1])
        else:
            if random.random() < 0.15:
                rows.append([t.isoformat(), ip, "login", "fail", 1])
            else:
                rows.append([t.isoformat(), ip, "request", "success", 1])
    df = pd.DataFrame(rows, columns=["timestamp","ip","event","result","count"])
    df.to_csv(path, index=False)
    print(f"Wrote {len(df)} logs to {path}")

if __name__ == "__main__":
    make_logs()
