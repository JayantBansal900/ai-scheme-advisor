import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
import sys
import pickle
import os

# 🔥 BASE PATH
BASE_DIR = os.path.dirname(__file__)

# 🔥 GLOBAL CACHE
model = None
index = None
schemes = None

# =========================
# 🔥 LOAD FUNCTIONS (LAZY)
# =========================

def get_model():
    global model
    if model is None:
        model = SentenceTransformer('all-MiniLM-L6-v2')
    return model


def load_data():
    global index, schemes

    if index is None:
        index = faiss.read_index(os.path.join(BASE_DIR, "scheme_index.faiss"))

    if schemes is None:
        with open(os.path.join(BASE_DIR, "schemes.pkl"), "rb") as f:
            schemes = pickle.load(f)

# =========================
# 🧹 CLEAN TEXT
# =========================

def clean_text(text):
    if not text:
        return ""

    text = text.replace("\n", " ").strip()
    sentences = text.split(".")
    return ". ".join(sentences[:2]).strip() + "."

# =========================
# 🤖 SUMMARY
# =========================

def generate_summary(scheme, query):
    return f"Relevant to '{query}' in {scheme.get('category','general')} category."

# =========================
# 🔍 SEARCH ENGINE
# =========================

def search(query):
    if not query:
        return []

    load_data()
    model = get_model()

    query_lower = query.lower()

    try:
        # 🔥 EMBEDDING
        query_embedding = model.encode([query], convert_to_numpy=True)

        # 🔥 FAISS SEARCH (INCREASED)
        D, I = index.search(query_embedding, k=100)

    except Exception:
        return []

    results = []

    for idx, i in enumerate(I[0]):
        try:
            # ✅ safety check
            if i >= len(schemes):
                continue

            scheme = schemes[i]

            category = scheme.get("category", "").lower()
            tags = scheme.get("tags", "").lower()
            state = scheme.get("state", "").lower()
            scheme_type = scheme.get("type", "").lower()

            # =========================
            # 🎯 FILTERS
            # =========================

            # 🏛️ type filter
            if "central" in query_lower and scheme_type != "central":
                continue

            if "state" in query_lower and scheme_type != "state":
                continue

            # 🌍 state filter
            states = [
                "rajasthan","madhya pradesh","bihar","uttar pradesh",
                "karnataka","west bengal","chhattisgarh","goa","tamil nadu"
            ]

            if any(s in query_lower for s in states):
                if state not in query_lower:
                    continue

            # 🎓 keyword intent
            keywords_map = {
                "student": "education",
                "farmer": "agriculture",
                "women": "women",
                "health": "health",
                "startup": "entrepreneur"
            }

            skip = False
            for key, cat in keywords_map.items():
                if key in query_lower and cat not in category:
                    skip = True
                    break

            if skip:
                continue

            # =========================
            # 🧠 SCORING
            # =========================

            score = 0
            words = query_lower.split()

            for word in words:
                if word in tags:
                    score += 3
                if word in category:
                    score += 2
                if word in state:
                    score += 2

            # semantic boost
            dist = max(D[0][idx], 0)
            score += float(1 / (1 + dist))

            results.append((scheme, score))

        except Exception:
            continue

    # 🔥 SORT
    results = sorted(results, key=lambda x: x[1], reverse=True)

    # 🔥 RETURN TOP 20
    return [r[0] for r in results[:20]]

# =========================
# 🚀 MAIN
# =========================

if __name__ == "__main__":
    try:
        if len(sys.argv) < 2:
            print(json.dumps([]))
            sys.exit(0)

        query = sys.argv[1]
        results = search(query)

        output = []

        for r in results:
            output.append({
                "scheme_name": r.get("scheme_name", ""),
                "state": r.get("state", ""),
                "type": r.get("type", ""),
                "category": r.get("category", ""),
                "eligibility": clean_text(r.get("eligibility", "")),
                "benefits": clean_text(r.get("benefits", "")),
                "summary": generate_summary(r, query)
            })

        print(json.dumps(output))

    except Exception:
        print(json.dumps([]))