import httpx
import re
import google.generativeai as genai
import os
from fastapi import APIRouter
from dotenv import load_dotenv
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from Routers.StockIdeas import ChatBot
from Models.StocksModels import Symbols
from fastapi_sqlalchemy import db
from sqlalchemy import or_, and_
import nltk
from nltk.corpus import stopwords

# nltk.download('stopwords')

load_dotenv()

ChatRouter = APIRouter()

genai.configure(api_key=os.getenv("gemini_key"))



def generate_stock_analysis(symbol, query):
    print(os.getenv("gemini_key"))

    """Generate an AI-powered stock analysis based on the user's query without providing investment advice."""

    model = genai.GenerativeModel(
        model_name='gemini-1.5-pro',
        system_instruction=(
            "You are a professional financial analyst providing factual stock market insights. "
            "Your analysis should focus on historical trends, key metrics, and market conditions. "
            "Do not provide personalized financial advice or recommend investments. "
            "Always maintain a neutral and data-driven approach."
        ),
        generation_config={
            "temperature": 0.3,
            "top_p": 0.95,
            "max_output_tokens": 800
        }
    )


    print(symbol)
    
    if symbol:
        stock_data = ChatBot(symbol)  # Fetch stock data
        
        if not stock_data:
            return f"I'm sorry, but I couldn't retrieve the {symbol} stock data at the moment. Please try again later."

        stock_data = stock_data[0]

        # Constructing a refined prompt
        prompt = f"""
        Here is an objective analysis of {stock_data['Name']} ({stock_data['Symbol']}).
        
        ** Stock Overview:**
        - **Current Price:** {stock_data['Price']}
        - **Price Change (%):** {stock_data['ChangePercentage']}
        - **Day Range:** {stock_data['DayLow']} - {stock_data['DayHigh']}
        - **52-Week Range:** {stock_data['YearLow']} - {stock_data['YearHigh']}
        - **Market Capitalization:** {stock_data['MarketCap']}
        - **Sector:** {stock_data['Sector']}
        - **Exchange:** {stock_data['Exchange']}
        - **Volume:** {stock_data['Volume']}
        
        ** Technical Indicators:**
        - **P/E Ratio:** {stock_data['PE']}
        - **50-Day SMA:** {stock_data['SMA50']}
        - **200-Day SMA:** {stock_data['SMA200']}
        - **RSI (Relative Strength Index):** {stock_data['RSI']}
        - **Beta (Volatility Indicator):** {stock_data['Beta']}
        
        ** Financial Performance:**
        - **EPS (Earnings Per Share):** {stock_data['EPS']}
        - **Revenue Growth:** {stock_data['revenueGrowth']}
        - **Net Income Growth:** {stock_data['NetIncomeGrowth']}
        - **Dividend Yield (TTM):** {stock_data['DividendYieldTTM']}
        - **Debt-Equity Ratio:** {stock_data['DebtEquityRatioTTM']}
        
        ** Recent Performance:**
        - **1-Day Change:** {stock_data['1D']}
        - **5-Day Change:** {stock_data['5D']}
        - **1-Month Performance:** {stock_data['1M']}
        - **3-Month Performance:** {stock_data['3M']}
        - **6-Month Performance:** {stock_data['6M']}
        - **Year-to-Date (YTD):** {stock_data['YTD']}
        - **1-Year Performance:** {stock_data['1Y']}
        
        ** Analysis Based on Your Query:**
        "{query}"
        
        ** Key Insights (Strictly Informational):**
        - If you're inquiring about stock trends, here are relevant price movements and indicators.
        - If you're analyzing financial health, here are key metrics such as revenue growth and profitability.
        - If you're interested in market behavior, here’s how the stock has performed in different timeframes.
        - If you're looking at risk factors, here’s an overview of volatility, debt ratios, and historical performance.

        ** Important Note:**
        This analysis is strictly informational and does not constitute financial advice. Always conduct your own research or consult a financial professional before making investment decisions.
        """

    else:
        prompt = f"""
        Hello! I'm here to provide general insights into the stock market.

        **Your Query:** "{query}"

        Please specify a stock symbol or a market-related question, such as:
        -  Historical stock trends
        -  Company financial performance
        -  Market analysis techniques
        -  Macroeconomic trends

        I will generate an objective and fact-based response. Let me know how I can assist you!
        """

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f" Analysis Error: {str(e)}"


