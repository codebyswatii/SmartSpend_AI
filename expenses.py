from flask import Blueprint, request, jsonify, session
from analytics import generate_insights

from db import (
    insert_expense,
    get_all_expenses,
    delete_last_expense
)

from ml import (
    predict_category,
    extract_amount
)

expenses_bp = Blueprint("expenses", __name__)

# API route
@expenses_bp.route('/add', methods=['POST'])
def add_expense():
    data = request.json or {}
    text = data.get("text", "")
    # user_id = data.get("user_id", "")
    # user_id = session["user_id"]
    owner_id = session.get("user_id") or session.get("guest_id")

    category = predict_category(text)
    amount = extract_amount(text)
    insert_expense(owner_id, text, amount, category)

    return jsonify({
        "text": text,
        "category": category,
        "amount": amount
    })

@expenses_bp.route('/expenses', methods=['POST'])
def fetch_expenses():
    # data = request.json or {}
    # user_id = data.get("user_id","")

    # user_id = session["user_id"]
    owner_id = session.get("user_id") or session.get("guest_id")

    data = get_all_expenses(owner_id)
    return jsonify(data)

@expenses_bp.route('/delete', methods=['POST'])
def delete_expense():
    # data = request.json or {}
    # user_id = data.get("user_id","")
    # user_id = session["user_id"]
    owner_id = session.get("user_id") or session.get("guest_id")

    delete_last_expense(owner_id)

    return jsonify({"message": "Last expense deleted"})

@expenses_bp.route('/insights', methods=['POST'])
def insights():
    # data_json = request.json or {}
    # user_id = data_json.get("user_id","")

    # user_id = session["user_id"]
    owner_id = session.get("user_id") or session.get("guest_id")

    return jsonify(generate_insights(owner_id))

