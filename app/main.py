from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import numpy as np

from feature_extractor import extract_features

app = FastAPI(title="Phishing Detection API")

model = joblib.load("model.pkl")
scaler = joblib.load("scaler.pkl")

class PredictionRequest(BaseModel):
    url: str

@app.get("/")
def root():
    return {"status": "API is running"}

@app.post("/predict")
def predict(request: PredictionRequest):
    features = extract_features(request.url)

    X = np.array(features).reshape(1, -1)
    X_scaled = scaler.transform(X)

    prediction = model.predict(X_scaled)[0]
    probability = model.predict_proba(X_scaled)[0].max()

    return {
        "url": request.url,
        "prediction": "phishing" if prediction == 1 else "legitimate",
        "confidence": round(float(probability), 4)
    }
