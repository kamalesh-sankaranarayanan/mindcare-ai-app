from flask import Flask, render_template, request, redirect, url_for, jsonify, session
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
import firebase_admin
from firebase_admin import credentials, db
import google.generativeai as genai
import os

# ---------------- LOAD ENV ----------------
load_dotenv()

# ---------------- GEMINI SETUP ----------------
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)

# ---------------- FLASK APP ----------------
app = Flask(__name__)
app.secret_key = os.environ.get(
    "SECRET_KEY",
    "change-this-secret-key"
)
# ---------------- FIREBASE ----------------
import json

if not firebase_admin._apps:

    with open("serviceAccountKey.json", "r") as f:
        firebase_config = json.load(f)

    cred = credentials.Certificate(firebase_config)

    firebase_admin.initialize_app(cred, {
        "databaseURL": firebase_config.get("databaseURL")
    })

# ---------------- QUESTIONS ----------------
QUESTIONS = [
    "Little interest or pleasure in doing things?",
    "Feeling down, depressed, or hopeless?",
    "Trouble sleeping or sleeping too much?",
    "Feeling tired or having little energy?",
    "Poor appetite or overeating?",
    "Feeling bad about yourself?",
    "Trouble concentrating on studies or work?",
    "Moving or speaking slowly, or being restless?",
    "Thoughts of self-harm or feeling life is not worth living?",
    "Feeling anxious, nervous, or worried?",
    "Feeling lonely or isolated?",
    "Difficulty making decisions?",
    "Loss of interest in friends or activities?",
    "Feeling irritated or angry easily?",
    "Feeling academic or exam pressure?",
    "Feeling hopeless about the future?"
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

# ---------------- ACTIVITIES ----------------
def get_activities(level, category):

    # ---------- TEEN ----------
    if category == "teen":

        if level == "Mild":

            return [

                {
                    "icon": "🎮",
                    "title": "Mini Memory Game",
                    "desc": "Interactive focus game",
                    "url": "/memory-game"
                },

                {
                    "icon": "🎵",
                    "title": "Music Therapy",
                    "desc": "Relax with calming music",
                    "url": "/music"
                },

                {
                    "icon": "🌬️",
                    "title": "Breathing Exercise",
                    "desc": "Calm your mind slowly",
                    "url": "/breathing"
                },

                {
                    "icon": "🧘",
                    "title": "Meditation",
                    "desc": "Guided meditation session",
                    "url": "/meditation"
                },

                {
                    "icon": "😂",
                    "title": "Funny Video Break",
                    "desc": "Lighten your mood",
                    "url": "/funny-video"
                }
            ]

        elif level == "Moderate":

            return [

                {
                    "icon": "🎯",
                    "title": "Focus Challenge",
                    "desc": "Improve focus and calmness",
                    "url": "/stress-game"
                },

                {
                    "icon": "📝",
                    "title": "Journal Writing",
                    "desc": "Express your thoughts",
                    "url": "/journal"
                },

                {
                    "icon": "🎮",
                    "title": "Reaction Game",
                    "desc": "Fast reflex challenge",
                    "url": "/memory-game"
                },

                {
                    "icon": "🌬️",
                    "title": "Breathing Game",
                    "desc": "Guided breathing exercise",
                    "url": "/breathing"
                },

                {
                    "icon": "🎵",
                    "title": "Relax Playlist",
                    "desc": "Calming lofi music",
                    "url": "/music"
                }
            ]

        else:

            return [

                {
                    "icon": "🤝",
                    "title": "Talk to Trusted Person",
                    "desc": "Reach out for support",
                    "url": "/support"
                },

                {
                    "icon": "🌬️",
                    "title": "Calm Breathing",
                    "desc": "Reduce anxiety slowly",
                    "url": "/breathing"
                },

                {
                    "icon": "🧘",
                    "title": "Meditation",
                    "desc": "Guided meditation session",
                    "url": "/meditation"
                },

                {
                    "icon": "📞",
                    "title": "Support Contact",
                    "desc": "Talk to someone you trust",
                    "url": "/support"
                },

                {
                    "icon": "😂",
                    "title": "Relaxing Videos",
                    "desc": "Watch calming videos",
                    "url": "/funny-video"
                }
            ]


    # ---------- COLLEGE ----------
    elif category == "college":

        if level == "Mild":

            return [

                {
                    "icon": "📚",
                    "title": "Study Focus Timer",
                    "desc": "Pomodoro productivity timer",
                    "url": "/stress-game"
                },

                {
                    "icon": "🎵",
                    "title": "Lo-fi Music",
                    "desc": "Deep focus study music",
                    "url": "/music"
                },

                {
                    "icon": "🌬️",
                    "title": "Breathing Exercise",
                    "desc": "Refresh your mind",
                    "url": "/breathing"
                },

                {
                    "icon": "🧘",
                    "title": "Meditation",
                    "desc": "Short mindful relaxation",
                    "url": "/meditation"
                },

                {
                    "icon": "🎮",
                    "title": "Brain Game",
                    "desc": "Interactive memory challenge",
                    "url": "/memory-game"
                }
            ]

        elif level == "Moderate":

            return [

                {
                    "icon": "🧘",
                    "title": "Meditation",
                    "desc": "Guided meditation",
                    "url": "/meditation"
                },

                {
                    "icon": "🌬️",
                    "title": "Stress Relief",
                    "desc": "Breathing animation",
                    "url": "/breathing"
                },

                {
                    "icon": "📝",
                    "title": "Journal",
                    "desc": "Write your thoughts",
                    "url": "/journal"
                },

                {
                    "icon": "🎯",
                    "title": "Placement Stress Guide",
                    "desc": "Placement preparation support",
                    "url": "/stress-game"
                },

                {
                    "icon": "🎮",
                    "title": "Puzzle Game",
                    "desc": "Interactive memory game",
                    "url": "/memory-game"
                }
            ]

        else:

            return [

                {
                    "icon": "🤝",
                    "title": "Talk to Mentor",
                    "desc": "Seek support and guidance",
                    "url": "/support"
                },

                {
                    "icon": "📞",
                    "title": "Support Contact",
                    "desc": "Reach out immediately",
                    "url": "/support"
                },

                {
                    "icon": "🌬️",
                    "title": "Emergency Breathing",
                    "desc": "Calming breathing exercise",
                    "url": "/breathing"
                },

                {
                    "icon": "🧠",
                    "title": "Mental Relaxation",
                    "desc": "Reduce mental overload",
                    "url": "/meditation"
                },

                {
                    "icon": "🧘",
                    "title": "Guided Meditation",
                    "desc": "Slow guided relaxation",
                    "url": "/meditation"
                }
            ]


    # ---------- ADULT ----------
    elif category == "adult":

        if level == "Mild":

            return [

                {
                    "icon": "📖",
                    "title": "Mindful Reading",
                    "desc": "Relax your thoughts",
                    "url": "/journal"
                },

                {
                    "icon": "🚶",
                    "title": "Walking Relaxation",
                    "desc": "Short mindful walk",
                    "url": "/breathing"
                },

                {
                    "icon": "🎵",
                    "title": "Calm Music",
                    "desc": "Slow instrumental music",
                    "url": "/music"
                },

                {
                    "icon": "🧘",
                    "title": "Meditation",
                    "desc": "Mindful relaxation",
                    "url": "/meditation"
                },

                {
                    "icon": "🎮",
                    "title": "Logic Puzzle",
                    "desc": "Focus improvement puzzle",
                    "url": "/memory-game"
                }
            ]

        elif level == "Moderate":

            return [

                {
                    "icon": "🧘",
                    "title": "Meditation",
                    "desc": "Guided meditation",
                    "url": "/meditation"
                },

                {
                    "icon": "📝",
                    "title": "Stress Journal",
                    "desc": "Express your feelings",
                    "url": "/journal"
                },

                {
                    "icon": "🌬️",
                    "title": "Breathing",
                    "desc": "Reduce stress gradually",
                    "url": "/breathing"
                },

                {
                    "icon": "🎵",
                    "title": "Relax Music",
                    "desc": "Reduce screen stress",
                    "url": "/music"
                },

                {
                    "icon": "🎯",
                    "title": "Burnout Recovery",
                    "desc": "Mental energy restoration",
                    "url": "/stress-game"
                }
            ]

        else:

            return [

                {
                    "icon": "📞",
                    "title": "Professional Support",
                    "desc": "Talk to a professional",
                    "url": "/support"
                },

                {
                    "icon": "🤝",
                    "title": "Family Support",
                    "desc": "Reach out to loved ones",
                    "url": "/support"
                },

                {
                    "icon": "🧘",
                    "title": "Calm Meditation",
                    "desc": "Slow relaxation session",
                    "url": "/meditation"
                },

                {
                    "icon": "🌬️",
                    "title": "Grounding Exercise",
                    "desc": "Reduce panic and stress",
                    "url": "/breathing"
                },

                {
                    "icon": "🚨",
                    "title": "Emergency Wellness Help",
                    "desc": "Immediate support guidance",
                    "url": "/support"
                }
            ]

    return []
# ---------------- FALLBACK CHATBOT ----------------
def fallback_bot(message):

    msg = message.lower()

    if any(w in msg for w in [
        "sad", "depressed", "lonely",
        "hopeless", "cry", "worthless"
    ]):
        return (
            "I'm sorry you're feeling low. "
            "Resting for a while, listening to calm music, "
            "or talking to someone you trust may help."
        )

    elif any(w in msg for w in [
        "stress", "exam", "pressure",
        "anxiety", "panic", "overthinking",
        "frustrated", "frustration",
        "angry", "irritated"
    ]):
        return (
            "It sounds emotionally overwhelming right now. "
            "Take a short pause, breathe slowly, and focus only on the next small task."
        )

    elif any(w in msg for w in [
        "motivation", "motivated",
        "unmotivated", "lazy", "tired"
    ]):
        return (
            "Yes, taking short rest is okay. "
            "Rest helps when your mind feels overloaded."
        )

    elif any(w in msg for w in [
        "boring", "ugly", "failure",
        "bad", "not good enough"
    ]):
        return (
            "No, you are not boring. "
            "Everyone feels low or insecure sometimes."
        )

    elif any(w in msg for w in [
        "sleep", "insomnia", "can't sleep"
    ]):
        return (
            "Try reducing screen usage before bed, "
            "keep lights dim, and take slow deep breaths."
        )

    else:
        return (
            "I understand. "
            "Would you like relaxation activities, motivation, "
            "stress help, or someone to talk with?"
        )


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

        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        age = request.form.get("age")
        category = request.form.get("category")
        health_background = request.form.get(
            "health_background"
        )

        if not name or not email or not password:
            return render_template(
                "register.html",
                error="All fields are required."
            )

        user_key = clean_email_key(email)

        user_ref = db.reference(
            f"users/{user_key}"
        )

        if user_ref.get():
            return render_template(
                "register.html",
                error="User already exists."
            )

        user_ref.set({
            "name": name,
            "email": email,
            "password_hash": generate_password_hash(password),

            "user_profile": {
                "age": age,
                "category": category
            },

            "streak": 0,
            "xp": 0,
            "health_background": health_background,

            "created_at": datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )
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

        email = request.form.get(
            "email", ""
        ).strip().lower()

        password = request.form.get("password", "")

        user_key = clean_email_key(email)

        user_data = db.reference(
            f"users/{user_key}"
        ).get()

        if not user_data or not check_password_hash(
            user_data.get("password_hash", ""),
            password
        ):
            return render_template(
                "login.html",
                error="Invalid email or password."
            )

        session["user"] = {
            "key": user_key,
            "name": user_data.get("name", "User"),
            "email": email
        }

        return redirect(url_for("assessment"))

    return render_template("login.html")


# ---------------- LOGOUT ----------------
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


# ---------------- ASSESSMENT ----------------
@app.route("/assessment")
def assessment():

    if not current_user():
        return redirect(url_for("login"))

    return render_template(
        "assessment.html",
        questions=QUESTIONS,
        name=current_user()["name"]
    )


# ---------------- SUBMIT ----------------
@app.route("/submit", methods=["POST"])
def submit():

    if not current_user():
        return redirect(url_for("login"))

    answers = []

    for i in range(1, len(QUESTIONS) + 1):

        value = request.form.get(f"q{i}")

        if value is None:
            return f"Missing answer for question {i}", 400

        value = int(value)

        answers.append(value)

    user = current_user()

    score = sum(answers)

    level = get_level(score)

    user_data = db.reference(
        f"users/{user['key']}"
    ).get()

    category = user_data.get(
        "user_profile", {}
    ).get("category", "college")

    activities = get_activities(level, category)

    assessment_data = {
        "score": score,
        "level": level,
        "answers": answers,
        "created_at": datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )
    }

    db.reference(
        f"users/{user['key']}/assessments"
    ).push(assessment_data)

    # XP + STREAK
    user_ref = db.reference(
        f"users/{user['key']}"
    )

    current_data = user_ref.get()

    current_streak = current_data.get("streak", 0)
    current_xp = current_data.get("xp", 0)

    user_ref.update({
        "streak": current_streak + 1,
        "xp": current_xp + 10
    })

    return render_template(
        "result.html",
        name=user["name"],
        score=score,
        level=level,
        activities=activities
    )


# ---------------- DASHBOARD ----------------
@app.route("/dashboard")
def dashboard():

    if not current_user():
        return redirect(url_for("login"))

    user = current_user()

    data = db.reference(
        f"users/{user['key']}/assessments"
    ).get()

    user_data = db.reference(
        f"users/{user['key']}"
    ).get()

    streak = user_data.get("streak", 0)
    xp = user_data.get("xp", 0)

    history = []

    if data:

        for _, item in data.items():
            history.append({
                "date": item.get("created_at", ""),
                "score": item.get("score", 0),
                "level": item.get("level", "Unknown")
            })

    history = sorted(
        history,
        key=lambda x: x["date"]
    )

    return render_template(
        "dashboard.html",
        name=user["name"],
        history=history,
        streak=streak,
        xp=xp
    )


# ---------------- RELAX ----------------
@app.route("/relax/<level>")
def relax(level):

    if not current_user():
        return redirect(url_for("login"))

    user = current_user()

    user_data = db.reference(
        f"users/{user['key']}"
    ).get()

    category = user_data.get(
        "user_profile", {}
    ).get("category", "college")

    activities = get_activities(level, category)

    return render_template(
        "relax.html",
        level=level,
        activities=activities
    )


# ---------------- SAVE MOOD ----------------
@app.route("/save_mood", methods=["POST"])
def save_mood():

    if not current_user():
        return jsonify({
            "message": "Please login first."
        }), 401

    data = request.get_json()

    mood_data = {
        "mood": data.get("mood"),
        "note": data.get("note", ""),
        "created_at": datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )
    }

    db.reference(
        f"users/{current_user()['key']}/moods"
    ).push(mood_data)

    return jsonify({
        "message": "Mood saved successfully."
    })

