import os

import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split


def build_data(rows=1200):
    rng = np.random.default_rng(42)
    data = pd.DataFrame(
        {
            "Users": rng.integers(100, 6500, rows),
            "Bandwidth": rng.integers(80, 1800, rows),
            "Latency": rng.normal(55, 28, rows).clip(5, 180),
            "SignalStrength": rng.integers(35, 100, rows),
            "PacketLoss": rng.normal(4, 3, rows).clip(0, 25),
            "Throughput": rng.normal(650, 260, rows).clip(40, 1800),
            "Jitter": rng.normal(10, 7, rows).clip(0.5, 55),
            "EdgeServerLoad": rng.integers(10, 96, rows),
        }
    )
    risk = (
        data["Latency"] * 0.32
        + data["PacketLoss"] * 5
        + data["Jitter"] * 0.7
        + data["EdgeServerLoad"] * 0.38
        - data["Throughput"] * 0.025
        - data["SignalStrength"] * 0.10
    )
    data["Congestion"] = np.select([risk >= 70, risk >= 45], [2, 1], default=0)
    return data


data = build_data()
X = data.drop("Congestion", axis=1)
y = data["Congestion"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

model = RandomForestClassifier(n_estimators=120, random_state=42)
model.fit(X_train, y_train)

accuracy = accuracy_score(y_test, model.predict(X_test))
os.makedirs("models", exist_ok=True)
joblib.dump(model, "models/congestion_model.pkl")

print(f"Accuracy: {accuracy:.3f}")
print("Model saved to models/congestion_model.pkl")
