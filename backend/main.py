from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import yfinance as yf
import os
from dotenv import load_dotenv
# --- VITAL CHANGE BELOW ---
# We are now using the NEW library you installed
from google import genai 

# 1. Load Environment Variables
load_dotenv()
api_key = os.getenv("MY_AI_API_KEY")

# 2. Configure the New AI Client
if not api_key:
    print("⚠️ WARNING: No API key found! Check your .env file.")
    client = None
else:
    # The new library uses a 'Client' instead of 'configure'
    client = genai.Client(api_key=api_key)

app = FastAPI()

# 3. CORS Setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_ai_analysis(ticker, price):
    """
    Uses the new Google GenAI SDK to analyze the stock.
    """
    if not client:
        return "Error: AI API Key is missing."

    try:
        prompt = f"""
        You are a sarcastic financial advisor. The stock {ticker} is currently ${price}.
        Give me a 1-sentence reaction to this price.
        """
        
        # --- NEW CODE SYNTAX ---
        # The old way was 'model.generate_content'
        # The new way is 'client.models.generate_content'
        response = client.models.generate_content(
            model="gemini-2.5-flash", 
            contents=prompt
        )
        
        if response and response.text:
            return response.text
        return "AI was speechless."
        
    except Exception as e:
        return f"AI Error: {str(e)}"

@app.get("/")
def read_root():
    return {"status": "Server is running"}

@app.get("/stock/{ticker}")
def get_stock_price(ticker: str):
    try:
        # Fetch data from Yahoo Finance
        stock = yf.Ticker(ticker)
        data = stock.history(period="1d")
        
        if data.empty:
            raise HTTPException(status_code=404, detail="Stock not found")
            
        current_price = data['Close'].iloc[-1]
        
        # Call the AI
        ai_message = get_ai_analysis(ticker, round(current_price, 2))
        
        return {
            "symbol": ticker.upper(),
            "price": round(current_price, 2),
            "currency": "USD",
            "ai_message": ai_message 
        }
    except Exception as e:
        print(f"Server Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))