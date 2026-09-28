import os
from dotenv import load_dotenv
from flask import Flask, jsonify, render_template, request
from google import genai
from chatbot_config import SYSTEM_PROMPT

load_dotenv()

app = Flask(__name__)
MODEL_NAME = "gemini-3.1-flash-lite"

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise RuntimeError("GEMINI_API_KEY is not configured.")

client = genai.Client(api_key=api_key)

@app.get("/")
def index():
    return render_template("index.html")

@app.post("/api/chat")
def chat():
    data = request.get_json(silent=True) or {}
    message = str(data.get("message", "")).strip()
    if not message:
        return jsonify({"error": "Please enter a domain-related question."}), 400
    try:
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=message,
            config={
                "system_instruction": SYSTEM_PROMPT,
                "temperature": 0.3,
                "thinking_config": {"thinking_level": "minimal"},
            },
        )
        answer = (response.text or "").strip()
        return jsonify({"answer": answer or "I couldn't generate an answer right now. Please try again."})
    except Exception:
        return jsonify({"error": "I couldn't connect to the AI right now. Please try again."}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)), debug=False)
