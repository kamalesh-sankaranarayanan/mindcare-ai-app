from flask import Flask, render_template, request, redirect, url_for, jsonify, session
from datetime import datetime, timezone
from functools import wraps
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
app.config.update(
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Lax",
    SESSION_COOKIE_SECURE=os.getenv("FLASK_ENV") == "production",
)

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

    if not db_url:
        raise RuntimeError("FIREBASE_DATABASE_URL is required.")

    if firebase_env:
        try:
            firebase_config = json.loads(firebase_env)
        except json.JSONDecodeError as error:
            raise RuntimeError(f"Invalid FIREBASE_CONFIG JSON: {error}") from error
        cred = credentials.Certificate(firebase_config)
    else:
        local_key = os.path.join(os.path.dirname(__file__), "serviceAccountKey.json")
        if not os.path.exists(local_key):
            raise RuntimeError(
                "Set FIREBASE_CONFIG on Render or add serviceAccountKey.json locally."
            )
        cred = credentials.Certificate(local_key)

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

def login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if not current_user():
            return redirect(url_for("login"))
        return view(*args, **kwargs)
    return wrapped

def timestamp():
    return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")


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

@app.route("/health")
def health():
    return jsonify({"status": "healthy", "service": "mindcare"}), 200


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
@login_required
def dashboard():

    user = current_user()

    data = db.reference(
        f"users/{user['key']}/assessments"
    ).get()

    user_data = db.reference(
        f"users/{user['key']}"
    ).get()

    streak = user_data.get("streak", 0)
    xp = user_data.get("xp", 0)
    moods_data = user_data.get("moods", {}) or {}
    games_data = user_data.get("game_sessions", {}) or {}

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
    moods = sorted([
        {
            "mood": item.get("mood", "Unknown"),
            "note": item.get("note", ""),
            "date": item.get("created_at", "")
        }
        for item in moods_data.values()
    ], key=lambda x: x["date"])
    game_sessions = sorted([
        {
            "game": item.get("game", "Game"),
            "score": item.get("score", 0),
            "date": item.get("created_at", "")
        }
        for item in games_data.values()
    ], key=lambda x: x["date"], reverse=True)[:5]

    latest_score = history[-1]["score"] if history else None
    previous_score = history[-2]["score"] if len(history) > 1 else None
    score_change = latest_score - previous_score if previous_score is not None else None
    level = history[-1]["level"] if history else "Not assessed"

    return render_template(
        "dashboard.html",
        name=user["name"],
        history=history,
        streak=streak,
        xp=xp,
        moods=moods[-10:],
        recent_moods=list(reversed(moods[-4:])),
        game_sessions=game_sessions,
        latest_score=latest_score,
        score_change=score_change,
        current_level=level,
        progress=min(xp % 100, 100)
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
@login_required
def save_mood():

    if not current_user():
        return jsonify({
            "message": "Please login first."
        }), 401

    data = request.get_json(silent=True) or {}
    allowed_moods = {"Great", "Good", "Okay", "Low", "Stressed"}
    mood = data.get("mood")
    if mood not in allowed_moods:
        return jsonify({"message": "Please choose a valid mood."}), 400

    mood_data = {
        "mood": mood,
        "note": str(data.get("note", ""))[:500],
        "created_at": timestamp()
    }

    db.reference(
        f"users/{current_user()['key']}/moods"
    ).push(mood_data)

    return jsonify({
        "message": "Mood saved successfully."
    })

@app.route("/hub")
@login_required
def hub():
    return render_template("hub.html")

@app.route("/focus-flow")
@login_required
def focus_flow():
    return render_template("focus_flow.html")

@app.route("/reaction-game")
@login_required
def reaction_game():
    return render_template("reaction_game.html")

@app.route("/grounding-game")
@login_required
def grounding_game():
    return render_template("grounding_game.html")

@app.route("/api/game-session", methods=["POST"])
@login_required
def save_game_session():
    data = request.get_json(silent=True) or {}
    allowed_games = {"Memory Match", "Focus Flow", "Reaction Reset", "Grounding Quest"}
    game = data.get("game")
    try:
        score = max(0, min(int(data.get("score", 0)), 100000))
    except (TypeError, ValueError):
        return jsonify({"message": "Invalid score."}), 400
    if game not in allowed_games:
        return jsonify({"message": "Unknown game."}), 400

    db.reference(f"users/{current_user()['key']}/game_sessions").push({
        "game": game,
        "score": score,
        "created_at": timestamp()
    })
    user_ref = db.reference(f"users/{current_user()['key']}")
    user_data = user_ref.get() or {}
    reward = min(25, 5 + score // 100)
    user_ref.update({"xp": int(user_data.get("xp", 0)) + reward})
    return jsonify({"message": "Session saved", "xp_earned": reward})

@app.route("/api/journal", methods=["GET", "POST"])
@login_required
def journal_api():
    ref = db.reference(f"users/{current_user()['key']}/journals")
    if request.method == "GET":
        entries = ref.get() or {}
        result = sorted(entries.values(), key=lambda x: x.get("created_at", ""), reverse=True)
        return jsonify(result[:10])
    data = request.get_json(silent=True) or {}
    content = str(data.get("content", "")).strip()
    if not content:
        return jsonify({"message": "Write something before saving."}), 400
    ref.push({
        "content": content[:3000],
        "prompt": str(data.get("prompt", ""))[:300],
        "created_at": timestamp()
    })
    return jsonify({"message": "Reflection saved privately."})

@app.route("/meditation")
@login_required
def meditation():
    return render_template("meditation.html")


@app.route("/breathing")
@login_required
def breathing():
    return render_template("breathing.html")


@app.route("/journal")
@login_required
def journal():
    return render_template("journal.html")


@app.route("/memory-game")
@login_required
def memory_game():
    return render_template("memory_game.html")

@app.route("/music")
@login_required
def music():
    return render_template("music.html")


@app.route("/stress-game")
@login_required
def stress_game():
    return render_template("stress_game.html")


@app.route("/funny-video")
@login_required
def funny_video():
    return render_template("funny_video.html")

# ---------------- CHATBOT ----------------
@app.route("/chat", methods=["POST"])
@login_required
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
    app.run(debug=os.getenv("FLASK_DEBUG", "false").lower() == "true")
