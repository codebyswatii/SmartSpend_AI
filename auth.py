from flask import Blueprint, request, jsonify, session
from werkzeug.security import generate_password_hash, check_password_hash

from db import insert_user, get_user_by_email

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register", methods=["POST"])
def register():

    data = request.json

    username = data.get("username", "").strip()
    email = data.get("email", "").strip().lower()
    password = data.get("password", "")

    if not username or not email or not password:
        return jsonify({
            "message": "All fields are required."
        }), 400

    existing_user = get_user_by_email(email)

    if existing_user:
        return jsonify({
            "message": "Email already registered."
        }), 409

    password_hash = generate_password_hash(password)

    insert_user(username, email, password_hash)

    return jsonify({
        "message": "Registration successful."
    }), 201

@auth_bp.route("/login", methods=["POST"])
def login():

    data = request.json

    email = data.get("email", "").strip().lower()
    password = data.get("password", "")

    if not email or not password:
        return jsonify({
            "message": "Email and password are required."
        }), 400

    user = get_user_by_email(email)

    if not user:
        return jsonify({
            "message": "Invalid email or password."
        }), 401

    if not check_password_hash(user[3], password):
        return jsonify({
            "message": "Invalid email or password."
        }), 401

    session["user_id"] = str(user[0])
    session["username"] = user[1]

    return jsonify({
        "message": "Login successful.",
        "username": user[1]
    }), 200

@auth_bp.route("/logout", methods=["POST"])
def logout():

    session.clear()

    return jsonify({
        "message": "Logged out successfully."
    })