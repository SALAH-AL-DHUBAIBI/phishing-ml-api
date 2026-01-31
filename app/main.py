from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import numpy as np
from pathlib import Path

# ================================
# إعداد التطبيق
# ================================
app = FastAPI(title="Phishing Detection API")

# ================================
# تحديد مسار مجلد المشروع
# ================================
BASE_DIR = Path(__file__).resolve().parent.parent
MODELS_DIR = BASE_DIR / "app" / "models"

# ================================
# تحميل النموذج والملفات المساعدة
# ================================
model = joblib.load(MODELS_DIR / "random_forest_model_full.pkl")
scaler = joblib.load(MODELS_DIR / "scaler_full.pkl")
label_encoder = joblib.load(MODELS_DIR / "label_encoder_full.pkl")

# ================================
# نموذج الطلب (Request Schema)
# ================================
class PredictionRequest(BaseModel):
    features: list

# ================================
# Endpoint فحص حالة الـ API
# ================================
@app.get("/")
def root():
    return {"status": "API is running successfully"}

# ================================
# Endpoint التنبؤ
# ================================
@app.post("/predict")
def predict(data: PredictionRequest):
    X = np.array(data.features).reshape(1, -1)
    X_scaled = scaler.transform(X)
    prediction = model.predict(X_scaled)
    label = label_encoder.inverse_transform(prediction)

    return {
        "prediction": label[0]
    }
