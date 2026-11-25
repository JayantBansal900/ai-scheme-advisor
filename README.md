# 🚀 AI Government Scheme Advisor
[![CI](https://github.com/JayantBansal900/ai-scheme-advisor/actions/workflows/ci.yml/badge.svg)](https://github.com/JayantBansal900/ai-scheme-advisor/actions/workflows/ci.yml)

An AI-powered Government Scheme Recommendation System that helps users discover the most relevant central and state schemes using Machine Learning and Retrieval-Augmented Generation (RAG).

---

## 📌 Project Overview

This project combines **Machine Learning + Semantic Search (FAISS) + RAG** to provide intelligent recommendations for government schemes based on user queries and filters.

🔍 Users can:

* Search schemes using natural language
* Filter by category, state, and type
* Get AI-predicted scheme recommendations
* View detailed eligibility & benefits

---

## 🧠 Tech Stack

### 🔹 Frontend

* React.js
* Tailwind CSS

### 🔹 Backend

* Node.js (Express)

### 🔹 AI / ML Layer

* FastAPI (Python)
* Scikit-learn (ML Model)
* FAISS (Vector Search)
* Sentence Transformers (Embeddings)

---

## ⚙️ Architecture

```
User (React Frontend)
        ↓
Node.js Backend (API Gateway)
        ↓
FastAPI (AI Engine)
        ↓
FAISS + ML Model
```

---

## 📁 Project Structure

```
ai-scheme-advisor/
│
├── frontend/   # React UI
├── backend/    # Node API
├── rag/        # FastAPI + RAG + ML
├── data/       # Dataset files
```

---

## 🔍 Features

* ✅ AI-based scheme prediction
* ✅ Semantic search using FAISS
* ✅ State & category filtering
* ✅ Central vs State scheme filtering
* ✅ Fast response using caching
* ✅ Clean UI with Tailwind
* ✅ Modern UI with background image

---

## 🧠 AI Concepts Used

* Retrieval-Augmented Generation (RAG)
* Vector Search (FAISS)
* Sentence Embeddings (MiniLM)
* Machine Learning Classification

---

## 📊 Dataset

Each scheme contains:

```json
{
  "scheme_name": "",
  "description": "",
  "benefits": "",
  "eligibility": "",
  "category": "",
  "tags": "",
  "state": "",
  "type": "state | central"
}
```

---

## ⚡ How It Works

1. User enters query
2. Backend sends request to FastAPI
3. ML model predicts best scheme
4. FAISS retrieves similar schemes
5. Filters applied (state/category/type)
6. Top results returned to UI

---

## 🚀 Installation (Local Setup)

### 1️⃣ Clone Repo

```bash
git clone https://github.com/yourusername/ai-scheme-advisor.git
cd ai-scheme-advisor
```

---

### 2️⃣ Setup Backend

```bash
cd backend
npm install
node server.js
```

---

### 3️⃣ Setup Frontend

```bash
cd frontend
npm install
npm start
```

---

### 4️⃣ Setup FastAPI (AI Engine)

```bash
cd rag
pip install -r requirements.txt
uvicorn rag_api:app --reload
```

---

## 🌐 API Endpoint

### POST `/recommend`

```json
{
  "query": "student scholarship",
  "category": "education",
  "state": "rajasthan",
  "type": "central"
}
```

---

## ⚠️ Limitations

* Initial load may be slow (model loading)
* No authentication system
* No pagination (top results only)

---

## 🚀 Future Improvements

* Chatbot interface 🤖
* Voice search 🎤
* User login & personalization
* Deployment optimization
* Better UI animations

---

## 💡 Learning Outcomes

* Built full-stack AI system
* Integrated Node ↔ Python
* Implemented RAG pipeline
* Used FAISS for semantic search
* Optimized performance with caching

---

## 👨‍💻 Author

**Jayant Bansal**

---

## ⭐ Support

If you like this project, give it a ⭐ on GitHub!
