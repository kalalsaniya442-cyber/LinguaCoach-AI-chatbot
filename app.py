import os
import sys
import uuid
from flask import Flask, request, jsonify, send_from_directory
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

app = Flask(__name__, static_folder="static")

# In-memory store for active chat sessions
# session_id -> chat session object
sessions = {}

def create_chat_session():
    """Initializes a new Gemini chat session."""
    if not API_KEY or API_KEY == "your_gemini_api_key_here":
        raise ValueError("GEMINI_API_KEY is not configured in .env file.")

    # Try google-genai
    try:
        from google import genai
        client = genai.Client(api_key=API_KEY)
        try:
            chat = client.chats.create(model="gemini-2.5-flash")
        except Exception:
            chat = client.chats.create(model="gemini-2.0-flash")

        def send_fn(message: str) -> str:
            res = chat.send_message(message)
            return res.text

        return send_fn
    except ImportError:
        pass

    # Try google-generativeai
    try:
        import google.generativeai as genai_legacy
        genai_legacy.configure(api_key=API_KEY)
        model = genai_legacy.GenerativeModel("gemini-1.5-flash")
        chat = model.start_chat(history=[])

        def send_fn(message: str) -> str:
            res = chat.send_message(message)
            return res.text

        return send_fn
    except ImportError:
        pass

    raise RuntimeError("Neither 'google-genai' nor 'google-generativeai' is installed.")

@app.route("/")
def index():
    return send_from_directory(app.static_folder, "index.html")

@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json(silent=True) or {}
    user_message = data.get("message", "").strip()
    session_id = data.get("sessionId")

    if not user_message:
        return jsonify({"error": "Message cannot be empty."}), 400

    # Ensure a valid session exists
    if not session_id or session_id not in sessions:
        session_id = str(uuid.uuid4())
        try:
            sessions[session_id] = create_chat_session()
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    send_fn = sessions[session_id]

    try:
        reply = send_fn(user_message)
        return jsonify({
            "reply": reply,
            "sessionId": session_id
        })
    except Exception as e:
        return jsonify({"error": f"Gemini API Error: {str(e)}"}), 500

@app.route("/api/reset", methods=["POST"])
def reset():
    data = request.get_json(silent=True) or {}
    session_id = data.get("sessionId")
    if session_id and session_id in sessions:
        del sessions[session_id]
    return jsonify({"status": "reset"})

if __name__ == "__main__":
    if not API_KEY or API_KEY == "your_gemini_api_key_here":
        print("[WARNING] GEMINI_API_KEY is not set or using placeholder...")

    port = 8080
    print(f"Starting Gemini Web Chatbot on http://127.0.0.1:{port}")
    app.run(debug=True, port=port)