import json
import re

# 📂 Load dataset
with open("../data/schemes.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# 🧠 State list
states = [
    "andhra pradesh", "arunachal pradesh", "assam", "bihar",
    "chhattisgarh", "goa", "gujarat", "haryana", "himachal pradesh",
    "jharkhand", "karnataka", "kerala", "madhya pradesh",
    "maharashtra", "manipur", "meghalaya", "mizoram", "nagaland",
    "odisha", "punjab", "rajasthan", "sikkim", "tamil nadu",
    "telangana", "tripura", "uttar pradesh", "uttarakhand",
    "west bengal", "delhi"
]

# 🧠 Keywords for central schemes
central_keywords = [
    "ministry", "government of india", "central sector",
    "pm ", "pradhan mantri", "national scheme"
]

def detect_state(text):
    text = text.lower()

    for state in states:
        if state in text:
            return state.title()

    return None

def detect_type(text):
    text = text.lower()

    for word in central_keywords:
        if word in text:
            return "central"

    return "state"


# 🔥 PROCESS
for scheme in data:
    full_text = (
        str(scheme.get("scheme_name", "")) + " " +
        str(scheme.get("description", "")) + " " +
        str(scheme.get("eligibility", ""))
    )

    state = detect_state(full_text)

    if state:
        scheme["state"] = state
        scheme["type"] = "state"
    else:
        scheme["state"] = "India"
        scheme["type"] = detect_type(full_text)

# 💾 SAVE NEW FILE
with open("../data/schemes_updated.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2)

print("✅ Dataset updated successfully!")