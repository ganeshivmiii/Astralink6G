import pandas as pd
import joblib
import os
from sklearn.preprocessing import LabelEncoder

print("Program Started")

data = pd.read_csv("data/raw/network_data.csv")

print("Dataset Loaded")

models_dir = "models"
os.makedirs(models_dir, exist_ok=True)

congestion_encoder = LabelEncoder()
slice_encoder = LabelEncoder()

data["Congestion"] = congestion_encoder.fit_transform(data["Congestion"])
data["NetworkSlice"] = slice_encoder.fit_transform(data["NetworkSlice"])

print("Encoding Completed")

os.makedirs("data/processed", exist_ok=True)
data.to_csv("data/processed/processed_network_data.csv", index=False)
joblib.dump(congestion_encoder, os.path.join(models_dir, "congestion_label_encoder.pkl"))
joblib.dump(slice_encoder, os.path.join(models_dir, "network_slice_encoder.pkl"))

print("File Saved Successfully")
print("Encoders Saved Successfully")

print(data.head())
