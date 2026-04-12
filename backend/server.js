const express = require("express");
const cors = require("cors");
const axios = require("axios");

const app = express();

app.use(cors());
app.use(express.json());

// 🔥 TEMP: disable cache for debugging
const USE_CACHE = false;
const cache = new Map();

app.get("/", (req, res) => {
  res.send("Backend running with FastAPI 🚀");
});

app.post("/recommend", async (req, res) => {
  try {
    const { query, category, state, type } = req.body;

    if (!query) {
      return res.status(400).json({ error: "Query is required" });
    }

    const finalQuery = [query, category, state, type]
      .filter(v => v && v !== "All")
      .join(" ");

    const cacheKey = finalQuery.toLowerCase();

    console.log("Incoming:", finalQuery);

    // ✅ CACHE (optional)
    if (USE_CACHE && cache.has(cacheKey)) {
      console.log("⚡ Cache hit");
      return res.json(cache.get(cacheKey));
    }

    // 🚀 CALL FASTAPI
    const response = await axios.post(
      "http://127.0.0.1:8000/recommend",
      req.body,
      { timeout: 20000 }
    );

    const data = response.data;

    if (USE_CACHE) {
      cache.set(cacheKey, data);
    }

    res.json(data);

  } catch (error) {
    console.error("❌ FULL ERROR:", error?.response?.data || error.message);

    res.status(500).json({
      error: "FastAPI request failed",
      details: error?.response?.data || error.message
    });
  }
});

app.listen(5000, () => {
  console.log("Server running on port 5000 🚀");
});