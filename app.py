import os, json, re
from flask import Flask, request, jsonify, render_template
import google.generativeai as genai
from dotenv import load_dotenv

# Load .env from the mindguard-ai subfolder
load_dotenv(os.path.join(os.path.dirname(__file__), "mindguard-ai", ".env"))

app = Flask(__name__)  # templates/ and static/ are right next to this file

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

SYSTEM_PROMPT = """
You are MindGuard AI, an empathetic mental health & drug prevention chatbot for students.
Rules:
1. Be empathetic, warm, supportive, non-judgmental.
2. Keep response to 2-3 sentences max.
3. Detect mood from: Stress, Anxiety, Sadness, Anger, Neutral, Hopeful, Overwhelmed, Lonely
4. Risk levels: Low, Medium, High (High ONLY if drugs/self-harm/abuse/suicide explicitly mentioned)
5. Return ONLY valid JSON: {"mood": "string", "risk_level": "string", "response": "string", "emergency_flag": boolean}
No extra text, no markdown, just raw JSON.
"""

def safe_json(text):
    text = re.sub(r'```json|```', '', text).strip()
    match = re.search(r'\{.*\}', text, re.DOTALL)
    if match:
        return json.loads(match.group())
    raise ValueError("Invalid JSON")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_msg = data.get("message", "").strip()
    if not user_msg:
        return jsonify({"error": "Empty message"}), 400

    try:
        res = model.generate_content(f"{SYSTEM_PROMPT}\nUser: {user_msg}")
        bot_data = safe_json(res.text)
        return jsonify(bot_data)
    except Exception as e:
        return jsonify({
            "mood": "Neutral",
            "risk_level": "high",
            "response": "I hear you, and I'm here for you. Can you tell me more about what you're going through?",
            "emergency_flag": True
        }), 200

if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)