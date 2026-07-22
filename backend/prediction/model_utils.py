from pathlib import Path
import csv
from datetime import datetime
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
import joblib

RAW_COLUMNS = ["Timestamp", "Shehia", "Bin"]
TARGET_COLUMN = "Waste Level"


def parse_timestamp(value):
    if value is None:
        return None
    if hasattr(value, "hour") and hasattr(value, "weekday"):
        return value
    text = str(value).strip()
    if text.endswith("Z"):
        text = text[:-1]
    try:
        return datetime.fromisoformat(text)
    except ValueError:
        return None


def normalize_text(value):
    if value is None:
        return "unknown"
    text = str(value).strip()
    return text if text else "unknown"


class WasteFeatureEngineer(BaseEstimator, TransformerMixin):
    def __init__(self):
        self.shehia_map = {}
        self.bin_map = {}

    def fit(self, X, y=None):
        rows = self._rows_from_input(X)
        shehias = sorted({normalize_text(row["Shehia"]) for row in rows})
        bins = sorted({normalize_text(row["Bin"]) for row in rows})
        self.shehia_map = {value: idx for idx, value in enumerate(shehias)}
        self.bin_map = {value: idx for idx, value in enumerate(bins)}
        return self

    def transform(self, X):
        rows = self._rows_from_input(X)
        result = []
        for row in rows:
            ts = parse_timestamp(row.get("Timestamp"))
            hour = ts.hour if ts else 0
            dow = ts.weekday() if ts else 0
            month = ts.month if ts else 0
            day = ts.day if ts else 0
            shehia = normalize_text(row.get("Shehia"))
            bin_name = normalize_text(row.get("Bin"))
            shehia_code = self.shehia_map.get(shehia, -1)
            bin_code = self.bin_map.get(bin_name, -1)
            result.append([shehia_code, bin_code, hour, dow, month, day])
        return np.array(result, dtype=float)

    def _rows_from_input(self, X):
        if isinstance(X, np.ndarray):
            if X.ndim == 1:
                X = X.reshape(1, -1)
            return [dict(zip(RAW_COLUMNS, row)) for row in X]
        if isinstance(X, list):
            if len(X) == 0:
                return []
            if isinstance(X[0], dict):
                return [x for x in X]
            return [dict(zip(RAW_COLUMNS, row)) for row in X]
        if hasattr(X, "items"):
            return [dict(X)]
        return []


def load_training_data(csv_path):
    csv_path = Path(csv_path)
    rows = []
    with open(csv_path, mode="r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for record in reader:
            if any(not record.get(col) for col in RAW_COLUMNS + [TARGET_COLUMN]):
                continue
            ts = parse_timestamp(record["Timestamp"])
            if ts is None:
                continue
            rows.append({
                "Timestamp": record["Timestamp"],
                "Shehia": normalize_text(record["Shehia"]),
                "Bin": normalize_text(record["Bin"]),
                TARGET_COLUMN: record[TARGET_COLUMN],
            })
    return rows


def build_pipeline():
    pipeline = Pipeline([
        ("engineer", WasteFeatureEngineer()),
        ("model", RandomForestClassifier(n_estimators=120, random_state=42)),
    ])
    return pipeline


def build_and_save_model(train_csv_path, output_path):
    rows = load_training_data(train_csv_path)
    X = [{col: row[col] for col in RAW_COLUMNS} for row in rows]
    y = [row[TARGET_COLUMN] for row in rows]

    pipeline = build_pipeline()
    pipeline.fit(X, y)

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(pipeline, output_path)
    return output_path


def load_pipeline(pickle_path):
    pickle_path = Path(pickle_path)
    return joblib.load(pickle_path)


def predict_waste_level(pipeline, timestamp, shehia, bin_name):
    raw_data = [{"Timestamp": timestamp, "Shehia": shehia, "Bin": bin_name}]
    prediction = pipeline.predict(raw_data)[0]
    probabilities = pipeline.predict_proba(raw_data)[0]
    classes = pipeline.named_steps["model"].classes_
    return {
        "prediction": str(prediction),
        "probabilities": {str(c): float(p) for c, p in zip(classes, probabilities)},
    }