@app.route("/meditation")
def meditation():
    return render_template("meditation.html")


@app.route("/breathing")
def breathing():
    return render_template("breathing.html")


@app.route("/journal")
def journal():
    return render_template("journal.html")


@app.route("/memory-game")
def memory_game():
    return render_template("memory_game.html")

@app.route("/music")
def music():
    return render_template("music.html")


@app.route("/stress-game")
def stress_game():
    return render_template("stress_game.html")


@app.route("/funny-video")
def funny_video():
    return render_template("funny_video.html")

# ---------------- CHATBOT ----------------
@app.route("/chat", methods=["POST"])
def chat():

    user_message = request.json.get(
        "message",
        ""
    ).strip()

    if not user_message:
        return jsonify({
            "reply": "Please type a message."
        })

    emergency_words = [
        "suicide",
        "kill myself",
        "self harm",
        "die",
        "end my life",
        "harm myself"
    ]

    if any(word in user_message.lower() for word in emergency_words):
        return jsonify({
            "reply": (
                "I'm really sorry you're feeling this way. "
                "Please contact a trusted person immediately."
            )
        })

# ---------- AI CHATBOT ----------
    try:

        response = client.chat.completions.create(

            model="openai/gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are MindCare AI, a supportive wellness assistant. "
                        "Be calm, practical, supportive, and conversational."
                    )
                },
                {
                    "role": "user",
                    "content": user_message
                }
            ]
        )

        ai_reply = response.choices[0].message.content

        return jsonify({
            "reply": ai_reply
        })

    except Exception as e:

        print("AI Error:", str(e))

        reply = fallback_bot(user_message)

        return jsonify({
            "reply": reply
        })


# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run(debug=True)
