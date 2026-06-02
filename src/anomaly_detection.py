import os

import pandas as pd
from sklearn.ensemble import IsolationForest


FEATURES = [
    "Latency",
    "PacketLoss",
    "Jitter",
    "Throughput",
    "EdgeServerLoad",
    "HandoverRate"
]


def detect_anomalies():
    data = pd.read_csv("data/processed/processed_network_data.csv")

    detector = IsolationForest(
        contamination=0.06,
        random_state=42
    )

    labels = detector.fit_predict(data[FEATURES])
    scores = detector.decision_function(data[FEATURES])

    data["Anomaly"] = labels
    data["AnomalyScore"] = scores.round(4)
    data["AnomalyLabel"] = data["Anomaly"].map({1: "Normal", -1: "Anomaly"})

    os.makedirs("reports", exist_ok=True)
    data.to_csv("reports/anomaly_detection.csv", index=False)

    summary = data["AnomalyLabel"].value_counts().reset_index()
    summary.columns = ["Status", "Count"]
    summary.to_csv("reports/anomaly_summary.csv", index=False)

    print("Anomaly Detection Summary:")
    print(summary)
    print("\nAnomaly report saved to reports/anomaly_detection.csv")


if __name__ == "__main__":
    detect_anomalies()
