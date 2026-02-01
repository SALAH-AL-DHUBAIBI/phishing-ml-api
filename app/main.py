from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import pandas as pd
import numpy as np
import os

from feature_extractor import FeatureExtractor

print("🔥 NEW VERSION LOADED - URL INPUT 🔥")


app = FastAPI(title="Phishing Detection API")

# ---------- Request Model ----------
class PredictionRequest(BaseModel):
    url: str

# ---------- Paths ----------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ---------- Load Artifacts ----------
model = joblib.load(os.path.join(BASE_DIR, "random_forest_model_full.pkl"))
scaler = joblib.load(os.path.join(BASE_DIR, "scaler_full.pkl"))
label_encoder = joblib.load(os.path.join(BASE_DIR, "label_encoder_full.pkl"))
selected_features = joblib.load(os.path.join(BASE_DIR, "feature_info_full.pkl"))

extractor = FeatureExtractor()

# ---------- Routes ----------
@app.get("/")
def root():
    return {"status": "API is running successfully"}

@app.post("/predict")
def predict(data: PredictionRequest):
    try:
        # 1️⃣ Feature Extraction
        features = extractor.extract(data.url)

        # 2️⃣ Convert to DataFrame
        df = pd.DataFrame([features])

        # 3️⃣ Ensure feature consistency
        missing_features = set(selected_features) - set(df.columns)
        if missing_features:
            return {
                "error": "Feature mismatch",
                "missing_features": list(missing_features)
            }

        df = df[selected_features]

        # 4️⃣ Scaling
        X_scaled = scaler.transform(df.values)

        # 5️⃣ Prediction
        prediction = model.predict(X_scaled)
        probabilities = model.predict_proba(X_scaled)[0]

        label = label_encoder.inverse_transform(prediction)[0]

        return {
            "url": data.url,
            "prediction": label,
            "confidence": {
                "legitimate": float(probabilities[0]),
                "phishing": float(probabilities[1])
            }
        }

    except Exception as e:
        return {
            "error": "Internal Server Error",
            "details": str(e),
            "exception_type": type(e).__name__
        }
