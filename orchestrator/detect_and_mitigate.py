# detect_and_mitigate.py
# Run detection on aggregated features and simulate mitigation actions

import os
import joblib
from preprocessing import clean_and_aggregate

MODEL_PATH = "models/rf_model.joblib"
RESULTS_DIR = "results"
LOG_PATH = os.path.join(RESULTS_DIR, "mitigation_log.txt")

def mitigate(action: str, ip: str):
    os.makedirs(RESULTS_DIR, exist_ok=True)
    msg = f"[AUTO-MITIGATION] {action} on {ip}"
    print(msg)
    with open(LOG_PATH, "a") as f:
        f.write(msg + "\n")

def run_detection(model_path: str = MODEL_PATH):
    if not os.path.exists(model_path):
        print("Model not found. Run train_model.py first.")
        return
    clf = joblib.load(model_path)
    agg = clean_and_aggregate()
    if agg.empty:
        print("No aggregated features found (check data/sample_logs.csv).")
        return

    for _, row in agg.iterrows():
        X = [[row["failed"], row["count"], row["failed_ratio"]]]
        pred = clf.predict(X)[0]
        prob = clf.predict_proba(X).max() if hasattr(clf, "predict_proba") else 1.0
        print(f"IP {row['ip']} pred={pred} prob={prob:.2f}")
        # simple rule: if predicted attack and probability high -> mitigate
        if pred == 1 and prob >= 0.6:
            mitigate("simulate_block_ip", row["ip"])

if __name__ == "__main__":
    run_detection()
