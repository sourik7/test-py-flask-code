from flask import Flask, jsonify, render_template, request
from dotenv import find_dotenv, load_dotenv
import os
import google.generativeai as genai

# Load environment variables from .env
load_dotenv(find_dotenv())

app = Flask(__name__)

# Securely get the Gemini API key from environment
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Load Gemini model
model = genai.GenerativeModel("gemini-2.5-flash")

@app.route("/")
def home():
    return render_template("home.html")  # Template file at /templates/home.html

@app.route("/ask", methods=["POST"])
def ask():
    data = request.json
    user_message = data.get("message")
    if not user_message:
        return jsonify({"error": "No message provided"}), 400
    try:
        response = model.generate_content(user_message)
        return jsonify({"response": response.text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
