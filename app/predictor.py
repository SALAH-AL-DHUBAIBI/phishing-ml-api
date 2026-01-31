import joblib
import numpy as np
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODELS_DIR = os.path.join(BASE_DIR, "models")

model = joblib.load(os.path.join(MODELS_DIR, "random_forest_model_full.pkl"))
scaler = joblib.load(os.path.join(MODELS_DIR, "scaler_full.pkl"))
label_encoder = joblib.load(os.path.join(MODELS_DIR, "label_encoder_full.pkl"))

def predict_label(features):
    X = np.array(features).reshape(1, -1)
    X_scaled = scaler.transform(X)
    pred = model.predict(X_scaled)
    label = label_encoder.inverse_transform(pred)
    return {"prediction": label[0]}
