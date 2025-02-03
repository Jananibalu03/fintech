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

load_dotenv()

ChatRouter = APIRouter()

genai.configure(api_key=os.getenv("gemini_key"))



def generate_stock_analysis(symbol, query):
    """Generate AI-powered stock analysis based on the query."""

    

    # if not stock_data:
    #     return "Sorry, I couldn't fetch the stock data for your query."

    model = genai.GenerativeModel(
                                model_name='gemini-1.5-pro',
                                system_instruction=(
                                    "You are a financial analyst assistant. Analyze stock data using the provided information. "
                                    "Focus on factual insights, historical context, and market trends. "
                                    "Do not provide personalized financial advice. "
                                    "Highlight both positive and negative indicators."
                                ),
                                generation_config={
                                    "temperature": 0.3,
                                    "top_p": 0.95,
                                    "max_output_tokens": 1024
                                }
                                )

    if symbol:
        stock_data = ChatBot(symbol)[0]
        # Dynamic prompt adjustment based on user query
        prompt = f"""
        Based on the following stock data, provide an analysis for the question: "{query}"
        
        **Stock Data:**
        "Name": {stock_data['Name']},
        "Symbol": {stock_data['Symbol']},
        "Price": {stock_data['Price']}",
        "ChangePercentage": {stock_data['ChangePercentage']},
        "DayLow": {stock_data['DayLow']},
        "DayHigh": {stock_data['DayHigh']},
        "YearLow": {stock_data['YearLow']},
        "YearHigh": {stock_data['YearHigh']},
        "MarketCap": {stock_data['MarketCap']},
        "P/E": {stock_data['PE']},
        "SMA50": {stock_data['SMA50']},
        "SMA200": {stock_data['SMA200']},
        "RSI": {stock_data['RSI']},
        "Sector": {stock_data['Sector']},
        "EPS": {stock_data['EPS']},
        "Growth": {stock_data['revenueGrowth']},
        "Exchange": {stock_data['Exchange']},
        "Volume": {stock_data['Volume']},
        "AvgVolume": {stock_data['AvgVolume']},
        "OpenPrice": {stock_data['OpenPrice']},
        "PreviousClose": {stock_data['PreviousClose']},
        "OneDayVolatility": {stock_data['OneDayVolatility']},
        "Beta": {stock_data['Beta']},
        "1D": {stock_data['1D']},
        "5D": {stock_data['5D']},
        "1M": {stock_data['1M']},
        "3M": {stock_data['3M']},
        "6M": {stock_data['6M']},
        "YTD": {stock_data['YTD']},
        "1Y": {stock_data['1Y']},
        "DividendYieldTTM": {stock_data['DividendYieldTTM']},
        "PayoutRatioTTM": {stock_data['PayoutRatioTTM']},
        "CurrentRatioTTM": {stock_data['CurrentRatioTTM']},
        "QuickRatioTTM": {stock_data['QuickRatioTTM']},
        "DebtRatioTTM": {stock_data['DebtRatioTTM']},
        "DebtEquityRatioTTM": {stock_data['DebtEquityRatioTTM']},
        "FreeCashFlowPerShareTTM": {stock_data['FreeCashFlowPerShareTTM']},
        "PriceToBookRatioTTM": {stock_data['PriceToBookRatioTTM']},
        "ProfitMarginsTTM": {stock_data['ProfitMarginsTTM']},
        "EarningGrowthTTM": {stock_data['EarningGrowthTTM']},
        "NetIncomeGrowth": {stock_data['NetIncomeGrowth']},
        "revenueGrowth": {stock_data['revenueGrowth']},

        **Analysis Guidelines:**
        1. If the user asks about price trends, explain current price trends, day range, and yearly performance.
        2. If the user asks about growth or profitability, discuss the P/E ratio, revenue growth, and EPS.
        3. If the user asks about technical analysis, focus on RSI, SMA50, and key price movements.
        4. Always provide a neutral, factual tone and make comparisons to industry benchmarks if relevant.
        Provide a concise analysis of the stock based on the provided data.
        """
    else:
        prompt = f"""
            Focus specifically on the user's question: "{query}"
        """

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Analysis Error: {str(e)}"

# List of popular stock symbols to match user input
tickers = [
            'AAPL', 'MSFT', 'AMZN', 'GOOGL', 'NVDA', 'META', 'TSLA', 'ADBE', 'PYPL', 'NFLX', 
            'INTC', 'MRNA', 'QCOM', 'PEP', 'SBUX', 'CSCO', 'SPOT', 'AMD', 'NOW', 'SQ', 
            'TTD', 'ILMN', 'ASML', 'BMY', 'BIIB', 'WDAY', 'JNJ', 'JPM', 'XOM', 'KO', 
            'DIS', 'PG', 'CVX', 'V', 'PFE', 'HD', 'MCD', 'MRK', 'BA', 'CAT', 'VZ', 
            'IBM', 'XOM', 'LMT', 'NKE', 'CL', 'T', 'PEP', 'ABBV', 'WBA', 'GE', 
            'TGT', 'AXP', 'GS', 'CVX', 'MMM', 'UNH', 'AMT', 'SPGI', 'ABT'
        ]

class Message(BaseModel):
    message: str

@ChatRouter.post('/chatbot')
async def Bot(ChatModel: Message):

    user_input = ChatModel.message.strip().upper()

    cleaned_string = re.sub(r'[^A-Za-z0-9\s]', '', user_input)
    user_data = cleaned_string.split(" ")
 
    matching_elements = [item for item in user_data if item in tickers]

    if matching_elements:
        symbol = matching_elements[0]
        result = generate_stock_analysis(symbol, user_input)
        return JSONResponse(result)
    else:
        result = generate_stock_analysis(None, user_input)
        return JSONResponse(result)
    
    