# List of popular stock symbols to match user input
tickers  = [
    "ABT", "CVX", "DIS", "MRK", "XOM", "PG", "T", "AXP", "ILMN", "NKE", 
    "NOW", "CL", "AMD", "CSCO", "IBM", "KO", "PFE", "SPGI", "VZ", "JPM", 
    "AMT", "V", "GE", "CAT", "LMT", "BA", "MRNA", "MMM", "MCD", "AAPL", 
    "GOOGL", "INTC", "SPOT", "JNJ", "BIIB", "ADBE", "ABBV", "GS", "HD", 
    "META", "TGT", "UNH", "PEP", "ASML", "BMY", "SBUX", "QCOM", "AMZN", 
    "TSLA", "NVDA", "MSFT", "WBA", "PYPL", "NFLX", "TTD", "WDAY", "SQ", 
    "NPOF.ME", "KZMS.ME", "PMGOLD.AX", "TERRAREAL.BO", "ADANIENT.NS", 
    "BSE.NS", "HDFCBANK.NS", "DIVISLAB.NS", "CUB.NS", "CBPE.JK", "BBNI.JK", 
    "BBCA.JK", "BRIS.JK", "P34.SI", "GPSO.JK", "U11.SI", "K71U.SI", "N2IU.SI"
]


import re
import json

def extract_financial_entities(query: str) -> dict:
    """
    Extracts stock tickers and company names from user input
    Returns: { "symbol": str|None, "company": str|None }
    """
    # Configure Gemini for entity extraction
    extraction_model = genai.GenerativeModel('gemini-pro')


    
    prompt = f"""
    Analyze this financial query and extract ONLY:
    - Stock ticker symbols (1-5 uppercase letters)
    - Full company names
    
    Return JSON format with these strict rules:
    1. Only include stock symbols in "symbol" field
    2. Only include full company names in "company" field
    3. Use null for missing values
    4. No explanations, only JSON
    
    Examples:
    Input: "What's AAPL's current price?"
    Output: {{"symbol": "AAPL", "company": null}}
    
    Input: "Show me Microsoft's earnings"
    Output: {{"symbol": null, "company": "Microsoft"}}
    
    Input: "IBM and Apple stock analysis"
    Output: {{"symbol": "IBM", "company": "Apple"}}
    
    Now process: "{query}"
    """
    
    try:
        response = extraction_model.generate_content(prompt)
        # Clean Gemini response
        cleaned = response.text.strip().strip('```json').strip()
        return json.loads(cleaned)
    except:
        # Fallback to regex if AI extraction fails
        return regex_fallback(query)

def regex_fallback(query: str) -> dict:
    """Fallback method using regex patterns"""
    # Stock symbol pattern (1-5 uppercase letters)
    symbols = re.findall(r'\b[A-Z]{1,5}\b', query.upper())
    
    # Company name pattern (Title Case words)
    companies = re.findall(r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b', query)
    
    return {
        "symbol": symbols[0] if symbols else None,
        "company": companies[0] if companies else None
    }

class Message(BaseModel):
    message: str

@ChatRouter.post('/chatbot')
def Bot(ChatModel: Message):

    user_input = ChatModel.message.lower().strip()

    greetings = ["hi", "hello", "hey", "good morning", "good evening"]
    farewells = ["bye", "goodbye", "see you", "take care"]
    general_queries = [
        "what can you do", 
        "what information do you provide", 
        "how can you help", 
        "who are you"
    ]
    user_input = re.sub(r"[^a-zA-Z0-9\s]", "", user_input).lower().strip()

    if user_input in greetings:
        return JSONResponse("Hello! I am a stock market chatbot. How can I assist you with stock-related queries today?")
    elif user_input in farewells:
        return JSONResponse("Goodbye! Have a great day and happy investing!")
    elif user_input in general_queries:
        return JSONResponse(
            "I am a stock market chatbot. I can provide real-time stock prices, historical trends, market insights, "
            "company financials, and general stock market updates. Feel free to ask about any stock symbol or company!"
        )
    else:
        entities = extract_financial_entities(user_input.upper())
        print(entities)
        if entities:
            if entities['symbol']:
                result = generate_stock_analysis(entities['symbol'], user_input)
                return JSONResponse(result)
            elif entities['company']:
                result = generate_stock_analysis(entities['company'], user_input)
                return JSONResponse(result)
            else:
                return JSONResponse("I couldn't find a stock symbol or company name in your request. Please provide a valid stock ticker symbol or company name for analysis.")
        else:
            return JSONResponse("I couldn't find a stock symbol or company name in your request. Please provide a valid stock ticker symbol or company name for analysis.")