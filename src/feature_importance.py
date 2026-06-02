import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.inspection import permutation_importance
import joblib
import os

# Load Dataset
data = pd.read_csv("data/processed/processed_network_data.csv")

# Features and Target
X = data.drop("Congestion", axis=1)
y = data["Congestion"]

# Train-Test Split
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

model = joblib.load("models/congestion_model.pkl")

# Permutation Importance
importance = permutation_importance(
    model,
    X_test,
    y_test,
    n_repeats=12,
    random_state=42
)

# Create DataFrame
importance_df = pd.DataFrame({
    "Feature": X.columns,
    "Importance": importance.importances_mean
})

# Sort Descending
importance_df = importance_df.sort_values(
    by="Importance",
    ascending=False
)

print("\nFeature Importance:\n")
print(importance_df)

os.makedirs("reports", exist_ok=True)
importance_df.to_csv("reports/feature_importance.csv", index=False)

# Plot
plt.figure(figsize=(8,5))
plt.bar(
    importance_df["Feature"],
    importance_df["Importance"]
)

plt.title("Feature Importance for Network Congestion Prediction")
plt.xlabel("Features")
plt.ylabel("Importance Score")
plt.tight_layout()

plt.savefig("reports/feature_importance.png")
print("\nFeature importance report saved to reports/feature_importance.csv")
