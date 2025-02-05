from fastapi import APIRouter,HTTPException,Query, Depends
from fastapi.responses import JSONResponse
from Models.StocksModels import Symbols, StockInfo, CompanyProfile, StockPerformance, FinancialMetrics, TechnicalIndicator, FinancialGrowth, StandardDeviation
from dotenv import load_dotenv
import os
import httpx
from fastapi_sqlalchemy import db
from typing import List, Optional
from datetime import datetime, time
import math
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger
import pytz
from sqlalchemy import and_
from collections import defaultdict

from apscheduler.executors.pool import ThreadPoolExecutor

load_dotenv()
router = APIRouter()

Symbol_Base_URL = "https://financialmodelingprep.com/api/v3/stock/list"

Stock_Base_URL = "https://financialmodelingprep.com/api/v3/quote" 

Company_Base_URL = "https://financialmodelingprep.com/api/v3/profile"

Stock_Performance_URL = "https://financialmodelingprep.com/api/v3/stock-price-change"

Stock_Ratio_URL = "https://financialmodelingprep.com/api/v3/ratios-ttm"

RSI_Technical_URL = "https://financialmodelingprep.com/api/v3/technical_indicator/1day"

Intradata_URL = "https://financialmodelingprep.com/api/v3/historical-price-full"

FINANCIAL_GROWTH_URL = "https://financialmodelingprep.com/api/v3/financial-growth"

StandardDeviation_URL = "https://financialmodelingprep.com/api/v3/technical_indicator/1day"

@router.get("/UploadSymbols")
async def Upload_Symbols():
    params = {
        "apikey": os.getenv("API_KEY")
    }
    try:
        tickers = [
            'AAPL', 'MSFT', 'AMZN', 'GOOGL', 'NVDA', 'META', 'TSLA', 'ADBE', 'PYPL', 'NFLX', 
            'INTC', 'MRNA', 'QCOM', 'PEP', 'SBUX', 'CSCO', 'SPOT', 'AMD', 'NOW', 'SQ', 
            'TTD', 'ILMN', 'ASML', 'BMY', 'BIIB', 'WDAY', 'JNJ', 'JPM', 'XOM', 'KO', 
            'DIS', 'PG', 'CVX', 'V', 'PFE', 'HD', 'MCD', 'MRK', 'BA', 'CAT', 'VZ', 
            'IBM', 'XOM', 'LMT', 'NKE', 'CL', 'T', 'PEP', 'ABBV', 'WBA', 'GE', 
            'TGT', 'AXP', 'GS', 'CVX', 'MMM', 'UNH', 'AMT', 'SPGI', 'ABT', 'IBM'
        ]
        
        with httpx.Client() as r:
            response = r.get(Symbol_Base_URL, params=params)
            data = response.json()


            for comp in data:

                if comp['symbol'] in tickers:
                    default_company = Symbols(
                        Csymbol=comp["symbol"],
                        Cname=comp["name"],
                        exchange=comp["exchangeShortName"]
                    )
                    db.session.add(default_company)
                    db.session.commit()
                    db.session.refresh(default_company)

        exchanges = defaultdict(int)
        exchange_name = []
        count = 0
        with httpx.Client() as r:
            response = r.get(Symbol_Base_URL, params=params)
            data = response.json()

            for comp in data:

                if count > 50:
                    break

                exchange_name = comp["exchangeShortName"]

                # Skip if already reached the 20-symbol limit
                if exchanges[exchange_name] >= 5:
                    continue

                # Create StockCompany object and store it for bulk insert
                stock_companies = Symbols(
                    Csymbol=comp["symbol"],
                    Cname=comp["name"],
                    exchange=exchange_name
                )
                db.session.add(stock_companies)
                db.session.commit()
                db.session.refresh(stock_companies)
                exchanges[exchange_name] += 1
                count+=1

      
        return JSONResponse(status_code=200,content={"message": "Data Successfully Inserted."})
    except Exception as e:
        return HTTPException(status_code=403,detail=f"An Error Occured! {e.args}")

