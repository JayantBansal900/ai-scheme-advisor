import pandas as pd
import json

# 📁 Load CSV file
df = pd.read_csv("../data/updated_data.csv")

# 🧹 Rename columns (IMPORTANT)
df = df.rename(columns={
    "details": "description",
    "schemeCategory": "category"
})

# 🧹 Select only needed columns
columns_needed = [
    "scheme_name",
    "description",
    "benefits",
    "eligibility",
    "category",
    "tags"
]

df = df[columns_needed]

# 🧹 Handle missing values
df = df.fillna("")

# 🔥 Convert to JSON
data = df.to_dict(orient="records")

# 💾 Save JSON file
with open("../data/schemes.json", "w") as f:
    json.dump(data, f, indent=2)

print("✅ JSON file created successfully!")