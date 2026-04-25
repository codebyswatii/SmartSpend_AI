from flask import Flask, request
from flask import jsonify
from db import init_db, insert_expense, get_all_expenses
from flask import render_template
import pickle
import re

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/demo')
def demo():
    text = "paid 300 for pizza"
    return {
        "category": predict_category(text),
        "amount": extract_amount(text)
    }



@app.route('/expenses', methods=['GET'])
def get_expenses():
    data = get_all_expenses()
    return jsonify(data)


@app.route('/add-test')
def add_test():
    text = "pizza 300"
    text = "uber ride 200"
    text = "electricity bill 1000"
    text = "pizza 300"
    
    category = predict_category(text)
    amount = extract_amount(text)
    
    insert_expense(text, amount, category)
    
    return {
        "text": text,
        "category": category,
        "amount": amount
    }


@app.route('/insights', methods=['GET'])
def insights():
    data = get_all_expenses()

    if not data:
        return jsonify({
        "total_spent": 0,
        "category_distribution": {},
        "insights": []
    })

    total = 0
    category_sum = {}

    for row in data:
        amount = row[2]
        category = row[3]

        total += amount

        if category not in category_sum:
            category_sum[category] = 0

        category_sum[category] += amount

    # Calculate percentages
    result = {}
    insights = []

    for cat, amt in category_sum.items():
        percent = (amt / total) * 100
        result[cat] = round(percent, 2)

        if percent > 50:
            insights.append(f"High spending on {cat}")
        elif percent > 30:
            insights.append(f"Moderate spending on {cat}")
        else:
            insights.append(f"Low spending on {cat}")

    # 🔥 Anomaly Detection (NEW CODE)
    # for row in data:
    #     amount = row[2]
        
    #     if amount > 2000:
    #         insights.append(f"Unusually high expense detected: ₹{amount}")
    # 🔥 Smarter Anomaly Detection
    amounts = [row[2] for row in data]
    avg = sum(amounts) / len(amounts)

    for row in data:
        amount = row[2]
        
        if amount > avg * 2:
            insights.append(f"Unusual high expense detected: ₹{amount}")

    if "bills" in result and result["bills"] > 50:
            insights.append("High fixed expenses may reduce savings")

    return jsonify({
        "total_spent": total,
        "category_distribution": result,
        "insights": insights
    })

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

# API route
@app.route('/add', methods=['POST'])
def add_expense():
    data = request.json
    text = data.get("text", "")

    category = predict_category(text)
    amount = extract_amount(text)
    insert_expense(text, amount, category)

    return jsonify({
        "text": text,
        "category": category,
        "amount": amount
    })

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000)