@router.get("/Symbols")
async def GetSymbols( 
    symbol: Optional[str] = Query(None),
    exchange: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    limit: int = Query(10, le=100)
    ):
    try:
        skip = (page - 1) * limit
        query = db.session.query(Symbols)

        # Apply filters if query parameters are provided
        if symbol:
            query = query.filter(Symbols.Csymbol.ilike(f"%{symbol}%"))
        if exchange:
            query = query.filter(Symbols.exchange.ilike(f"%{exchange}%"))

        # Get the total count of users that match the filters
        total_count = query.count()

        # Apply pagination
        result = query.offset(skip).limit(limit).all()

        companies = [{"Symbol": result.Csymbol,"Name": result.Cname, "Exchange": result.exchange} for result in result]
    
        # Return paginated users and total count
        return JSONResponse(status_code = 200, content={"total": total_count, "Compines": companies})
    except Exception as e:
        return HTTPException(status_code=403,detail=f"An Error Occured! {e.args}")


# def fetch_volatility_in_batch(symbols):
#     params = {
#         "type": "standardDeviation",
#         "period": 10,
#         "apikey": os.getenv("API_KEY")
#     }

#     if not symbols:
#         return None

#     with httpx.Client() as r:
#         try:
#             res = r.get(f"{StandardDeviation_URL}/{symbols}", params=params, timeout=30)
#             response = res.json()
#             if response:  # Ensure response is not empty
#                 item = response[0] 
#                 return item.get("standardDeviation", 0) * 100

#         except (IndexError, KeyError, TypeError) as e:
#             print(f"Error fetching volatility for {e}")


@router.get("/UploadStocks")
def Upload_Stocks():
    print("task1")
    params = {"apikey": os.getenv("API_KEY")}
    print(os.getenv("API_KEY"))

    try:
        with db():
            with httpx.Client() as r:
                # Fetch all existing stock symbols in a single query
                existing_symbols = {s.symbol: s for s in db.session.query(StockInfo).all()}

                # Fetch all stock data from API in a single request
                symbol_query = db.session.query(Symbols).all()
                # stock_data_list = []

                for symbol in symbol_query:
                    response = r.get(f"{Stock_Base_URL}/{symbol.Csymbol}", params=params, timeout=30)
                    res = response.json()

                    for data in res:
                        stock_info = existing_symbols.get(data.get("symbol"))

                        if not stock_info:  
                            # New entry
                            stock_data_list = StockInfo(
                                symbol=data.get("symbol"),
                                name=data.get("name"),
                                price=data.get("price"),
                                changesPercentage=data.get("changesPercentage"),
                                change=data.get("change"),
                                dayLow=data.get("dayLow"),
                                dayHigh=data.get("dayHigh"),
                                yearHigh=data.get("yearHigh"),
                                yearLow=data.get("yearLow"),
                                marketCap=data.get("marketCap"),
                                priceAvg50=data.get("priceAvg50"),
                                priceAvg200=data.get("priceAvg200"),
                                exchange=data.get("exchange"),
                                volume=data.get("volume"),
                                avgVolume=data.get("avgVolume"),
                                open_price=data.get("open"),
                                previousClose=data.get("previousClose"),
                                eps=data.get("eps"),
                                pe=data.get("pe"),
                                timestamp=datetime.fromtimestamp(data.get("timestamp")).strftime("%Y-%m-%d")
                            )

                            db.session.add(stock_data_list)
                            db.session.commit()
                            db.session.refresh(stock_data_list)
                        else:
                            # Update existing record
                            stock_info.name = data.get("name", stock_info.name)
                            stock_info.price = data.get("price", stock_info.price)
                            stock_info.changesPercentage = data.get("changesPercentage", stock_info.changesPercentage)
                            stock_info.change = data.get("change", stock_info.change)
                            stock_info.dayLow = data.get("dayLow", stock_info.dayLow)
                            stock_info.dayHigh = data.get("dayHigh", stock_info.dayHigh)
                            stock_info.yearHigh = data.get("yearHigh", stock_info.yearHigh)
                            stock_info.yearLow = data.get("yearLow", stock_info.yearLow)
                            stock_info.marketCap = data.get("marketCap", stock_info.marketCap)
                            stock_info.priceAvg50 = data.get("priceAvg50", stock_info.priceAvg50)
                            stock_info.priceAvg200 = data.get("priceAvg200", stock_info.priceAvg200)
                            stock_info.exchange = data.get("exchange", stock_info.exchange)
                            stock_info.volume = data.get("volume", stock_info.volume)
                            stock_info.avgVolume = data.get("avgVolume", stock_info.avgVolume)
                            stock_info.open_price = data.get("open", stock_info.open_price)
                            stock_info.previousClose = data.get("previousClose", stock_info.previousClose)
                            stock_info.eps = data.get("eps", stock_info.eps)
                            stock_info.pe = data.get("pe", stock_info.pe)
                            stock_info.timestamp = datetime.fromtimestamp(data.get("timestamp")).strftime("%Y-%m-%d")

                            db.session.commit()
                            db.session.refresh(stock_info)

                return JSONResponse(status_code=200, content={"message": "Data Successfully Inserted."})

    except Exception as e:
        return HTTPException(status_code=403, detail=f"An Error Occurred! {e.args}")

