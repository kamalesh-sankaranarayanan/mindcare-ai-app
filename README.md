# MindCare

## New Features
- Login and register page
- Question-by-question assessment page
- Firebase Realtime Database storage
- Result-based activity recommendations
- Dashboard with Chart.js
- Mood journal
- Interactive chatbot
- Optional Gemini API chatbot with free-tier support
- Personal wellness dashboard with assessment trends and mood check-ins
- Mind Lab with Focus Flow, Reaction Reset, Grounding Quest, and Memory Garden
- Private guided journal and saved game sessions with XP rewards
- Responsive dark/light interface

## Setup
1. Put `serviceAccountKey.json` near `app.py` for local development.
2. Add `FIREBASE_DATABASE_URL` to `.env`.
3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Run:

```bash
python app.py
```

5. Open:

```text
http://127.0.0.1:5000
```

## AI Chatbot Setup
1. Create an OpenRouter API key.
2. Create API key.
3. Create `.env` file based on `.env.example`.
4. Add:

```text
OPENROUTER_API_KEY=your_key_here
```

If no API key is added, the app still works using the rule-based chatbot.

## Render

Use `web: gunicorn app:app` as the start command. Set these environment variables:

- `FIREBASE_CONFIG`: the complete Firebase service-account JSON
- `FIREBASE_DATABASE_URL`: your Realtime Database URL
- `SECRET_KEY`: a long random value
- `OPENROUTER_API_KEY`: optional
- `FLASK_ENV=production`

Set the Render health-check path to `/health`. Never upload `.env` or
`serviceAccountKey.json`; both are already excluded by `.gitignore`.
