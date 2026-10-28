"""
train_model.py
==============
A simple, beginner-friendly script to train a Support Vector Machine (SVM)
classifier to predict weather categories (Sunny, Rainy, Cloudy, Snowy)
from physical atmospheric measurements.

Steps performed:
1. Load and inspect the dataset from data/weather.csv.
2. Check for missing values and validate feature columns.
3. Split the data into 80% training and 20% testing sets.
4. Build a Pipeline combining StandardScaler and an RBF-kernel SVM classifier.
5. Train the model and evaluate it using Accuracy, Precision, Recall, and F1-Score.
6. Save the fitted pipeline and metrics to models/weather_model.joblib.
"""

import os
import sys
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.pipeline import Pipeline
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report,
    confusion_matrix
)
import joblib


# -------------------------------------------------------------
# Configuration Constants
# -------------------------------------------------------------
DATA_PATH = os.path.join("data", "weather.csv")
MODEL_DIR = "models"
MODEL_PATH = os.path.join(MODEL_DIR, "weather_model.joblib")

# Selected physical features that match live weather sensor APIs
FEATURE_COLUMNS = [
    "Temperature",           # in Celsius
    "Humidity",              # in percentage (0 - 100%)
    "Wind Speed",            # in km/h
    "Precipitation (%)",     # in percentage (0 - 100%)
    "Atmospheric Pressure",  # in hPa
    "UV Index",              # index level (0 - 14)
    "Visibility (km)"        # in kilometers
]

TARGET_COLUMN = "Weather Type"


def train_weather_model():
    print("=" * 60)
    print(" WEATHER CLASSIFICATION USING SVM - MODEL TRAINING")
    print("=" * 60)

    # 1. Verify dataset exists
    if not os.path.exists(DATA_PATH):
        print(f"\n[ERROR] Dataset not found at '{DATA_PATH}'.")
        print("Please place the 'weather.csv' file inside the 'data/' directory.")
        sys.exit(1)

    print(f"\n1. Loading dataset from '{DATA_PATH}'...")
    df = pd.read_csv(DATA_PATH)
    print(f"   -> Loaded {df.shape[0]} rows and {df.shape[1]} columns.")

    # 2. Check required columns
    missing_cols = [col for col in FEATURE_COLUMNS + [TARGET_COLUMN] if col not in df.columns]
    if missing_cols:
        print(f"[ERROR] Missing required columns in dataset: {missing_cols}")
        sys.exit(1)

    # 3. Handle missing values (if any)
    missing_count = df[FEATURE_COLUMNS + [TARGET_COLUMN]].isnull().sum().sum()
    if missing_count > 0:
        print(f"   -> Found {missing_count} missing values. Dropping rows with missing values...")
        df = df.dropna(subset=FEATURE_COLUMNS + [TARGET_COLUMN])
    else:
        print("   -> No missing values found in selected columns.")

    # 4. Extract features (X) and target (y)
    X = df[FEATURE_COLUMNS]
    y = df[TARGET_COLUMN]

    print("\n2. Dataset Class Distribution:")
    for class_name, count in y.value_counts().items():
        print(f"   - {class_name:<10}: {count} samples")

    # 5. Split into training (80%) and testing (20%) sets
    print("\n3. Splitting data into 80% train and 20% test sets (stratified)...")
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.20,
        random_state=42,
        stratify=y
    )
    print(f"   -> Training samples: {len(X_train)}")
    print(f"   -> Testing samples:  {len(X_test)}")

    # 6. Build the scikit-learn Pipeline
    # Using StandardScaler to normalize feature distributions
    # Using SVC with RBF kernel and probability=True for confidence scoring
    print("\n4. Building Pipeline with StandardScaler + RBF-Kernel SVM (SVC)...")
    pipeline = Pipeline([
        ("scaler", StandardScaler()),
        ("svm", SVC(kernel="rbf", probability=True, random_state=42))
    ])

    # 7. Train the model
    print("   -> Training SVM on training data (this may take a few moments)...")
    pipeline.fit(X_train, y_train)
    print("   -> Training completed successfully!")

    # 8. Evaluate on test set
    print("\n5. Evaluating model on unseen test set...")
    y_pred = pipeline.predict(X_test)

    acc = accuracy_score(y_test, y_pred)
    prec = precision_score(y_test, y_pred, average="weighted")
    rec = recall_score(y_test, y_pred, average="weighted")
    f1 = f1_score(y_test, y_pred, average="weighted")

    print("\n" + "-" * 50)
    print(" MODEL EVALUATION METRICS:")
    print("-" * 50)
    print(f" Accuracy : {acc * 100:.2f}%")
    print(f" Precision: {prec * 100:.2f}% (weighted)")
    print(f" Recall   : {rec * 100:.2f}% (weighted)")
    print(f" F1-Score : {f1 * 100:.2f}% (weighted)")
    print("-" * 50)

    print("\nDetailed Classification Report:")
    print(classification_report(y_test, y_pred))

    print("Confusion Matrix:")
    labels = list(pipeline.classes_)
    cm = confusion_matrix(y_test, y_pred, labels=labels)
    cm_df = pd.DataFrame(cm, index=labels, columns=labels)
    print(cm_df)

    # 9. Store metadata
    metrics_dict = {
        "accuracy": round(float(acc), 4),
        "precision": round(float(prec), 4),
        "recall": round(float(rec), 4),
        "f1_score": round(float(f1), 4),
        "classes": labels,
        "features": FEATURE_COLUMNS,
        "test_samples": int(len(y_test)),
        "train_samples": int(len(X_train))
    }
    pipeline.custom_metrics_ = metrics_dict
    pipeline.custom_feature_names_ = FEATURE_COLUMNS

    # 10. Save the complete fitted pipeline and metadata
    os.makedirs(MODEL_DIR, exist_ok=True)
    model_bundle = {
        "pipeline": pipeline,
        "metrics": metrics_dict,
        "feature_names": FEATURE_COLUMNS,
        "target_classes": labels
    }
    joblib.dump(model_bundle, MODEL_PATH)
    print(f"\n6. Successfully saved model pipeline to: '{MODEL_PATH}'")
    print("=" * 60)
    print(" Training finished cleanly!")
    print("=" * 60)

    return pipeline, metrics_dict


if __name__ == "__main__":
    train_weather_model()