@router.get("/Stocks")
async def StocksDetails( 
    symbol: Optional[str] = Query(None),
    exchange: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    limit: int = Query(10, le=100)
    ):
    try:
        skip = (page - 1) * limit
        query = db.session.query(StockInfo)

        # Apply filters if query parameters are provided
        if symbol:
            query = query.filter(StockInfo.symbol.ilike(f"%{symbol}%"))
        if exchange:
            query = query.filter(StockInfo.exchange.ilike(f"%{exchange}%"))
    

        # Get the total count of users that match the filters
        total_count = query.count()

        # Apply pagination
        result = query.offset(skip).limit(limit).all()

        companies = [{  "symbol" : result.symbol,
                        "name" : result.name,
                        "price" : result.price,
                        "changesPercentage" : result.changesPercentage,
                        "change" : result.change,
                        "dayLow" : result.dayLow,
                        "dayHigh" : result.dayHigh,
                        "52weekshigh" : result.yearHigh,
                        "52weeklow" : result.yearLow,
                        "marketCap" : result.marketCap,
                        "SMA50" : result.priceAvg50,
                        "SMA200" : result.priceAvg200,
                        "exchange" : result.exchange,
                        "volume" : result.volume,
                        "avgVolume" : result.avgVolume,
                        "open_price" :result.open_price ,
                        "previousClose" : result.previousClose,
                        "Employeepershare" : result.eps,
                        "PERatio" : result.pe,
                        "timestamp" :  result.timestamp.strftime("%Y-%m-%d")
                    } for result in result]
    
        # Return paginated users and total count
        return JSONResponse(status_code = 200, content={"total": total_count, "Compines": companies})
    except Exception as e:
        return HTTPException(status_code=403,detail=f"An Error Occured! {e.args}")
    

