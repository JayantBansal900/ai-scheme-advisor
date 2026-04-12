import sys
import joblib
import numpy as np
import json
import os

# 🔥 BASE PATH
BASE_DIR = os.path.dirname(__file__)

# 🔥 GLOBALS (LOAD ONCE)
model = None
occ_encoder = None
scheme_encoder = None


def load_models():
    global model, occ_encoder, scheme_encoder

    if model is None:
        try:
            model = joblib.load(os.path.join(BASE_DIR, "model.pkl"))
            occ_encoder = joblib.load(os.path.join(BASE_DIR, "occ_encoder.pkl"))
            scheme_encoder = joblib.load(os.path.join(BASE_DIR, "scheme_encoder.pkl"))
        except Exception:
            return False

    return True


# 🔥 INPUT HANDLING
def get_input():
    try:
        age = int(sys.argv[1])
        income = int(sys.argv[2])
        occupation = sys.argv[3]
    except:
        age = 20
        income = 200000
        occupation = "student"

    return age, income, occupation


# 🔥 ENCODING
def encode_occupation(occupation):
    try:
        return occ_encoder.transform([occupation])[0]
    except:
        return occ_encoder.transform(["student"])[0]


# 🔥 PREDICTION
def predict(age, income, occupation):
    try:
        occ = encode_occupation(occupation)
        X = np.array([[age, income, occ]])

        pred = model.predict(X)
        scheme = scheme_encoder.inverse_transform(pred)[0]

        return scheme

    except Exception:
        return "Not available"


# 🚀 MAIN
if __name__ == "__main__":
    try:
        if not load_models():
            print(json.dumps({"predicted_scheme": "Model loading failed"}))
            sys.exit(0)

        age, income, occupation = get_input()

        scheme = predict(age, income, occupation)

        print(json.dumps({
            "predicted_scheme": scheme
        }))

    except Exception:
        print(json.dumps({
            "predicted_scheme": "Not available"
        }))