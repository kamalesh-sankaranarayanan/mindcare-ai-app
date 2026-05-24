from flask import Flask, render_template, request, redirect, url_for, jsonify, session
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
from openai import OpenAI

import firebase_admin
from firebase_admin import credentials, db

import os
import json

# ---------------- LOAD ENV ----------------
load_dotenv()

# ---------------- FLASK APP ----------------
app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "change-this-secret-key")

# ---------------- OPENROUTER AI ----------------
client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)

# ---------------- FIREBASE INIT (FIXED) ----------------
firebase_app = None

def init_firebase():

    global firebase_app

    if firebase_admin._apps:
        return firebase_admin.get_app()

    firebase_env = os.getenv("FIREBASE_CONFIG")
    db_url = os.getenv("FIREBASE_DATABASE_URL")

    if not firebase_env:
        raise Exception("FIREBASE_CONFIG missing in Render environment variables")

    if not db_url:
        raise Exception("FIREBASE_DATABASE_URL missing in Render environment variables")

    try:
        firebase_config = json.loads(firebase_env)
    except Exception as e:
        raise Exception(f"Invalid FIREBASE_CONFIG JSON: {str(e)}")

    cred = credentials.Certificate(firebase_config)

    firebase_app = firebase_admin.initialize_app(cred, {
        "databaseURL": db_url
    })

    return firebase_app

# INIT FIREBASE ON START
init_firebase()

# ---------------- QUESTIONS ----------------
QUESTIONS = [
    "Little interest or pleasure in doing things?",
    "Feeling down, depressed, or hopeless?",
    "Trouble sleeping or sleeping too much?",
    "Feeling tired or having little energy?",
    "Poor appetite or overeating?",
    "Feeling bad about yourself?",
    "Trouble concentrating?",
    "Moving or speaking slowly?",
    "Thoughts of self-harm?",
    "Feeling anxious or worried?",
    "Feeling lonely?",
    "Difficulty making decisions?",
    "Loss of interest in friends?",
    "Feeling irritated?",
    "Academic stress?",
    "Feeling hopeless?"
]

# ---------------- HELPERS ----------------
def clean_email_key(email):
    return email.replace(".", "_dot_").replace("@", "_at_")

def current_user():
    return session.get("user")

def get_level(score):
    if score <= 16:
        return "Mild"
    elif score <= 32:
        return "Moderate"
    return "High"

# ---------------- HOME ----------------
@app.route("/")
def home():
    if current_user():
        return redirect(url_for("assessment"))
    return redirect(url_for("login"))

# ---------------- REGISTER ----------------
@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        name = request.form.get("name")
        email = request.form.get("email","").lower()
        password = request.form.get("password")

        user_key = clean_email_key(email)
        ref = db.reference(f"users/{user_key}")

        if ref.get():
            return render_template("register.html", error="User already exists")

        ref.set({
            "name": name,
            "email": email,
            "password_hash": generate_password_hash(password),
            "streak": 0,
            "xp": 0,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })

        session["user"] = {
            "key": user_key,
            "name": name,
            "email": email
        }

        return redirect(url_for("assessment"))

    return render_template("register.html")

# ---------------- LOGIN ----------------
@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form.get("email","").lower()
        password = request.form.get("password")

        user_key = clean_email_key(email)

        user_data = db.reference(f"users/{user_key}").get()

        if not user_data or not check_password_hash(user_data.get("password_hash",""), password):
            return render_template("login.html", error="Invalid credentials")

        session["user"] = {
            "key": user_key,
            "name": user_data.get("name")
        }

        return redirect(url_for("assessment"))

    return render_template("login.html")

# ---------------- ASSESSMENT ----------------
@app.route("/assessment")
def assessment():

    if not current_user():
        return redirect(url_for("login"))

    return render_template("assessment.html", questions=QUESTIONS)

# ---------------- SUBMIT ----------------
@app.route("/submit", methods=["POST"])
def submit():

    user = current_user()
    answers = []

    for i in range(len(QUESTIONS)):
        val = request.form.get(f"q{i+1}")
        answers.append(int(val))

    score = sum(answers)
    level = get_level(score)

    db.reference(f"users/{user['key']}/assessments").push({
        "score": score,
        "level": level,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })

    return jsonify({"score": score, "level": level})

# ---------------- CHATBOT ----------------
@app.route("/chat", methods=["POST"])
def chat():

    message = request.json.get("message","")

    try:
        response = client.chat.completions.create(
            model="openai/gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are MindCare AI assistant."},
                {"role": "user", "content": message}
            ]
        )

        return jsonify({
            "reply": response.choices[0].message.content
        })

    except Exception as e:
        print("AI error:", e)
        return jsonify({
            "reply": "I am here for you. Please take a deep breath."
        })

# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))