@router.get("/UploadCompanyProfiles")
def Upload_CompanyProfile():
    print("task2")
    params = {
        "apikey": os.getenv("API_KEY")
    }
    try:
        with db():
            with httpx.Client() as r:
                symbol_query = db.session.query(Symbols).all()

                for symbol in symbol_query:
                    response = r.get(f"{Company_Base_URL}/{symbol.Csymbol}", params = params,  timeout=30)
                    res = response.json()
                    for data in res:
                        symbol_id = db.session.query(CompanyProfile).filter(CompanyProfile.symbol==symbol.Csymbol).first()
                        if not symbol_id:
                            company_profile_list = CompanyProfile(   symbol=data.get("symbol"),
                                                                beta=data.get("beta"),
                                                                lastDiv=data.get("lastDiv"),
                                                                companyName=data.get("companyName"),
                                                                industry=data.get("industry"),
                                                                website=data.get("website"),
                                                                description=data.get("description"),
                                                                sector=data.get("sector"),
                                                                country=data.get("country"),
                                                                phone=data.get("phone"),
                                                                address=data.get("address"),
                                                                city=data.get("city"),
                                                                state=data.get("state"),
                                                                zip_code=data.get("zip"),
                                                                ipoDate=data.get("ipoDate")
                                                            )
                            db.session.add(company_profile_list)
                            db.session.commit()
                            db.session.refresh(company_profile_list)
                        else:
                            symbol_id.beta = data.get("beta", symbol_id.beta)
                            symbol_id.lastDiv = data.get("lastDiv", symbol_id.lastDiv)
                            symbol_id.companyName = data.get("companyName", symbol_id.companyName)
                            symbol_id.industry = data.get("industry", symbol_id.industry)
                            symbol_id.website = data.get("website", symbol_id.website)
                            symbol_id.description = data.get("description", symbol_id.description)
                            symbol_id.sector = data.get("sector", symbol_id.sector)
                            symbol_id.country = data.get("country", symbol_id.country)
                            symbol_id.phone = data.get("phone", symbol_id.phone)
                            symbol_id.address = data.get("address", symbol_id.address)
                            symbol_id.city = data.get("city", symbol_id.city)
                            symbol_id.state = data.get("state", symbol_id.state)
                            symbol_id.zip_code = data.get("zip", symbol_id.zip_code)
                            symbol_id.ipoDate = data.get("ipoDate", symbol_id.ipoDate)

                            db.session.commit()  
                            db.session.refresh(symbol_id)

                return JSONResponse(status_code=200,content={"message": "Data Successfully Inserted."})
    except Exception as e:
        raise HTTPException(status_code=403,detail=f"An Error Occured! {e.args}")
    

@router.get("/CompanyProfiles")
async def CompanyProfile_Details( 
    symbol: Optional[str] = Query(None),
    exchange: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    limit: int = Query(10, le=100)
    ):
    try:
        skip = (page - 1) * limit
        query = db.session.query(CompanyProfile)

        # Apply filters if query parameters are provided
        if symbol:
            query = query.filter(CompanyProfile.symbol.ilike(f"%{symbol}%"))
        if exchange:
            query = query.filter(CompanyProfile.exchange.ilike(f"%{exchange}%"))

        # Get the total count of users that match the filters
        total_count = query.count()

        # Apply pagination
        result = query.offset(skip).limit(limit).all()

        companies = [{  
                        "symbol" : result.symbol,
                        "beta" : result.beta,
                        "lastDiv": result.lastDiv,
                        "companyName": result.companyName,
                        "industry": result.industry,
                        "website": result.website,
                        "description": result.description,
                        "sector": result.sector,
                        "country": result.country,
                        "phone": result.phone,
                        "address": result.address,
                        "city": result.city,
                        "state": result.state,
                        "zip_code": result.zip_code,
                        "ipoDate":result.ipoDate.strftime("%Y-%m-%d")
                        
                    } for result in result]
    
        # Return paginated users and total count
        return JSONResponse(status_code = 200, content={"total": total_count, "Compines": companies})
    except Exception as e:
        return HTTPException(status_code=403,detail=f"An Error Occured! {e.args}")
    
