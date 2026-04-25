import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
import pickle

# Step 1: Load dataset
data = pd.read_csv("dataset.csv")

# Step 2: Split input and output
X = data["text"]
y = data["category"]

# Step 3: Convert text → numbers (NLP)
vectorizer = TfidfVectorizer()
X_vec = vectorizer.fit_transform(X)

# Step 4: Train ML model
model = MultinomialNB()
model.fit(X_vec, y)

# Step 5: Save model
pickle.dump(model, open("model.pkl", "wb"))
pickle.dump(vectorizer, open("vectorizer.pkl", "wb"))

print("Model trained and saved successfully!")