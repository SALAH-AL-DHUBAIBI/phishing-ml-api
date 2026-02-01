@app.post("/predict")
def predict(data: FeaturesRequest):
    X = np.array(data.features).reshape(1, -1)
    X_scaled = scaler.transform(X)

    prediction = model.predict(X_scaled)
    label = label_encoder.inverse_transform(prediction)

    return {
        "prediction": label[0]
    }