@router.get("/UploadStocksPerformance")
def Upload_StocksPerformance():
    print("task3")
    params = {
        "apikey": os.getenv("API_KEY")
    }
    try:
        with db():
            with httpx.Client() as r:
                symbol_query = db.session.query(Symbols).all()

                for symbol in symbol_query:
                    response = r.get(f"{Stock_Performance_URL}/{symbol.Csymbol}", params = params,  timeout=30)
                    res = response.json()

                    for data in res:
                        symbol_id = db.session.query(StockPerformance).filter(StockPerformance.symbol==symbol.Csymbol).first()
                        if not symbol_id:
                            Stock_performance_list=StockPerformance(
                                                                    symbol=data.get("symbol"),
                                                                    one_day=data.get("1D"),
                                                                    five_day=data.get("5D"),
                                                                    one_month=data.get("1M"),
                                                                    three_month=data.get("3M"),
                                                                    six_month=data.get("6M"),
                                                                    ytd=data.get("ytd"),
                                                                    one_year=data.get("1Y"),
                                                                    three_year=data.get("3Y"),
                                                                    five_year=data.get("5Y"),
                                                                    ten_year=data.get("10Y"),
                                                                    max_val=data.get("max"),
                                                                )
                            db.session.add(Stock_performance_list)
                            db.session.commit()
                            db.session.refresh(Stock_performance_list)
                        else:
                            # Update existing record
                            symbol_id.one_day = data.get("1D", symbol_id.one_day)
                            symbol_id.five_day = data.get("5D", symbol_id.five_day)
                            symbol_id.one_month = data.get("1M", symbol_id.one_month)
                            symbol_id.three_month = data.get("3M", symbol_id.three_month)
                            symbol_id.six_month = data.get("6M", symbol_id.six_month)
                            symbol_id.ytd = data.get("ytd", symbol_id.ytd)
                            symbol_id.one_year = data.get("1Y", symbol_id.one_year)
                            symbol_id.three_year = data.get("3Y", symbol_id.three_year)
                            symbol_id.five_year = data.get("5Y", symbol_id.five_year)
                            symbol_id.ten_year = data.get("10Y", symbol_id.ten_year)
                            symbol_id.max_val = data.get("max", symbol_id.max_val)

                            db.session.commit()
                            db.session.refresh(symbol_id)

                return JSONResponse(status_code=200,content={"message": "Data Successfully Inserted."})
    except Exception as e:
        return HTTPException(status_code=403,detail=f"An Error Occured! {e.args}")
    

@router.get("/StockPerformance")
async def Stock_Performance( 
    symbol: Optional[str] = Query(None),
    exchange: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    limit: int = Query(10, le=100)
    ):
    try:
        skip = (page - 1) * limit
        query = db.session.query(StockPerformance)

        # Apply filters if query parameters are provided
        if symbol:
            query = query.filter(StockPerformance.symbol.ilike(f"%{symbol}%"))
        if exchange:
            query = query.filter(StockPerformance.exchange.ilike(f"%{exchange}%"))

        # Get the total count of users that match the filters
        total_count = query.count()

        # Apply pagination
        result = query.offset(skip).limit(limit).all()

        companies = [{  
                        "symbol": result.symbol,
                        "one_day": result.one_day,
                        "five_day": result.five_day,
                        "one_month": result.one_month,
                        "three_month": result.three_month,
                        "six_month": result.six_month,
                        "ytd": result.ytd,
                        "one_year": result.one_year,
                        "three_year": result.three_year,
                        "five_year": result.five_year,
                        "ten_year": result.ten_year,
                        "max_val": result.max_val,
                        
                    } for result in result]
    
        # Return paginated users and total count
        return JSONResponse(status_code = 200, content={"total": total_count, "Compines": companies})
    except Exception as e:
        return HTTPException(status_code=403,detail=f"An Error Occured! {e.args}")
    
