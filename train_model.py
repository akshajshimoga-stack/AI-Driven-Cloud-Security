# train_model.py
# Minimal RandomForest trainer for Phase-1

import os
import joblib
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from preprocessing import clean_and_aggregate

MODEL_DIR = "models"
MODEL_PATH = os.path.join(MODEL_DIR, "rf_model.joblib")

def train_and_save(model_path: str = MODEL_PATH):
    os.makedirs(MODEL_DIR, exist_ok=True)
    df = clean_and_aggregate()
    # Create a simple label: if failed > 3 -> attack (1) else normal (0)
    df["label"] = (df["failed"] > 3).astype(int)
    X = df[["failed", "count", "failed_ratio"]].values
    y = df["label"].values

    # If too few rows, add synthetic examples so model trains
    if len(X) < 4:
        synthetic = np.array([[5,6,0.8],[0,10,0.0],[4,5,0.6],[1,2,0.5]])
        X = np.vstack([X, synthetic])
        y = np.hstack([y, [1,0,1,0]])

    Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.33, random_state=42)
    clf = RandomForestClassifier(n_estimators=100, random_state=42)
    clf.fit(Xtr, ytr)

    print("Train score: {:.3f}".format(clf.score(Xtr, ytr)))
    print("Test score:  {:.3f}".format(clf.score(Xte, yte)))

    joblib.dump(clf, model_path)
    print(f"Saved model to {model_path}")

if __name__ == "__main__":
    train_and_save()
