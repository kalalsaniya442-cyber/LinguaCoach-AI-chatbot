import os
import sys
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

def check_api_key():
    if not API_KEY or API_KEY == "your_gemini_api_key_here":
        print("\n[ERROR] GEMINI_API_KEY is not set or is still the default placeholder.")
        print("Please create a .env file with your API key:\n")
        print("    GEMINI_API_KEY=AIzaSy...")
        print("\nYou can get a free API key at: https://aistudio.google.com/\n")
        sys.exit(1)

def init_chat_session():
    """Initializes the chat session using google-genai or google-generativeai."""
    # Attempt 1: New official google-genai SDK
    try:
        from google import genai
        client = genai.Client(api_key=API_KEY)
        
        # Try gemini-2.5-flash or gemini-2.0-flash
        chat = client.chats.create(model="gemini-2.5-flash")
        
        def send_message(text: str) -> str:
            response = chat.send_message(text)
            return response.text

        return send_message, "google-genai (gemini-2.5-flash)"
    except ImportError:
        pass
    except Exception:
        # If gemini-2.5-flash isn't available in standard tier, try gemini-2.0-flash
        try:
            from google import genai
            client = genai.Client(api_key=API_KEY)
            chat = client.chats.create(model="gemini-2.0-flash")
            def send_message(text: str) -> str:
                return chat.send_message(text).text
            return send_message, "google-genai (gemini-2.0-flash)"
        except Exception:
            pass

    # Attempt 2: google-generativeai SDK
    try:
        import google.generativeai as genai_legacy
        genai_legacy.configure(api_key=API_KEY)
        model = genai_legacy.GenerativeModel("gemini-1.5-flash")
        chat = model.start_chat(history=[])

        def send_message(text: str) -> str:
            response = chat.send_message(text)
            return response.text

        return send_message, "google-generativeai (gemini-1.5-flash)"
    except ImportError:
        pass

    print("\n[ERROR] Neither 'google-genai' nor 'google-generativeai' is installed.")
    print("Please install dependencies by running:\n")
    print("    pip install -r requirements.txt\n")
    sys.exit(1)

def main():
    print("========================================")
    print("        Gemini CLI Chatbot              ")
    print("========================================")
    
    check_api_key()
    
    print("Connecting to Gemini API...")
    try:
        send_msg, model_info = init_chat_session()
        print(f"Connected using {model_info}!")
    except Exception as e:
        print(f"[ERROR] Failed to initialize Gemini: {e}")
        sys.exit(1)

    print("\nChat session started! Type 'exit', 'quit', or press Ctrl+C to stop.\n")

    while True:
        try:
            user_input = input("You: ").strip()
            
            if not user_input:
                continue
                
            if user_input.lower() in ("exit", "quit", "q"):
                print("\nGoodbye!")
                break

            print("\nGemini is thinking...", end="\r")
            reply = send_msg(user_input)
            # Clear the 'thinking' line and print response
            print(" " * 30, end="\r")
            print(f"Gemini: {reply}\n")

        except KeyboardInterrupt:
            print("\n\nSession ended by user. Goodbye!")
            break
        except Exception as e:
            print(f"\n[ERROR] An error occurred: {e}\n")

if __name__ == "__main__":
    main()