@router.get("/UploadFinancialMetrics")
def Upload_FinancialMetrics():
    print("task4")

    params = {
        "apikey": os.getenv("API_KEY")
    }
    try:
        with db():
            with httpx.Client() as r:
                symbol_query = db.session.query(Symbols).all()


                for symbol in symbol_query:
                    response = r.get(f"{Stock_Ratio_URL}/{symbol.Csymbol}", params = params,  timeout=30)
                    res = response.json()

                    for data in res:
                        symbol_id = db.session.query(FinancialMetrics).filter(FinancialMetrics.symbol==symbol.Csymbol).first()
                        if not symbol_id:
                            financial_metrics_list = FinancialMetrics(
                                                            symbol = symbol.Csymbol,
                                                            dividendYielTTM =data.get("dividendYielTTM"), #--------
                                                            dividendYielPercentageTTM =data.get("dividendYielPercentageTTM"),
                                                            payoutRatioTTM =data.get("payoutRatioTTM") ,#----------
                                                            currentRatioTTM =data.get("currentRatioTTM"),#----------
                                                            quickRatioTTM =data.get("quickRatioTTM"), #----------
                                                            grossProfitMarginTTM =data.get("grossProfitMarginTTM"),
                                                            netProfitMarginTTM =data.get("netProfitMarginTTM"),
                                                            debtRatioTTM =data.get("debtRatioTTM"),
                                                            debtEquityRatioTTM =data.get("debtEquityRatioTTM"),
                                                            cashFlowToDebtRatioTTM =data.get("cashFlowToDebtRatioTTM"),
                                                            freeCashFlowPerShareTTM =data.get("freeCashFlowPerShareTTM"),
                                                            cashPerShareTTM =data.get("cashPerShareTTM"),
                                                            priceBookValueRatioTTM =data.get("priceBookValueRatioTTM"),
                                                            priceToBookRatioTTM =data.get("priceToBookRatioTTM"),
                                                            priceEarningsRatioTTM =data.get("priceEarningsRatioTTM"),
                                                            dividendPerShareTTM =data.get("dividendPerShareTTM")

                            )
                            db.session.add(financial_metrics_list)
                            db.session.commit()
                            db.session.refresh(financial_metrics_list)

                        else:
                            symbol_id.symbol = symbol.Csymbol
                            symbol_id.dividendYielTTM =data.get("dividendYielTTM")
                            symbol_id.dividendYielPercentageTTM =data.get("dividendYielPercentageTTM")
                            symbol_id.payoutRatioTTM =data.get("payoutRatioTTM")
                            symbol_id.currentRatioTTM =data.get("currentRatioTTM")
                            symbol_id.quickRatioTTM =data.get("quickRatioTTM")
                            symbol_id.grossProfitMarginTTM =data.get("grossProfitMarginTTM")
                            symbol_id.netProfitMarginTTM =data.get("netProfitMarginTTM")
                            symbol_id.debtRatioTTM =data.get("debtRatioTTM")
                            symbol_id.debtEquityRatioTTM =data.get("debtEquityRatioTTM")
                            symbol_id.cashFlowToDebtRatioTTM =data.get("cashFlowToDebtRatioTTM")
                            symbol_id.freeCashFlowPerShareTTM =data.get("freeCashFlowPerShareTTM")
                            symbol_id.cashPerShareTTM =data.get("cashPerShareTTM")
                            symbol_id.priceBookValueRatioTTM =data.get("priceBookValueRatioTTM")
                            symbol_id.priceToBookRatioTTM =data.get("priceToBookRatioTTM")
                            symbol_id.priceEarningsRatioTTM =data.get("priceEarningsRatioTTM")
                            symbol_id.dividendPerShareTTM =data.get("dividendPerShareTTM")

                            db.session.commit()
                            db.session.refresh(symbol_id)
                                
                return JSONResponse(status_code=200,content={"message": "Data Successfully Inserted."})
    except Exception as e:
        return HTTPException(status_code=403,detail=f"An Error Occured! {e.args}")

