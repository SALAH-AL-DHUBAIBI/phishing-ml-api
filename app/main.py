@app.post("/predict")
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
