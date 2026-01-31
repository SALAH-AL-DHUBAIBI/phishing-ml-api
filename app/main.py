from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import numpy as np
import os

from feature_extraction import extract_features

app = FastAPI(title="Phishing Detection API")

# ---------- Request ----------
class URLRequest(BaseModel):
    url: str

# ---------- Load Models ----------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

model = joblib.load(os.path.join(BASE_DIR, "random_forest_model_full.pkl"))
scaler = joblib.load(os.path.join(BASE_DIR, "scaler_full.pkl"))
label_encoder = joblib.load(os.path.join(BASE_DIR, "label_encoder_full.pkl"))

# ---------- Routes ----------
@app.get("/")
def root():
    return {"status": "API is running successfully"}

@app.post("/predict-url")
def predict_url(data: URLRequest):
    features = extract_features(data.url)

    X = np.array(features).reshape(1, -1)
    X_scaled = scaler.transform(X)

    prediction = model.predict(X_scaled)
    label = label_encoder.inverse_transform(prediction)

    return {
        "url": data.url,
        "prediction": label[0]
    }