@router.get("/UploadTechnicalIndicator")
def Technical_Indicator():
    print("task5")

    params = {
        "type": "rsi",
        "period": 10,
        "apikey": os.getenv("API_KEY")
    }
    try:
        with db():
            with httpx.Client() as r:
                symbol_query = db.session.query(Symbols).all()

                for symbol in symbol_query:
                    response = r.get(f"{RSI_Technical_URL}/{symbol.Csymbol}", params = params,  timeout=30)
                    res = response.json()
                    
                    if res:
                        data = res[0]
                        formatted_date = datetime.strptime(data.get("date"), "%Y-%m-%d %H:%M:%S").date()
                        symbol_id = db.session.query(TechnicalIndicator).filter(
                            and_(
                                TechnicalIndicator.date ==  formatted_date,
                                TechnicalIndicator.symbol == symbol.Csymbol
                            )
                            ).first()
                        
                        if not symbol_id:
                            technical_indicator_list = TechnicalIndicator(
                                symbol = symbol.Csymbol,
                                date = formatted_date,
                                rsi = data.get("rsi")
                            )
                            db.session.add(technical_indicator_list)
                            db.session.commit()
                            db.session.refresh(technical_indicator_list)
                        else:
                            symbol_id.date = formatted_date
                            symbol_id.rsi = data.get("rsi", symbol_id.rsi)
                            db.session.commit()
                            db.session.refresh(symbol_id)

                return JSONResponse(status_code=200,content={"message": "Data Successfully Inserted."})
    except Exception as e:
        return HTTPException(status_code=403,detail=f"An Error Occured! {e.args}")

@router.get("/UploadFinancialGrowth")
def upload_financial_growth():
    print("task6")
    params = {
        "period": "annual",
        "apikey": os.getenv("API_KEY")
        }
    
    try:
        with db():
            with httpx.Client() as client:
                symbols = db.session.query(Symbols).all()

                # financial_growth_list = []

                for symbol in symbols:
                    response = client.get(f"{FINANCIAL_GROWTH_URL}/{symbol.Csymbol}", params=params, timeout=30)
                    res = response.json()
                    
                    if res:
                        data = res[0]
                        formatted_date = datetime.strptime(data.get("date"), "%Y-%m-%d").date()
                        
                        existing_record = db.session.query(FinancialGrowth).filter(
                            and_(
                                FinancialGrowth.date == formatted_date,
                                FinancialGrowth.symbol == symbol.Csymbol
                            )
                        ).first()
                        
                        if not existing_record:
                            financial_growth_list = FinancialGrowth(
                                symbol=data.get('symbol'),
                                date=data.get('date'),
                                calendarYear=data.get('calendarYear'),
                                period=data.get('period'),
                                revenueGrowth=data.get('revenueGrowth'),
                                grossProfitGrowth=data.get('grossProfitGrowth'),
                                ebitgrowth=data.get('ebitgrowth'),
                                netIncomeGrowth=data.get('netIncomeGrowth'),
                                epsgrowth=data.get('epsgrowth')
                            )
                            db.session.add(financial_growth_list)
                            db.session.commit()
                            db.session.refresh(financial_growth_list)
                        else:
                            existing_record.symbol = data.get('symbol', existing_record.symbol)
                            existing_record.date =data.get('date', existing_record.date)
                            existing_record.calendarYear=data.get('calendarYear', existing_record.calendarYear)
                            existing_record.period=data.get('period',existing_record.period)
                            existing_record.revenueGrowth=data.get('revenueGrowth',existing_record.revenueGrowth)
                            existing_record.grossProfitGrowth=data.get('grossProfitGrowth',existing_record.grossProfitGrowth)
                            existing_record.ebitgrowth=data.get('ebitgrowth',existing_record.ebitgrowth)
                            existing_record.netIncomeGrowth=data.get('netIncomeGrowth',existing_record.netIncomeGrowth)
                            existing_record.epsgrowth=data.get('epsgrowth',existing_record.epsgrowth)

                            db.session.commit()
                            db.session.refresh(existing_record)
            
                return JSONResponse({"message": "Financial Growth Data Successfully Inserted."})
    except Exception as e:
        return HTTPException(status_code=403, detail=f"An Error Occurred! {e.args}")

