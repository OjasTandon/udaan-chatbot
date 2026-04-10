from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

SYSTEM_PROMPT = """
You are the official enquiry assistant for "Udaan Future School".

Rules:
- Be polite, formal, and helpful
- Answer admissions, fees, timings, facilities
- Keep answers short and structured
- If unknown, say you will forward to school office
- Never say you are an AI

School Context:
Udaan Future School is an educational institution focused on student growth and learning.
"""

@app.route("/")
def home():
    return "Udaan Chatbot Backend Running 🚀"

@app.route("/chat", methods=["POST"])
def chat():
    try:
        user_message = request.json.get("message")

        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "meta-llama/llama-3.3-70b-instruct:free",
                "messages": [
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": user_message}
                ],
                "temperature": 0.6,
                "max_tokens": 700
            }
        )

        data = response.json()

        reply = data["choices"][0]["message"]["content"]

        return jsonify({"reply": reply})

    except Exception as e:
        print(e)
        return jsonify({
            "reply": "Sorry, the chatbot is currently unavailable."
        })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
