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

        # 🔥 Fallback models (important for stability)
        models = [
            "qwen/qwen2.5-7b-instruct:free",
            "meta-llama/llama-3.1-8b-instruct:free"
        ]

        for model in models:
            response = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                    "Content-Type": "application/json",
                    "HTTP-Referer": "https://udaan-chatbot.onrender.com",
                    "X-Title": "Udaan Future School Chatbot"
                },
                json={
                    "model": model,
                    "messages": [
                        {"role": "system", "content": SYSTEM_PROMPT},
                        {"role": "user", "content": user_message}
                    ],
                    "temperature": 0.6,
                    "max_tokens": 700
                }
            )

            data = response.json()

            # 🔥 Debug safety (prevents crashes)
            if "choices" in data:
                return jsonify({
                    "reply": data["choices"][0]["message"]["content"]
                })

            print("Model failed:", model)
            print("Response:", data)

        return jsonify({
            "reply": "All AI models are busy right now. Please try again in a few seconds."
        })

    except Exception as e:
        print("ERROR:", e)
        return jsonify({
            "reply": "Sorry, the chatbot is currently unavailable."
        })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
