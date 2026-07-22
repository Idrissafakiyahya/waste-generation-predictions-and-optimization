from pathlib import Path
from prediction.model_utils import build_and_save_model

if __name__ == "__main__":
    repo_root = Path(__file__).resolve().parent.parent
    train_path = repo_root / "waste_10weeks_training.csv"
    model_path = Path(__file__).resolve().parent / "waste_model.pkl"

    build_and_save_model(train_path, model_path)
    print(f"Saved waste prediction pipeline to: {model_path}")
