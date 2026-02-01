# main.py
from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import pandas as pd
import os

from feature_extractor import AdvancedURLFeatureExtractor

# -------------------------
# تحميل الملفات
# -------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

model = joblib.load(os.path.join(BASE_DIR, "random_forest_model_full.pkl"))
scaler = joblib.load(os.path.join(BASE_DIR, "scaler_full.pkl"))
label_encoder = joblib.load(os.path.join(BASE_DIR, "label_encoder_full.pkl"))

feature_info = joblib.load(os.path.join(BASE_DIR, "feature_info_full.pkl"))
selected_features = feature_info["selected_features"]

extractor = AdvancedURLFeatureExtractor()

# -------------------------
# FastAPI App
# -------------------------
app = FastAPI(
    title="Phishing Detection API",
    description="ML API for detecting phishing URLs",
    version="1.0"
)

# -------------------------
# Request Model
# -------------------------
class PredictionRequest(BaseModel):
    url: str

# -------------------------
# Routes
# -------------------------
@app.get("/")
def root():
    return {"status": "API is running"}

@app.post("/predict")
def predict(data: PredictionRequest):

    # 1) استخراج الميزات
    features = extractor.extract(data.url)

    # 2) DataFrame
    df = pd.DataFrame([features])

    # 3) اختيار نفس الميزات التي دُرب عليها النموذج
    df_selected = df[selected_features]

    # 4) تطبيع
    X_scaled = scaler.transform(df_selected.values)

    # 5) تنبؤ
    pred = model.predict(X_scaled)
    label = label_encoder.inverse_transform(pred)

    return {
        "url": data.url,
        "prediction": label[0]
    }
