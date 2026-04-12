# build_index.py (FINAL)

import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
import pickle

model = SentenceTransformer('all-MiniLM-L6-v2')

with open('../data/schemes.json', 'r', encoding='utf-8') as f:
    schemes = json.load(f)

texts = []

for s in schemes:
    text = f"""
    {s.get('scheme_name','')}
    {s.get('description','')}
    {s.get('eligibility','')}
    {s.get('benefits','')}
    {s.get('category','')}
    {s.get('tags','')}
    {s.get('state','')}
    {s.get('type','')}
    """
    texts.append(text.strip())

print("Generating embeddings... ⏳")

embeddings = model.encode(texts, convert_to_numpy=True, show_progress_bar=True)

index = faiss.IndexFlatL2(embeddings.shape[1])
index.add(embeddings)

faiss.write_index(index, "scheme_index.faiss")

with open("schemes.pkl", "wb") as f:
    pickle.dump(schemes, f)

print("✅ Index built successfully!")