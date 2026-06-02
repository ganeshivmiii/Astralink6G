<<<<<<< HEAD
AstraLink 6G
============

AstraLink 6G is a premium AI-powered 6G network operations dashboard. It generates realistic synthetic network traffic, predicts congestion, detects abnormal network behavior, compares machine-learning models, and visualizes smart multi-factor routing in an interactive Streamlit experience.

Features
--------

- Synthetic 6G dataset with latency, bandwidth, signal strength, packet loss, throughput, jitter, energy consumption, handover rate, mobility speed, edge server load, and network slice type.
- Congestion prediction using model comparison across Random Forest, Gradient Boosting, and SVM.
- Cross-validation, accuracy, classification report, confusion matrix, and feature importance reports.
- Anomaly detection for latency spikes, packet loss issues, jitter, throughput drops, and edge-load pressure.
- Smart routing that considers latency, packet loss, bandwidth, and congestion instead of latency alone.
- Premium responsive Streamlit dashboard for desktop and mobile, with scenario presets, live risk scoring, loading animation, analytics controls, model insights, anomalies, and route visualization.

Project Structure
-----------------

```text
data/
  raw/network_data.csv
  processed/processed_network_data.csv
models/
  congestion_model.pkl
  congestion_label_encoder.pkl
  network_slice_encoder.pkl
reports/
  anomaly_detection.csv
  classification_report.json
  confusion_matrix.csv
  feature_importance.csv
  model_comparison.csv
src/
  anomaly_detection.py
  dashboard.py
  dataset_generator.py
  feature_importance.py
  preprocessing.py
  routing.py
  train_model.py
```

Setup
-----

```bash
pip install -r requirements.txt
```

Run Workflow
------------

Run these commands from the project root:

```bash
python src/dataset_generator.py
python src/preprocessing.py
python src/train_model.py
python src/feature_importance.py
python src/anomaly_detection.py
python src/routing.py
streamlit run src/dashboard.py
```

Generated Reports
-----------------

- `reports/model_comparison.csv`: accuracy and cross-validation scores for each model.
- `reports/classification_report.json`: precision, recall, and F1-score.
- `reports/confusion_matrix.csv`: class-level prediction matrix.
- `reports/feature_importance.csv`: permutation importance of network features.
- `reports/anomaly_detection.csv`: normal/anomaly labels and anomaly scores.
- `reports/smart_route.png`: multi-factor routing graph.

Future Scope
------------

- Add live network telemetry ingestion.
- Include reinforcement learning for dynamic routing decisions.
- Add energy-aware optimization for green 6G communication.
- Add edge-cloud task offloading recommendations.
- Connect the dashboard to a real-time alerting channel.
=======
# Astralink6G
>>>>>>> 4df94d0f7e68b9d91a92f1bfadd9edf9f249042f
