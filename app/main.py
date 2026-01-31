from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import numpy as np
import os

app = FastAPI(title="Phishing Detection API")

# =========================
# Request Model
# =========================
class PredictionRequest(BaseModel):
    features: list[float]

# =========================
# Paths (IMPORTANT)
# =========================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODELS_DIR = os.path.join(BASE_DIR, "models")

model = joblib.load(os.path.join(MODELS_DIR, "random_forest_model_full.pkl"))
scaler = joblib.load(os.path.join(MODELS_DIR, "scaler_full.pkl"))
label_encoder = joblib.load(os.path.join(MODELS_DIR, "label_encoder_full.pkl"))

# =========================
# Routes
# =========================
@app.get("/")
def root():
    return {"status": "API is running successfully"}

@app.post("/predict")
def predict(data: PredictionRequest):
    X = np.array(data.features).reshape(1, -1)
    X_scaled = scaler.transform(X)
    prediction = model.predict(X_scaled)
    label = label_encoder.inverse_transform(prediction)

    return {
        "prediction": label[0]
    }

# =========================
# Local / Colab Run
# =========================
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
