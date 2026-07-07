import pickle
import re

# Load ML model
model = pickle.load(open("model.pkl", "rb"))
vectorizer = pickle.load(open("vectorizer.pkl", "rb"))

# Function: predict category
def predict_category(text):

    text_lower = text.lower()

    # 🔥 Rule-based override (important words)
    if "trip" in text_lower or "travel" in text_lower:
        return "travel"
    if "rent" in text_lower or "bill" in text_lower:
        return "bills"

    if "flight" in text_lower or "hotel" in text_lower:
        return "travel"

    print(text)
    vec = vectorizer.transform([text])
    return model.predict(vec)[0]

# Function: extract amount
def extract_amount(text):
    numbers = re.findall(r'\d+', text)
    return int(numbers[0]) if numbers else 0

