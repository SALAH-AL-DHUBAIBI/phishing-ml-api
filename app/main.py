from fastapi import FastAPI
from app.schemas import PredictionRequest
from app.predictor import predict_label

app = FastAPI(title="Phishing Detection API")

@app.get("/")
def root():
    return {"status": "API is running successfully"}

@app.post("/predict")
def predict(data: PredictionRequest):
    return predict_label(data.features)
