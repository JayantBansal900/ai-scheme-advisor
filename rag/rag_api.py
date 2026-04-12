from fastapi import FastAPI
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
import pickle
import os
import joblib

app = FastAPI()

BASE_DIR = os.path.dirname(__file__)

print("🔥 Loading models...")

# =========================
# 🔥 LOAD EVERYTHING ONCE
# =========================

model = SentenceTransformer('all-MiniLM-L6-v2')
index = faiss.read_index(os.path.join(BASE_DIR, "scheme_index.faiss"))

with open(os.path.join(BASE_DIR, "schemes.pkl"), "rb") as f:
    schemes = pickle.load(f)

ml_model = joblib.load(os.path.join(BASE_DIR, "model.pkl"))
occ_encoder = joblib.load(os.path.join(BASE_DIR, "occ_encoder.pkl"))
scheme_encoder = joblib.load(os.path.join(BASE_DIR, "scheme_encoder.pkl"))

print("✅ FastAPI Ready 🚀")


# =========================
# 🔍 RAG SEARCH
# =========================

def search(query):
    query_embedding = model.encode([query], convert_to_numpy=True)

    # 🔥 FIXED HERE
    D, I = index.search(query_embedding, k=100)

    results = []

    for idx, i in enumerate(I[0]):
        try:
            if i >= len(schemes):
                continue

            s = schemes[i]

            results.append({
                "scheme_name": s.get("scheme_name", ""),
                "state": s.get("state", ""),
                "type": s.get("type", ""),
                "category": s.get("category", ""),
                "eligibility": s.get("eligibility", "")[:200],
                "benefits": s.get("benefits", "")[:200],
                "summary": f"Relevant to '{query}'"
            })
        except:
            continue

    # 🔥 RETURN MORE RESULTS
    return results[:20]


# =========================
# 🧠 ML PREDICT
# =========================

def predict(age, income, occupation):
    try:
        try:
            occ = occ_encoder.transform([occupation])[0]
        except:
            occ = occ_encoder.transform(["student"])[0]

        X = np.array([[age, income, occ]])
        pred = ml_model.predict(X)

        scheme = scheme_encoder.inverse_transform(pred)[0]
        return scheme

    except:
        return "Not available"


# =========================
# 🚀 MAIN API
# =========================

@app.post("/recommend")
def recommend(data: dict):
    query = data.get("query", "")
    age = data.get("age", 20)
    income = data.get("income", 200000)
    occupation = data.get("occupation", "student")
    category = data.get("category", "")
    state = data.get("state", "")
    type_ = data.get("type", "")

    final_query = " ".join(
        [str(x) for x in [query, category, state, type_] if x]
    )

    rag_results = search(final_query)
    predicted = predict(age, income, occupation)

    return {
        "predicted_scheme": predicted,
        "recommendations": rag_results
    }