import json
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
import joblib

# Load data
with open('../data/ml_data.json', 'r') as f:
    data = json.load(f)

# Prepare data
ages = [d["age"] for d in data]
incomes = [d["income"] for d in data]
occupations = [d["occupation"] for d in data]
schemes = [d["scheme"] for d in data]

# Encode categorical
occ_encoder = LabelEncoder()
scheme_encoder = LabelEncoder()

occ_encoded = occ_encoder.fit_transform(occupations)
scheme_encoded = scheme_encoder.fit_transform(schemes)

# Features
X = np.column_stack((ages, incomes, occ_encoded))
y = scheme_encoded

# Train model
model = RandomForestClassifier()
model.fit(X, y)

# Save everything
joblib.dump(model, "model.pkl")
joblib.dump(occ_encoder, "occ_encoder.pkl")
joblib.dump(scheme_encoder, "scheme_encoder.pkl")

print("✅ ML model trained and saved")