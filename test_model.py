import pickle

# Load saved model
model = pickle.load(open("model.pkl", "rb"))
vectorizer = pickle.load(open("vectorizer.pkl", "rb"))

def predict_category(text):
    vec = vectorizer.transform([text])
    return model.predict(vec)[0]

# Test inputs
tests = [
    "paid 300 for pizza",
    "uber ride 200",
    "electricity bill 1500",
    "coffee at cafe 120",
    "metro ticket 50"
]

for t in tests:
    print(t, "→", predict_category(t))