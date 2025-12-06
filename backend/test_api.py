import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load .env from parent directory
dotenv_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(dotenv_path)

api_key = os.getenv("GEMINI_API_KEY")
print(f"API Key found: {bool(api_key)}")

if api_key:
    genai.configure(api_key=api_key)
    try:
        print("Testing models/gemma-3-1b-it with user key...")
        model = genai.GenerativeModel('models/gemma-3-1b-it')
        response = model.generate_content("Hello")
        print("SUCCESS: Model works!")
        print("Response:", response.text)
    except Exception as e:
        print("FAILED:", e)
else:
    print("No API Key found in .env")
