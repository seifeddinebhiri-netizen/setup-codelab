import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("MY_AI_API_KEY")
genai.configure(api_key=api_key)

print(f"Checking key: {api_key[:5]}...")

try:
    print("Available models for you:")
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(f" - {m.name}")
except Exception as e:
    print(f"Error connecting: {e}")