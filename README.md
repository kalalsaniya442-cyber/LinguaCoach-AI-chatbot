# Minimal Gemini Chatbot

A simple, lightweight chatbot built in Python using the official Google Gemini API. It supports continuous multi-turn conversations through either a command-line interface (CLI) or a clean, modern web interface.

---

## 1. Setup

### Step 1: Install Dependencies
Open a terminal in this directory and run:
```bash
pip install -r requirements.txt
```

### Step 2: Configure API Key
1. Get a Gemini API key from [Google AI Studio](https://aistudio.google.com/).
2. Copy `.env.example` to a new file named `.env`:
   ```bash
   copy .env.example .env
   ```
3. Open `.env` and paste your API key:
   ```env
   GEMINI_API_KEY=AIzaSyYourActualKeyHere
   ```

---

## 2. Usage

### Option A: Command-Line Chatbot (CLI)
Run the interactive terminal chat:
```bash
python cli_chat.py
```
- Type your prompt and press **Enter**.
- Supports multi-turn memory within the conversation session.
- Type `exit` or `quit` (or press `Ctrl+C`) to exit.

### Option B: Web Chatbot
Start the local web server:
```bash
python app.py
```
Then open your browser and navigate to:
```
http://127.0.0.1:5000
```
- Features a clean, responsive dark-mode chat interface.
- Supports multi-turn conversation context.
- Click **New Chat** to reset the conversation at any time.

---

## Project Structure

```
├── .env.example      # Example environment variables template
├── requirements.txt  # Project dependencies
├── cli_chat.py       # Command-line chatbot script
├── app.py            # Flask backend for the web chatbot
├── static/
│   └── index.html    # Clean, responsive Web UI
└── README.md         # Setup and run instructions
```
