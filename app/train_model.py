# train_model.py
import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier

from feature_extractor import extract_features

# تحميل Dataset (مثال)
df = pd.read_csv("phishing_dataset.csv")  # يحتوي url,label

X = df["url"].apply(extract_features).tolist()
y = df["label"]

# Scaling
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Model
model = RandomForestClassifier(
    n_estimators=200,
    random_state=42
)
model.fit(X_scaled, y)

# حفظ الملفات
joblib.dump(model, "model.pkl")
joblib.dump(scaler, "scaler.pkl")

print("✅ Model & Scaler trained and saved successfully")
