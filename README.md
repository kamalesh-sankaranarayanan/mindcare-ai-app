# MindCare AI Firebase V2

## New Features
- Login and register page
- Question-by-question assessment page
- Firebase Realtime Database storage
- Result-based activity recommendations
- Dashboard with Chart.js
- Mood journal
- Interactive chatbot
- Optional Gemini API chatbot with free-tier support

## Setup
1. Put `serviceAccountKey.json` near `app.py`.
2. In `app.py`, check your Firebase databaseURL.
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

## Gemini Chatbot Setup
1. Go to Google AI Studio.
2. Create API key.
3. Create `.env` file based on `.env.example`.
4. Add:

```text
GEMINI_API_KEY=your_key_here
```

If no Gemini key is added, the app still works using the free rule-based chatbot.
