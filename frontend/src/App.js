import { useState } from "react";
import bg from "./assets/bg.png";

function App() {
  const [query, setQuery] = useState("");
  const [category, setCategory] = useState("");
  const [state, setState] = useState("");
  const [type, setType] = useState("");
  const [results, setResults] = useState([]);
  const [predicted, setPredicted] = useState("");
  const [loading, setLoading] = useState(false);

  const statesList = [
    "andhra pradesh","arunachal pradesh","assam","bihar","chhattisgarh",
    "goa","gujarat","haryana","himachal pradesh","jharkhand","karnataka",
    "kerala","madhya pradesh","maharashtra","manipur","meghalaya",
    "mizoram","nagaland","odisha","punjab","rajasthan","sikkim",
    "tamil nadu","telangana","tripura","uttar pradesh","uttarakhand",
    "west bengal","delhi"
  ];

  const formatState = (st) =>
    st.split(" ").map(w => w[0].toUpperCase() + w.slice(1)).join(" ");

  const handleSearch = async () => {
    if (!query.trim()) return;
    setLoading(true);

    try {
      const res = await fetch("http://localhost:5000/recommend", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          age: 20,
          income: 200000,
          occupation: "student",
          query,
          category,
          state,
          type
        })
      });

      if (!res.ok) throw new Error("API failed");

      const data = await res.json();

      setPredicted(data.predicted_scheme || "");
      setResults(data.recommendations || []);

    } catch (error) {
      console.error(error);
      setResults([]);
      setPredicted("");
    }

    setLoading(false);
  };

  return (
    <div
      className="min-h-screen w-full relative font-sans pb-12 bg-fixed"
      style={{
        backgroundImage: `url(${bg})`,
        backgroundSize: "cover",        // 🔥 FULL SCREEN COVER
        backgroundPosition: "center",   // 🔥 CENTER FIX
        backgroundRepeat: "no-repeat",  // 🔥 NO REPEAT
        minHeight: "100vh"
      }}
    >
      {/* 🔥 OVERLAY */}
      <div className="absolute inset-0 bg-black/40"></div>

      <div className="relative z-10 text-slate-900">

        {/* NAVBAR */}
        <nav className="sticky top-0 z-50 bg-white/80 backdrop-blur-md border-b border-slate-200">
          <div className="max-w-7xl mx-auto px-6 h-16 flex items-center justify-between">
            <div className="flex items-center gap-2">
              <span className="text-2xl">🤖</span>
              <span className="font-bold text-xl tracking-tight bg-gradient-to-r from-indigo-600 to-blue-500 bg-clip-text text-transparent">
                SchemeAI
              </span>
            </div>
            <div className="hidden md:flex gap-6 text-sm font-medium text-slate-600">
              <span className="hover:text-indigo-600 cursor-pointer transition">Home</span>
              <span className="hover:text-indigo-600 cursor-pointer transition">About RAG</span>
              <span className="hover:text-indigo-600 cursor-pointer transition">Support</span>
            </div>
          </div>
        </nav>

        {/* HERO */}
        <div className="bg-transparent py-12 px-6">
          <div className="max-w-4xl mx-auto text-center">

            <h1 className="text-4xl md:text-5xl font-extrabold text-white mb-4 tracking-tight">
              Find the Right <span className="text-indigo-300">Government Schemes</span>
            </h1>

            <p className="text-lg text-gray-200 mb-8 max-w-2xl mx-auto">
              Our AI-powered engine uses ML and RAG to match you with the best central and state benefits in seconds.
            </p>

            {/* SEARCH */}
            <div className="bg-white p-2 rounded-2xl shadow-2xl flex flex-wrap md:flex-nowrap gap-2 items-center">
              
              <input
                type="text"
                placeholder="What are you looking for? (e.g. Scholarship)"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                onKeyDown={(e) => e.key === "Enter" && handleSearch()}
                className="flex-grow p-4 outline-none text-slate-700 bg-transparent min-w-[200px]"
              />

              <div className="flex flex-wrap gap-2 p-2">

                <select
                  value={category}
                  onChange={(e) => setCategory(e.target.value)}
                  className="p-3 bg-slate-50 rounded-xl text-sm"
                >
                  <option value="">Categories</option>
                  <option value="education">🎓 Education</option>
                  <option value="agriculture">🌾 Agriculture</option>
                  <option value="women">👩 Women</option>
                  <option value="startup">🚀 Startup</option>
                  <option value="health">🏥 Health</option>
                </select>

                <select
                  value={state}
                  onChange={(e) => setState(e.target.value)}
                  className="p-3 bg-slate-50 rounded-xl text-sm max-w-[150px]"
                >
                  <option value="">All States</option>
                  <option value="india">🇮🇳 All India</option>
                  {statesList.map((st) => (
                    <option key={st} value={st}>{formatState(st)}</option>
                  ))}
                </select>

                <select
                  value={type}
                  onChange={(e) => setType(e.target.value)}
                  className="p-3 bg-slate-50 rounded-xl text-sm"
                >
                  <option value="">All</option>
                  <option value="central">Central</option>
                  <option value="state">State</option>
                </select>

                <button
                  onClick={handleSearch}
                  disabled={loading}
                  className="bg-indigo-600 text-white px-8 py-3 rounded-xl font-bold hover:bg-indigo-700 transition"
                >
                  {loading ? "..." : "Search"}
                </button>

              </div>
            </div>

            {/* TAGS */}
            <div className="flex flex-wrap justify-center gap-2 mt-6">
              {["student", "farmer", "women", "startup", "health"].map((item) => (
                <button
                  key={item}
                  onClick={() => setQuery(item)}
                  className="px-4 py-1.5 bg-white border rounded-full text-sm hover:text-indigo-600"
                >
                  #{item}
                </button>
              ))}
            </div>

          </div>
        </div>

        {/* RESULTS */}
        <main className="max-w-7xl mx-auto px-6 py-10">

          {predicted && !loading && (
            <div className="mb-8 flex justify-center">
              <div className="bg-emerald-50 px-6 py-3 rounded-2xl flex gap-3">
                <span className="text-emerald-600 font-bold">🎯 AI Top Pick:</span>
                <span>{predicted}</span>
              </div>
            </div>
          )}

          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
            {results.map((item, index) => (
              <div key={index} className="bg-white p-6 rounded-3xl shadow-sm hover:shadow-xl transition">

                <h3 className="text-xl font-bold mb-3">{item.scheme_name}</h3>

                <p>📍 {item.state}</p>
                <p>🏛️ {item.type}</p>

                <p className="mt-2 text-sm">
                  <strong>Eligibility:</strong> {item.eligibility}
                </p>

                <p className="mt-2 text-sm">
                  <strong>Benefits:</strong> {item.benefits}
                </p>

                <p className="text-xs mt-2 text-gray-500">
                  🤖 {item.summary}
                </p>

              </div>
            ))}
          </div>

        </main>

      </div>
    </div>
  );
}

export default App;