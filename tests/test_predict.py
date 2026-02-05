import os
from learning_lab.predict import predict

def test_predict_returns_model_version():
    out = predict([1.0, 2.0])
    assert "prediction" in out
    assert out["model_version"] == "1.0.0"

def test_predict_default_model():
    out = predict([1.0, 2.0])
    assert out["model_version"] == "1.0.0"

def test_predict_canary_model(monkeypatch):
    monkeypatch.setenv("MODEL_VERSION", "1.0.1")
    out = predict([1.0, 2.0])
    assert out["model_version"] == "1.0.1"