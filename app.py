from flask import Flask, render_template, request, jsonify
import requests
from dotenv import load_dotenv
import os

app = Flask(__name__)

# Load the API key from .env file
load_dotenv()
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

# Print loaded key to confirm (for debugging)
print("🔐 Loaded API Key:", OPENROUTER_API_KEY)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_msg = request.json["message"]

    try:
        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "HTTP-Referer": "http://localhost:5000",
            "Content-Type": "application/json"
        }

        data = {
            "model": "gpt-3.5-turbo",
            "messages": [
                {"role": "user", "content": user_msg}
            ]
        }

        response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)

        # Debug: Print the API response
        print("🛰️ API RESPONSE:", response.text)

        response_json = response.json()

        if "choices" not in response_json:
            return jsonify({"response": f"Bot Error: 'choices' not found. Full response: {response_json}"})

        bot_reply = response_json["choices"][0]["message"]["content"]
        return jsonify({"response": bot_reply})

    except Exception as e:
        return jsonify({"response": f"Bot Error: {str(e)}"})

if __name__ == "__main__":
    app.run(debug=True)






