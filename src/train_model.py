import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.model_selection import cross_val_score
from sklearn.svm import SVC
import joblib
import json
import os

# Load Dataset
data = pd.read_csv("data/processed/processed_network_data.csv")

# Features
X = data.drop("Congestion", axis=1)

# Target
y = data["Congestion"]

# Split Dataset
X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

models = {
    "Random Forest": RandomForestClassifier(
        n_estimators=180,
        max_depth=12,
        random_state=42
    ),
    "Gradient Boosting": GradientBoostingClassifier(random_state=42),
    "SVM": SVC(kernel="rbf", probability=True, random_state=42)
}

results = []
trained_models = {}

for name, model in models.items():
    cv_scores = cross_val_score(model, X_train, y_train, cv=5)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)

    results.append({
        "Model": name,
        "Accuracy": round(float(accuracy), 4),
        "CVMean": round(float(cv_scores.mean()), 4),
        "CVStd": round(float(cv_scores.std()), 4)
    })
    trained_models[name] = model

results_df = pd.DataFrame(results).sort_values(
    by=["Accuracy", "CVMean"],
    ascending=False
)

best_model_name = results_df.iloc[0]["Model"]
best_model = trained_models[best_model_name]
best_predictions = best_model.predict(X_test)

os.makedirs("models", exist_ok=True)
os.makedirs("reports", exist_ok=True)

joblib.dump(best_model, "models/congestion_model.pkl")

results_df.to_csv("reports/model_comparison.csv", index=False)

report = classification_report(
    y_test,
    best_predictions,
    output_dict=True,
    zero_division=0
)
matrix = confusion_matrix(y_test, best_predictions)

with open("reports/classification_report.json", "w", encoding="utf-8") as file:
    json.dump(report, file, indent=2)

pd.DataFrame(matrix).to_csv("reports/confusion_matrix.csv", index=False)

metrics = {
    "best_model": best_model_name,
    "accuracy": round(float(accuracy_score(y_test, best_predictions)), 4),
    "features": list(X.columns)
}

with open("reports/model_metrics.json", "w", encoding="utf-8") as file:
    json.dump(metrics, file, indent=2)

print("\nModel Comparison:")
print(results_df)
print(f"\nBest Model: {best_model_name}")
print(f"Accuracy: {metrics['accuracy']}")
print("\nModel Saved Successfully")
