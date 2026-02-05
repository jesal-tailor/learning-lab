from learning_lab.predict import predict

def test_predict_returns_model_version():
    out = predict([1.0, 2.0])
    assert "prediction" in out
    assert out["model_version"] == "1.0.0"