@router.get("/UploadStandardDevation")
def Standard_devation():
    print("task7")

    params = {
        "type": "standardDeviation",
        "period": 10,
        "apikey": os.getenv("API_KEY")
    }

    try:
        with db():
            with httpx.Client() as r:
                symbol_query = db.session.query(Symbols).all()


                for symbol in symbol_query:
                    response = r.get(f"{StandardDeviation_URL}/{symbol.Csymbol}", params = params,  timeout=30)
                    res = response.json()
                    
                    if res:
                        data = res[0]
                        formatted_date = datetime.strptime(data.get("date"), "%Y-%m-%d %H:%M:%S").date()
                        symbol_id = db.session.query(StandardDeviation).filter(
                            and_(
                                StandardDeviation.date ==  formatted_date,
                                StandardDeviation.symbol == symbol.Csymbol
                            )
                            ).first()
                        
                        if not symbol_id:
                            standarddevation_list = StandardDeviation(
                                symbol = symbol.Csymbol,
                                date = formatted_date,
                                std = data.get("standardDeviation")
                            )
                            db.session.add(standarddevation_list)
                            db.session.commit()
                            db.session.refresh(standarddevation_list)
                        else:
                            symbol_id.date = formatted_date
                            symbol_id.rsi = data.get("standardDeviation", symbol_id.std)
                            db.session.commit()
                            db.session.refresh(symbol_id)

                return JSONResponse(status_code=200,content={"message": "Data Successfully Inserted."})
    except Exception as e:
        return HTTPException(status_code=403,detail=f"An Error Occured! {e.args}")
    
def Myscheduler():
    scheduler = BackgroundScheduler(timezone=pytz.timezone('US/Eastern'))
    
    # Tasks running every 10 minutes
    frequent_trigger = CronTrigger(hour="9-16", minute="30/5", day_of_week="mon-fri", timezone='US/Eastern')
    
    # Tasks running once daily
    daily_trigger = CronTrigger(hour="9", day_of_week="mon-fri", timezone='US/Eastern')
    
    # Task 1 - Every 10 minutes
    scheduler.add_job(
        Upload_Stocks,
        trigger=frequent_trigger,
        id='my_task1',
        replace_existing=True,
        max_instances=2,
        misfire_grace_time=60,
        coalesce=True
    )
    
    # Task 2 - Once daily
    scheduler.add_job(
        Upload_CompanyProfile,
        trigger=daily_trigger,
        id='my_task2',
        replace_existing=True,
        max_instances=2,
        misfire_grace_time=60,
        coalesce=True
    )
    
    # Task 3 - Once daily
    scheduler.add_job(
        Upload_StocksPerformance,
        trigger=daily_trigger,
        id='my_task3',
        replace_existing=True,
        max_instances=3,
        misfire_grace_time=120,
        coalesce=True
    )
    
    # Task 4 - Once daily
    scheduler.add_job(
        Upload_FinancialMetrics,
        trigger=daily_trigger,
        id='my_task4',
        replace_existing=True,
        max_instances=3,
        misfire_grace_time=120,
        coalesce=True
    )
    
    # Task 5 - Every 10 minutes
    scheduler.add_job(
        Technical_Indicator,
        trigger=frequent_trigger,
        id='my_task5',
        replace_existing=True,
        max_instances=1,
        misfire_grace_time=120,
        coalesce=True
    )
    
    # Task 6 - Once daily
    scheduler.add_job(
        upload_financial_growth,
        trigger=daily_trigger,
        id='my_task6',
        replace_existing=True,
        max_instances=2,
        misfire_grace_time=60,
        coalesce=True
    )
    
    # Task 7 - Every 10 minutes
    scheduler.add_job(
        Standard_devation,
        trigger=frequent_trigger,
        id='my_task7',
        replace_existing=True,
        max_instances=2,
        misfire_grace_time=60,
        coalesce=True
    )
    
    scheduler.start()