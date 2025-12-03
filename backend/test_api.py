import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
print(f"API Key found: {bool(api_key)}")

genai.configure(api_key=api_key)

try:
    print("Testing models to find a working one...")
    working_model = None
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(f"Testing {m.name}...")
            try:
                model = genai.GenerativeModel(m.name)
                response = model.generate_content("Hello")
                print(f"SUCCESS: {m.name} works!")
                working_model = m.name
                break
            except Exception as e:
                print(f"Failed {m.name}: {e}")
    
    if working_model:
        print(f"FOUND WORKING MODEL: {working_model}")
        with open('working_model.txt', 'w', encoding='utf-8') as f:
            f.write(working_model)
    else:
        print("NO WORKING MODEL FOUND.")
except Exception as e:
    print("Error listing models:", e)
