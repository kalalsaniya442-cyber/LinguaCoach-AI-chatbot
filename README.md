# 🌍 LinguaCoach - AI Language Learning Companion

LinguaCoach is a responsive, interactive Streamlit application designed for immersive language practice across multiple languages, skill levels, and conversation topics.

---

## ✨ Features

- **🗣️ Chat Practice**: AI-powered conversational partner that replies in your chosen target language, offers gentle corrections in your native language, and keeps dialogue flowing with contextual follow-up questions.
- **📚 Interactive Vocabulary**: Flashcard quizzes with multiple-choice options, instant right/wrong evaluation, and contextual example sentences.
- **✍️ Grammar Exercises**: Fill-in-the-blank and multiple-choice challenges paired with deep grammatical explanations and rule summaries.
- **📊 Real-time Progress Tracking**: Live session metrics, visual progress bars, accuracy calculations, and learning milestones.
- **🛡️ Resilient API Fallback**: Works seamlessly offline or with an OpenAI API key. If the key is missing or invalid, it gracefully activates curated offline practice responses while keeping all quizzes 100% interactive.

---

## 🚀 Quickstart Guide

### 1. Prerequisites
- Python 3.10+ (tested with Python 3.14)
- Git (optional)

### 2. Virtual Environment Setup

**Windows (PowerShell):**
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**macOS / Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configuration (Optional)
Copy the example environment file:
```bash
cp .env.example .env
```
Open `.env` and provide your OpenAI API Key:
```env
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-4o-mini
```
*(Note: You can also enter or paste your API key directly in the app's sidebar during runtime!)*

### 5. Launch Application
```bash
streamlit run app.py
```
Open your browser at `http://localhost:8501`.

---

## 🗂️ Project Structure

```
├── app.py              # Main Streamlit application
├── requirements.txt    # Dependencies (streamlit, openai, python-dotenv)
├── .env.example        # Sample environment configuration
├── .env                # Local secrets (excluded from git)
└── README.md           # Documentation and startup instructions
```
