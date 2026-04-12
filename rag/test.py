from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')

text = "government scheme for students"
embedding = model.encode(text)

print("✅ Working:", embedding[:5])