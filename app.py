from flask import Flask, request
from flask import jsonify
from db import init_db, insert_expense, get_all_expenses, delete_last_expense, insert_user, get_user_by_email
from flask import render_template
from flask import session, redirect
from werkzeug.security import generate_password_hash, check_password_hash

from dotenv import load_dotenv

from auth import auth_bp

from ml import predict_category, extract_amount

from expenses import expenses_bp

import uuid
import pickle
import re
import os

load_dotenv()

app = Flask(__name__)

# app.secret_key = os.environ.get("SECRET_KEY") or "dev_key_123"
app.secret_key = os.environ.get("SECRET_KEY")
init_db()

app.register_blueprint(auth_bp)
app.register_blueprint(expenses_bp)

@app.route('/')
def home():
    return render_template("landing.html")

@app.before_request
def set_user():
    # if "user_id" not in session:
    #     session["user_id"] = str(uuid.uuid4())

    if "guest_id" not in session:
        session["guest_id"] = str(uuid.uuid4())

@app.route('/demo')
def demo():
    text = "paid 300 for pizza"
    return {
        "category": predict_category(text),
        "amount": extract_amount(text)
    }


# @app.route('/expenses', methods=['POST'])
# def fetch_expenses():
#     # data = request.json or {}
#     # user_id = data.get("user_id","")

#     user_id = session["user_id"]

#     data = get_all_expenses(user_id)
#     return jsonify(data)

# @app.route('/add-test')
# def add_test():
#     text = "pizza 300"
#     text = "uber ride 200"
#     text = "electricity bill 1000"
#     text = "pizza 300"
    
#     category = predict_category(text)
#     amount = extract_amount(text)
    
#     insert_expense(text, amount, category)
    
#     return {
#         "text": text,
#         "category": category,
#         "amount": amount
#     }

# @app.route('/delete', methods=['POST'])
# def delete_expense():
#     # data = request.json or {}
#     # user_id = data.get("user_id","")
#     user_id = session["user_id"]

#     delete_last_expense(user_id)

#     return jsonify({"message": "Last expense deleted"})

# @app.route('/insights', methods=['POST'])
# def insights():
#     # data_json = request.json or {}
#     # user_id = data_json.get("user_id","")

#     user_id = session["user_id"]

#     data = get_all_expenses(user_id)

#     if not data:
#         return jsonify({
#         "total_spent": 0,
#         "category_distribution": {},
#         "insights": []
#     })

#     total = 0
#     category_sum = {}

#     for row in data:
#         try:
#             amount = int(row[3])
#         except:
#             amount = 0
    
#         category = row[4]

#         total += amount

#         if category not in category_sum:
#             category_sum[category] = 0

#         category_sum[category] += amount

#     # Calculate percentages
#     result = {}
#     insights = []

#     for cat, amt in category_sum.items():
#         percent = (amt / total) * 100 if total != 0 else 0
#         result[cat] = round(percent, 2)

#         if percent > 50:
#             insights.append(f"High spending on {cat}")
#         elif percent > 30:
#             insights.append(f"Moderate spending on {cat}")
#         else:
#             insights.append(f"Low spending on {cat}")

#     # 🔥 Anomaly Detection (NEW CODE)
#     # for row in data:
#     #     amount = row[2]
        
#     #     if amount > 2000:
#     #         insights.append(f"Unusually high expense detected: ₹{amount}")
#     # 🔥 Smarter Anomaly Detection
#     amounts = [int(row[3]) if str(row[3]).isdigit() else 0 for row in data]
#     avg = sum(amounts) / len(amounts)

#     for row in data:
#         amount = int(row[3])
        
#         if amount > avg * 2:
#             insights.append(f"Unusual high expense detected: ₹{amount}")

#     if "bills" in result and result["bills"] > 50:
#             insights.append("High fixed expenses may reduce savings")

#     return jsonify({
#         "total_spent": total,
#         "category_distribution": result,
#         "insights": insights
#     })

# Load ML model
# model = pickle.load(open("model.pkl", "rb"))
# vectorizer = pickle.load(open("vectorizer.pkl", "rb"))

# # Function: predict category
# def predict_category(text):

#     text_lower = text.lower()

#     # 🔥 Rule-based override (important words)
#     if "trip" in text_lower or "travel" in text_lower:
#         return "travel"
#     if "rent" in text_lower or "bill" in text_lower:
#         return "bills"

#     if "flight" in text_lower or "hotel" in text_lower:
#         return "travel"

#     print(text)
#     vec = vectorizer.transform([text])
#     return model.predict(vec)[0]

# # Function: extract amount
# def extract_amount(text):
#     numbers = re.findall(r'\d+', text)
#     return int(numbers[0]) if numbers else 0

# API route
# @app.route('/add', methods=['POST'])
# def add_expense():
#     data = request.json or {}
#     text = data.get("text", "")
#     # user_id = data.get("user_id", "")
#     user_id = session["user_id"]

#     category = predict_category(text)
#     amount = extract_amount(text)
#     insert_expense(user_id, text, amount, category)

#     return jsonify({
#         "text": text,
#         "category": category,
#         "amount": amount
#     })

# @app.route("/register", methods=["POST"])
# def register():

#     data = request.json

#     username = data.get("username", "").strip()
#     email = data.get("email", "").strip().lower()
#     password = data.get("password", "")

#     if not username or not email or not password:
#         return jsonify({
#             "message": "All fields are required."
#         }), 400

#     existing_user = get_user_by_email(email)

#     if existing_user:
#         return jsonify({
#             "message": "Email already registered."
#         }), 409

#     password_hash = generate_password_hash(password)

#     insert_user(username, email, password_hash)

#     return jsonify({
#         "message": "Registration successful."
#     }), 201

# @app.route("/login", methods=["POST"])
# def login():

#     data = request.json

#     email = data.get("email", "").strip().lower()
#     password = data.get("password", "")

#     if not email or not password:
#         return jsonify({
#             "message": "Email and password are required."
#         }), 400

#     user = get_user_by_email(email)

#     if not user:
#         return jsonify({
#             "message": "Invalid email or password."
#         }), 401

#     if not check_password_hash(user[3], password):
#         return jsonify({
#             "message": "Invalid email or password."
#         }), 401

#     session["user_id"] = str(user[0])

#     return jsonify({
#         "message": "Login successful.",
#         "username": user[1]
#     }), 200

@app.route("/session")
def session_test():
    return jsonify(dict(session))

# @app.route("/logout", methods=["POST"])
# def logout():

#     session.clear()

#     return jsonify({
#         "message": "Logged out successfully."
#     })

@app.route("/login-page")
def login_page():
    return render_template("login.html")

@app.route("/register-page")
def register_page():
    return render_template("register.html")

# @app.route("/dashboard")
# def dashboard():
#     if "user_id" not in session and "guest_id" not in session:
#         return redirect("/login-page")

#     return render_template("dashboard.html")

@app.route("/dashboard")
def dashboard():

    if "user_id" not in session and "guest_id" not in session:
        return redirect("/login-page")

    username = session.get("username", "Guest")

    return render_template(
        "dashboard.html",
        username=username
    )


if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000)

