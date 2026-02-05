import os
import json
from pathlib import Path
from typing import Dict, List

MODEL_MAP = {
    "1.0.0": "model_v1.json",
    "1.0.1": "model_v1_1.json",
}

def get_model_version() -> str:
    return os.getenv("MODEL_VERSION", "1.0.0")

def load_model() -> Dict:
    version = get_model_version()
    model_file = MODEL_MAP[version]
    path = Path(__file__).parent / "models" / model_file
    return json.loads(path.read_text())

def predict(features: List[float]) -> Dict:
    model = load_model()
    coef = model["coef"]
    intercept = model["intercept"]

    y = sum(f * c for f, c in zip(features, coef)) + intercept
    return {
        "prediction": y,
        "model_name": model["model_name"],
        "model_version": model["model_version"],
    }
