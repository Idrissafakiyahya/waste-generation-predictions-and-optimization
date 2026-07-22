from pathlib import Path
import pandas as pd
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import OrdinalEncoder
import joblib

RAW_COLUMNS = ["Timestamp", "Shehia", "Bin"]
TARGET_COLUMN = "Waste Level"

class WasteFeatureEngineer(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        return self

    def transform(self, X):
        if isinstance(X, np.ndarray):
            X = pd.DataFrame(X, columns=self.feature_names_in_)
        elif isinstance(X, list):
            X = pd.DataFrame(X)
        else:
            X = pd.DataFrame(X)

        df = X.copy()
        df["Timestamp"] = pd.to_datetime(df["Timestamp"], utc=True, errors="coerce")
        df["Hour"] = df["Timestamp"].dt.hour.fillna(0).astype(int)
        df["DayOfWeek"] = df["Timestamp"].dt.weekday.fillna(0).astype(int)
        df["Month"] = df["Timestamp"].dt.month.fillna(0).astype(int)
        df["Day"] = df["Timestamp"].dt.day.fillna(0).astype(int)
        df["Shehia"] = df["Shehia"].astype(str).fillna("unknown")
        df["Bin"] = df["Bin"].astype(str).fillna("unknown")
        return df[["Shehia", "Bin", "Hour", "DayOfWeek", "Month", "Day"]]


def load_training_data(csv_path):
    csv_path = Path(csv_path)
    df = pd.read_csv(csv_path, parse_dates=["Timestamp"])
    df = df.dropna(subset=RAW_COLUMNS + [TARGET_COLUMN]).copy()
    df["Shehia"] = df["Shehia"].astype(str).fillna("unknown")
    df["Bin"] = df["Bin"].astype(str).fillna("unknown")
    return df


def build_pipeline():
    categorical_encoder = OrdinalEncoder(handle_unknown="use_encoded_value", unknown_value=-1)
    feature_transformer = ColumnTransformer(
        [
            ("cat", categorical_encoder, ["Shehia", "Bin"]),
            ("num", "passthrough", ["Hour", "DayOfWeek", "Month", "Day"]),
        ],
        remainder="drop",
    )

    pipeline = Pipeline(
        [
            ("engineer", WasteFeatureEngineer()),
            ("encode", feature_transformer),
            ("model", RandomForestClassifier(n_estimators=120, random_state=42)),
        ]
    )
    return pipeline


def build_and_save_model(train_csv_path, output_path):
    df = load_training_data(train_csv_path)
    X = df[RAW_COLUMNS]
    y = df[TARGET_COLUMN]

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
    raw_data = pd.DataFrame(
        [{"Timestamp": timestamp, "Shehia": shehia, "Bin": bin_name}]
    )
    prediction = pipeline.predict(raw_data)[0]
    probabilities = pipeline.predict_proba(raw_data)[0]
    classes = pipeline.named_steps["model"].classes_
    return {
        "prediction": str(prediction),
        "probabilities": {str(c): float(p) for c, p in zip(classes, probabilities)},
    }
