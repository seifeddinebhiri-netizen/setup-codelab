import os
from dotenv import load_dotenv
from google import genai

# 1. Load the key
load_dotenv()
api_key = os.getenv("MY_AI_API_KEY")

print(f"🔑 Checking Key: {api_key[:5]}... (hidden)")

if not api_key:
    print("❌ ERROR: No API Key found in .env file")
    exit()

try:
    # 2. Connect to Google
    client = genai.Client(api_key=api_key)
    
    # 3. Ask Google "What models can I use?"
    print("\n📡 Connecting to Google servers...")
    all_models = list(client.models.list())
    
    print("\n✅ SUCCESS! Your API Key is working.\n")
    print("📋 Here are the models you can use in your code:")
    print("-" * 40)
    
    # 4. Filter for models that can generate text
    count = 0
    for m in all_models:
        # We only care about models that can generate content (chat)
        if "generateContent" in m.supported_actions:
            # Clean up the name (removes 'models/' prefix if present)
            clean_name = m.name.replace("models/", "")
            print(f" • {clean_name}")
            count += 1
            
    print("-" * 40)
    print(f"Total available models: {count}")

except Exception as e:
    print("\n❌ FAILURE: Your API Key or Connection is broken.")
    print(f"Error details: {e}")