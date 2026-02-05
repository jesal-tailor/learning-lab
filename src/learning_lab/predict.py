import json
from pathlib import Path
from typing import Dict, List

MODEL_PATH = Path(__file__).parent / "models" / "model_v1.json"

def load_model() -> Dict:
    return json.loads(MODEL_PATH.read_text())

def predict(features: List[float]) -> Dict:
    model = load_model()
    coef = model["coef"]
    intercept = model["intercept"]

    if len(features) != len(coef):
        raise ValueError(f"Expected {len(coef)} features, got {len(features)}")

    y = sum(f * c for f, c in zip(features, coef)) + intercept
    return {
        "prediction": y,
        "model_name": model["model_name"],
        "model_version": model["model_version"],
    }
