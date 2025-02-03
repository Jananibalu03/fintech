from fastapi import APIRouter,HTTPException,Query, Depends
from fastapi.responses import JSONResponse
from Models.StocksModels import Symbols, StockInfo, CompanyProfile, StockPerformance, FinancialMetrics, TechnicalIndicator, FinancialGrowth
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
            'TGT', 'AXP', 'GS', 'CVX', 'MMM', 'UNH', 'AMT', 'SPGI', 'ABT'
        ]


        with httpx.Client() as r:
            response = r.get(Symbol_Base_URL, params = params)
            data = response.json()
            for comp in data:
                if comp["symbol"] in tickers:
                    StockCompany = Symbols(Csymbol = comp["symbol"], Cname = comp["name"], exchange = comp["exchangeShortName"])
                    db.session.add(StockCompany)
                    db.session.commit()
                    db.session.refresh(StockCompany)

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

def OneDayVolatility(symbol):
    params = {
        "type": "standardDeviation",
        "period": 10,
        "apikey": os.getenv("API_KEY")
    }
    if symbol:
        with httpx.Client() as r:
            res = r.get(f"{StandardDeviation_URL}/{symbol}",params=params,  timeout=30)
            response = res.json()[0]
            daily_volatility = response.get("standardDeviation")*100
            return f"{round(daily_volatility,2)}%"
    else:
        return None
            
     

@router.get("/UploadStocks")
def Upload_Stocks():
    print("task1")
    params = {
        "apikey": os.getenv("API_KEY")
    }
    print(os.getenv("API_KEY"))

    try:
        with db():
            with httpx.Client() as r:
                symbol_query = db.session.query(Symbols).all()
                for symbol in symbol_query:
                    response = r.get(f"{Stock_Base_URL}/{symbol.Csymbol}", params = params,  timeout=30)
                    res = response.json()
                    for data in res:
                        symbol_id = db.session.query(StockInfo).filter(StockInfo.symbol==symbol.Csymbol).first()
                        if not symbol_id:
                            SctockDetails = StockInfo(  symbol = data.get("symbol"),
                                                        name = data.get("name"),
                                                        price = data.get("price"),
                                                        changesPercentage = data.get("changesPercentage"),
                                                        change = data.get("change"),
                                                        dayLow = data.get("dayLow"),
                                                        dayHigh = data.get("dayHigh"),
                                                        yearHigh = data.get("yearHigh"),
                                                        yearLow = data.get("yearLow"),
                                                        marketCap = data.get("marketCap"),
                                                        priceAvg50 = data.get("priceAvg50"),
                                                        priceAvg200 = data.get("priceAvg200"),
                                                        exchange = data.get("exchange"),
                                                        volume = data.get("volume"),
                                                        avgVolume = data.get("avgVolume"),
                                                        open_price = data.get("open") ,
                                                        previousClose = data.get("previousClose"),
                                                        eps  = data.get("eps"),
                                                        pe = data.get("pe"),
                                                        onedayvolatility = OneDayVolatility(data.get('symbol')),
                                                        timestamp = datetime.fromtimestamp(data.get("timestamp")).strftime("%Y-%m-%d")
                                                    )
                            db.session.add(SctockDetails)
                            db.session.commit()
                            db.session.refresh(SctockDetails)
                        else:
                            # **Update existing StockInfo record**
                            symbol_id.name = data.get("name", symbol_id.name)
                            symbol_id.price = data.get("price", symbol_id.price)
                            symbol_id.changesPercentage = data.get("changesPercentage", symbol_id.changesPercentage)
                            symbol_id.change = data.get("change", symbol_id.change)
                            symbol_id.dayLow = data.get("dayLow", symbol_id.dayLow)
                            symbol_id.dayHigh = data.get("dayHigh", symbol_id.dayHigh)
                            symbol_id.yearHigh = data.get("yearHigh", symbol_id.yearHigh)
                            symbol_id.yearLow = data.get("yearLow", symbol_id.yearLow)
                            symbol_id.marketCap = data.get("marketCap", symbol_id.marketCap)
                            symbol_id.priceAvg50 = data.get("priceAvg50", symbol_id.priceAvg50)
                            symbol_id.priceAvg200 = data.get("priceAvg200", symbol_id.priceAvg200)
                            symbol_id.exchange = data.get("exchange", symbol_id.exchange)
                            symbol_id.volume = data.get("volume", symbol_id.volume)
                            symbol_id.avgVolume = data.get("avgVolume", symbol_id.avgVolume)
                            symbol_id.open_price = data.get("open", symbol_id.open_price)
                            symbol_id.previousClose = data.get("previousClose", symbol_id.previousClose)
                            symbol_id.eps = data.get("eps", symbol_id.eps)
                            symbol_id.pe = data.get("pe", symbol_id.pe)
                            symbol_id.onedayvolatility = OneDayVolatility(symbol_id.symbol)
                            symbol_id.timestamp = datetime.fromtimestamp(data.get("timestamp")).strftime("%Y-%m-%d")

                            db.session.commit()
                            db.session.refresh(symbol_id)   
                return JSONResponse(status_code=200,content={"message": "Data Successfully Inserted."})
    except Exception as e:
        return HTTPException(status_code=403,detail=f"An Error Occured! {e.args}")
    

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
                        "1Day Volatility": result.onedayvolatility,
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
                    response = r.get(f"{Company_Base_URL}/{symbol.Csymbol}", params = params)
                    res = response.json()
                    for data in res:
                        symbol_id = db.session.query(CompanyProfile).filter(CompanyProfile.symbol==symbol.Csymbol).first()
                        if not symbol_id:
                            CompanyDetails = CompanyProfile(   symbol=data.get("symbol"),
                                                                price=data.get("price"),
                                                                beta=data.get("beta"),
                                                                volAvg=data.get("volAvg"),
                                                                mktCap=data.get("mktCap"),
                                                                lastDiv=data.get("lastDiv"),
                                                                price_range=data.get("range"),
                                                                changes=data.get("changes"),
                                                                companyName=data.get("companyName"),
                                                                currency=data.get("currency"),
                                                                cik=data.get("cik"),
                                                                isin=data.get("isin"),
                                                                cusip=data.get("cusip"),
                                                                exchange=data.get("exchange"),
                                                                exchangeShortName=data.get("exchangeShortName"),
                                                                industry=data.get("industry"),
                                                                website=data.get("website"),
                                                                description=data.get("description"),
                                                                ceo=data.get("ceo"),
                                                                sector=data.get("sector"),
                                                                country=data.get("country"),
                                                                fullTimeEmployees=data.get("fullTimeEmployees"),
                                                                phone=data.get("phone"),
                                                                address=data.get("address"),
                                                                city=data.get("city"),
                                                                state=data.get("state"),
                                                                zip_code=data.get("zip"),
                                                                dcfDiff=data.get("dcfDiff"),
                                                                dcf=data.get("dcf"),
                                                                image=data.get("image"),
                                                                ipoDate=data.get("ipoDate"),
                                                                defaultImage=data.get("defaultImage"),
                                                                isEtf=data.get("isEtf"),
                                                                isActivelyTrading=data.get("isActivelyTrading"),
                                                                isAdr=data.get("isAdr"),
                                                                isFund=data.get("isFund")
                                                            )

                            db.session.add(CompanyDetails)
                            db.session.commit()
                            db.session.refresh(CompanyDetails)
                        else:
                            symbol_id.price = data.get("price", symbol_id.price)
                            symbol_id.beta = data.get("beta", symbol_id.beta)
                            symbol_id.volAvg = data.get("volAvg", symbol_id.volAvg)
                            symbol_id.mktCap = data.get("mktCap", symbol_id.mktCap)
                            symbol_id.lastDiv = data.get("lastDiv", symbol_id.lastDiv)
                            symbol_id.price_range = data.get("range", symbol_id.price_range)
                            symbol_id.changes = data.get("changes", symbol_id.changes)
                            symbol_id.companyName = data.get("companyName", symbol_id.companyName)
                            symbol_id.currency = data.get("currency", symbol_id.currency)
                            symbol_id.cik = data.get("cik", symbol_id.cik)
                            symbol_id.isin = data.get("isin", symbol_id.isin)
                            symbol_id.cusip = data.get("cusip", symbol_id.cusip)
                            symbol_id.exchange = data.get("exchange", symbol_id.exchange)
                            symbol_id.exchangeShortName = data.get("exchangeShortName", symbol_id.exchangeShortName)
                            symbol_id.industry = data.get("industry", symbol_id.industry)
                            symbol_id.website = data.get("website", symbol_id.website)
                            symbol_id.description = data.get("description", symbol_id.description)
                            symbol_id.ceo = data.get("ceo", symbol_id.ceo)
                            symbol_id.sector = data.get("sector", symbol_id.sector)
                            symbol_id.country = data.get("country", symbol_id.country)
                            symbol_id.fullTimeEmployees = data.get("fullTimeEmployees", symbol_id.fullTimeEmployees)
                            symbol_id.phone = data.get("phone", symbol_id.phone)
                            symbol_id.address = data.get("address", symbol_id.address)
                            symbol_id.city = data.get("city", symbol_id.city)
                            symbol_id.state = data.get("state", symbol_id.state)
                            symbol_id.zip_code = data.get("zip", symbol_id.zip_code)
                            symbol_id.dcfDiff = data.get("dcfDiff", symbol_id.dcfDiff)
                            symbol_id.dcf = data.get("dcf", symbol_id.dcf)
                            symbol_id.image = data.get("image", symbol_id.image)
                            symbol_id.ipoDate = data.get("ipoDate", symbol_id.ipoDate)
                            symbol_id.defaultImage = data.get("defaultImage", symbol_id.defaultImage)
                            symbol_id.isEtf = data.get("isEtf", symbol_id.isEtf)
                            symbol_id.isActivelyTrading = data.get("isActivelyTrading", symbol_id.isActivelyTrading)
                            symbol_id.isAdr = data.get("isAdr", symbol_id.isAdr)
                            symbol_id.isFund = data.get("isFund", symbol_id.isFund)
                            db.session.commit()  
                            db.session.refresh(symbol_id)
                return JSONResponse(status_code=200,content={"message": "Data Successfully Inserted."})
    except Exception as e:
        return HTTPException(status_code=403,detail=f"An Error Occured! {e.args}")
    

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
                        "price": result.price,
                        "beta" : result.beta,
                        "volAvg": result.volAvg,
                        "mktCap": result.mktCap,
                        "lastDiv": result.lastDiv,
                        "price_range": result.price_range,
                        "changes": result.changes,
                        "companyName": result.companyName,
                        "currency": result.currency,
                        "cik": result.cik,
                        "isin": result.isin,
                        "cusip": result.cusip,
                        "exchange": result.exchange,
                        "exchangeShortName": result.exchangeShortName,
                        "industry": result.industry,
                        "website": result.website,
                        "description": result.description,
                        "ceo": result.ceo,
                        "sector": result.sector,
                        "country": result.country,
                        "fullTimeEmployees": result.fullTimeEmployees,
                        "phone": result.phone,
                        "address": result.address,
                        "city": result.city,
                        "state": result.state,
                        "zip_code": result.zip_code,
                        "dcfDiff": result.dcfDiff,
                        "dcf": result.dcf,
                        "image": result.image,
                        "ipoDate":result.ipoDate.strftime("%Y-%m-%d"),
                        "defaultImage": result.defaultImage,
                        "isEtf": result.isEtf,
                        "isActivelyTrading": result.isActivelyTrading,
                        "isAdr": result.isAdr,
                        "isFund": result.isFund
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
            
                    response = r.get(f"{Stock_Performance_URL}/{symbol.Csymbol}", params = params)
                    res = response.json()
                    for data in res:
                        symbol_id = db.session.query(StockPerformance).filter(StockPerformance.symbol==symbol.Csymbol).first()
                        if not symbol_id:
                            stock_performance = StockPerformance(
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
                            db.session.add(stock_performance)
                            db.session.commit()
                            db.session.refresh(stock_performance)
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
                    response = r.get(f"{Stock_Ratio_URL}/{symbol.Csymbol}", params = params)
                    res = response.json()
                    for data in res:
                        symbol_id = db.session.query(FinancialMetrics).filter(FinancialMetrics.symbol==symbol.Csymbol).first()
                        if not symbol_id:
                            MetricsData = FinancialMetrics(
                                                            symbol = symbol.Csymbol,
                                                            dividendYielTTM =data.get("dividendYielTTM"), #--------
                                                            dividendYielPercentageTTM =data.get("dividendYielPercentageTTM"),
                                                            peRatioTTM =data.get("peRatioTTM"),
                                                            pegRatioTTM =data.get("pegRatioTTM"),
                                                            payoutRatioTTM =data.get("payoutRatioTTM") ,#----------
                                                            currentRatioTTM =data.get("currentRatioTTM"),#----------
                                                            quickRatioTTM =data.get("quickRatioTTM"), #----------
                                                            cashRatioTTM =data.get("cashRatioTTM"), #-----------
                                                            daysOfSalesOutstandingTTM =data.get("daysOfSalesOutstandingTTM"),
                                                            daysOfInventoryOutstandingTTM =data.get("daysOfInventoryOutstandingTTM"),
                                                            operatingCycleTTM =data.get("operatingCycleTTM"),
                                                            daysOfPayablesOutstandingTTM =data.get("daysOfPayablesOutstandingTTM"),
                                                            cashConversionCycleTTM =data.get("cashConversionCycleTTM"),
                                                            grossProfitMarginTTM =data.get("grossProfitMarginTTM"),
                                                            operatingProfitMarginTTM =data.get("operatingProfitMarginTTM"),
                                                            pretaxProfitMarginTTM =data.get("pretaxProfitMarginTTM"),
                                                            netProfitMarginTTM =data.get("netProfitMarginTTM"),
                                                            effectiveTaxRateTTM =data.get("effectiveTaxRateTTM"),
                                                            returnOnAssetsTTM =data.get("returnOnAssetsTTM"),
                                                            returnOnEquityTTM =data.get("returnOnEquityTTM"),
                                                            returnOnCapitalEmployedTTM =data.get("returnOnCapitalEmployedTTM"),
                                                            netIncomePerEBTTTM =data.get("netIncomePerEBTTTM"),
                                                            ebtPerEbitTTM =data.get("ebtPerEbitTTM"),
                                                            ebitPerRevenueTTM =data.get("ebitPerRevenueTTM"),
                                                            debtRatioTTM =data.get("debtRatioTTM"),
                                                            debtEquityRatioTTM =data.get("debtEquityRatioTTM"),
                                                            longTermDebtToCapitalizationTTM =data.get("longTermDebtToCapitalizationTTM"),
                                                            totalDebtToCapitalizationTTM =data.get("totalDebtToCapitalizationTTM"),
                                                            interestCoverageTTM =data.get("interestCoverageTTM"),
                                                            cashFlowToDebtRatioTTM =data.get("cashFlowToDebtRatioTTM"),
                                                            companyEquityMultiplierTTM =data.get("companyEquityMultiplierTTM"),
                                                            receivablesTurnoverTTM =data.get("receivablesTurnoverTTM"),
                                                            payablesTurnoverTTM =data.get("payablesTurnoverTTM"),
                                                            inventoryTurnoverTTM =data.get("inventoryTurnoverTTM"),
                                                            fixedAssetTurnoverTTM =data.get("fixedAssetTurnoverTTM"),
                                                            assetTurnoverTTM =data.get("assetTurnoverTTM"),
                                                            operatingCashFlowPerShareTTM =data.get("operatingCashFlowPerShareTTM"),
                                                            freeCashFlowPerShareTTM =data.get("freeCashFlowPerShareTTM"),
                                                            cashPerShareTTM =data.get("cashPerShareTTM"),
                                                            operatingCashFlowSalesRatioTTM =data.get("operatingCashFlowSalesRatioTTM"),
                                                            freeCashFlowOperatingCashFlowRatioTTM =data.get("freeCashFlowOperatingCashFlowRatioTTM"),
                                                            cashFlowCoverageRatiosTTM =data.get("cashFlowCoverageRatiosTTM"),
                                                            shortTermCoverageRatiosTTM =data.get("shortTermCoverageRatiosTTM"),
                                                            capitalExpenditureCoverageRatioTTM =data.get("capitalExpenditureCoverageRatioTTM"),
                                                            dividendPaidAndCapexCoverageRatioTTM =data.get("dividendPaidAndCapexCoverageRatioTTM"),
                                                            priceBookValueRatioTTM =data.get("priceBookValueRatioTTM"),
                                                            priceToBookRatioTTM =data.get("priceToBookRatioTTM"),
                                                            priceToSalesRatioTTM =data.get("priceToSalesRatioTTM"),
                                                            priceEarningsRatioTTM =data.get("priceEarningsRatioTTM"),
                                                            priceToFreeCashFlowsRatioTTM =data.get("priceToFreeCashFlowsRatioTTM"),
                                                            priceToOperatingCashFlowsRatioTTM =data.get("priceToOperatingCashFlowsRatioTTM"),
                                                            priceCashFlowRatioTTM =data.get("priceCashFlowRatioTTM"),
                                                            priceEarningsToGrowthRatioTTM =data.get("priceEarningsToGrowthRatioTTM"),
                                                            priceSalesRatioTTM =data.get("priceSalesRatioTTM"),
                                                            enterpriseValueMultipleTTM =data.get("enterpriseValueMultipleTTM"),
                                                            priceFairValueTTM =data.get("priceFairValueTTM"),
                                                            dividendPerShareTTM =data.get("dividendPerShareTTM")

                                                        )
                            db.session.add(MetricsData)
                            db.session.commit()
                            db.session.refresh(MetricsData)
                        else:
                            for field in [
                                            "dividendYielTTM", "dividendYielPercentageTTM", "peRatioTTM", "pegRatioTTM", "payoutRatioTTM",
                                            "currentRatioTTM", "quickRatioTTM", "cashRatioTTM", "daysOfSalesOutstandingTTM",
                                            "daysOfInventoryOutstandingTTM", "operatingCycleTTM", "daysOfPayablesOutstandingTTM",
                                            "cashConversionCycleTTM", "grossProfitMarginTTM", "operatingProfitMarginTTM",
                                            "pretaxProfitMarginTTM", "netProfitMarginTTM", "effectiveTaxRateTTM", "returnOnAssetsTTM",
                                            "returnOnEquityTTM", "returnOnCapitalEmployedTTM", "netIncomePerEBTTTM", "ebtPerEbitTTM",
                                            "ebitPerRevenueTTM", "debtRatioTTM", "debtEquityRatioTTM", "longTermDebtToCapitalizationTTM",
                                            "totalDebtToCapitalizationTTM", "interestCoverageTTM", "cashFlowToDebtRatioTTM",
                                            "companyEquityMultiplierTTM", "receivablesTurnoverTTM", "payablesTurnoverTTM",
                                            "inventoryTurnoverTTM", "fixedAssetTurnoverTTM", "assetTurnoverTTM",
                                            "operatingCashFlowPerShareTTM", "freeCashFlowPerShareTTM", "cashPerShareTTM",
                                            "operatingCashFlowSalesRatioTTM", "freeCashFlowOperatingCashFlowRatioTTM",
                                            "cashFlowCoverageRatiosTTM", "shortTermCoverageRatiosTTM",
                                            "capitalExpenditureCoverageRatioTTM", "dividendPaidAndCapexCoverageRatioTTM",
                                            "priceBookValueRatioTTM", "priceToBookRatioTTM", "priceToSalesRatioTTM",
                                            "priceEarningsRatioTTM", "priceToFreeCashFlowsRatioTTM",
                                            "priceToOperatingCashFlowsRatioTTM", "priceCashFlowRatioTTM",
                                            "priceEarningsToGrowthRatioTTM", "priceSalesRatioTTM", "enterpriseValueMultipleTTM",
                                            "priceFairValueTTM", "dividendPerShareTTM"
                                        ]:
                                setattr(symbol_id, field, data.get(field, getattr(symbol_id, field)))
                                db.session.commit()

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
                    response = r.get(f"{RSI_Technical_URL}/{symbol.Csymbol}", params = params)
                    res = response.json()
                    data = res[0]
                    formatted_date = datetime.strptime(data.get("date"), "%Y-%m-%d %H:%M:%S").date()
                    symbol_id = db.session.query(TechnicalIndicator).filter(
                       and_(
                            TechnicalIndicator.date ==  formatted_date,
                            TechnicalIndicator.symbol == symbol.Csymbol
                        )
                        ).first()
                    
                    if not symbol_id:
                        TechnicaldData = TechnicalIndicator(
                            symbol = symbol.Csymbol,
                            date = formatted_date,
                            open_price = data.get("open"),
                            high = data.get("high"),
                            low = data.get("low"),
                            close = data.get("close"),
                            volume = data.get("volume"),
                            rsi = data.get("rsi")
                        )
                        db.session.add(TechnicaldData)
                        db.session.commit()
                        db.session.refresh(TechnicaldData)
                    else:
                        symbol_id.date = formatted_date
                        symbol_id.open_price = data.get("open", symbol_id.open_price)
                        symbol_id.high = data.get("high", symbol_id.high)
                        symbol_id.low = data.get("low", symbol_id.low)
                        symbol_id.close = data.get("close", symbol_id.close)
                        symbol_id.volume = data.get("volume", symbol_id.volume)
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
                for symbol in symbols:
                    response = client.get(f"{FINANCIAL_GROWTH_URL}/{symbol.Csymbol}", params=params)
                    res = response.json()
                    data = res[0]
                    formatted_date = datetime.strptime(data.get("date"), "%Y-%m-%d").date()
                    
                    existing_record = db.session.query(FinancialGrowth).filter(
                        and_(
                            FinancialGrowth.date == formatted_date,
                            FinancialGrowth.symbol == symbol.Csymbol
                        )
                    ).first()
                    
                    if not existing_record:
                        entry = FinancialGrowth(
                            symbol=data.get('symbol'),
                            date=data.get('date'),
                            calendarYear=data.get('calendarYear'),
                            period=data.get('period'),
                            revenueGrowth=data.get('revenueGrowth'),
                            grossProfitGrowth=data.get('grossProfitGrowth'),
                            ebitgrowth=data.get('ebitgrowth'),
                            operatingIncomeGrowth=data.get('operatingIncomeGrowth'),
                            netIncomeGrowth=data.get('netIncomeGrowth'),
                            epsgrowth=data.get('epsgrowth'),
                            epsdilutedGrowth=data.get('epsdilutedGrowth'),
                            weightedAverageSharesGrowth=data.get('weightedAverageSharesGrowth'),
                            weightedAverageSharesDilutedGrowth=data.get('weightedAverageSharesDilutedGrowth'),
                            dividendsperShareGrowth=data.get('dividendsperShareGrowth'),
                            operatingCashFlowGrowth=data.get('operatingCashFlowGrowth'),
                            freeCashFlowGrowth=data.get('freeCashFlowGrowth'),
                            tenYRevenueGrowthPerShare=data.get('tenYRevenueGrowthPerShare'),
                            fiveYRevenueGrowthPerShare=data.get('fiveYRevenueGrowthPerShare'),
                            threeYRevenueGrowthPerShare=data.get('threeYRevenueGrowthPerShare'),
                            tenYOperatingCFGrowthPerShare=data.get('tenYOperatingCFGrowthPerShare'),
                            fiveYOperatingCFGrowthPerShare=data.get('fiveYOperatingCFGrowthPerShare'),
                            threeYOperatingCFGrowthPerShare=data.get('threeYOperatingCFGrowthPerShare'),
                            tenYNetIncomeGrowthPerShare=data.get('tenYNetIncomeGrowthPerShare'),
                            fiveYNetIncomeGrowthPerShare=data.get('fiveYNetIncomeGrowthPerShare'),
                            threeYNetIncomeGrowthPerShare=data.get('threeYNetIncomeGrowthPerShare'),
                            tenYShareholdersEquityGrowthPerShare=data.get('tenYShareholdersEquityGrowthPerShare'),
                            fiveYShareholdersEquityGrowthPerShare=data.get('fiveYShareholdersEquityGrowthPerShare'),
                            threeYShareholdersEquityGrowthPerShare=data.get('threeYShareholdersEquityGrowthPerShare'),
                            tenYDividendperShareGrowthPerShare=data.get('tenYDividendperShareGrowthPerShare'),
                            fiveYDividendperShareGrowthPerShare=data.get('fiveYDividendperShareGrowthPerShare'),
                            threeYDividendperShareGrowthPerShare=data.get('threeYDividendperShareGrowthPerShare'),
                            receivablesGrowth=data.get('receivablesGrowth'),
                            inventoryGrowth=data.get('inventoryGrowth'),
                            assetGrowth=data.get('assetGrowth'),
                            bookValueperShareGrowth=data.get('bookValueperShareGrowth'),
                            debtGrowth=data.get('debtGrowth'),
                            rdexpenseGrowth=data.get('rdexpenseGrowth'),
                            sgaexpensesGrowth=data.get('sgaexpensesGrowth')

                        )
                        db.session.add(entry)
                        db.session.commit()
                        db.session.refresh(entry)
                    else:
                        existing_record.symbol = data.get('symbol', existing_record.symbol)
                        existing_record.date = data.get('date', existing_record.date)
                        existing_record.calendarYear = data.get('calendarYear', existing_record.calendarYear)
                        existing_record.period = data.get('period', existing_record.period)
                        existing_record.revenueGrowth = data.get('revenueGrowth', existing_record.revenueGrowth)
                        existing_record.grossProfitGrowth = data.get('grossProfitGrowth', existing_record.grossProfitGrowth)
                        existing_record.ebitgrowth = data.get('ebitgrowth', existing_record.ebitgrowth)
                        existing_record.operatingIncomeGrowth = data.get('operatingIncomeGrowth', existing_record.operatingIncomeGrowth)
                        existing_record.netIncomeGrowth = data.get('netIncomeGrowth', existing_record.netIncomeGrowth)
                        existing_record.epsgrowth = data.get('epsgrowth', existing_record.epsgrowth)
                        existing_record.epsdilutedGrowth = data.get('epsdilutedGrowth', existing_record.epsdilutedGrowth)
                        existing_record.weightedAverageSharesGrowth = data.get('weightedAverageSharesGrowth', existing_record.weightedAverageSharesGrowth)
                        existing_record.weightedAverageSharesDilutedGrowth = data.get('weightedAverageSharesDilutedGrowth', existing_record.weightedAverageSharesDilutedGrowth)
                        existing_record.dividendsperShareGrowth = data.get('dividendsperShareGrowth', existing_record.dividendsperShareGrowth)
                        existing_record.operatingCashFlowGrowth = data.get('operatingCashFlowGrowth', existing_record.operatingCashFlowGrowth)
                        existing_record.freeCashFlowGrowth = data.get('freeCashFlowGrowth', existing_record.freeCashFlowGrowth)
                        existing_record.tenYRevenueGrowthPerShare = data.get('tenYRevenueGrowthPerShare', existing_record.tenYRevenueGrowthPerShare)
                        existing_record.fiveYRevenueGrowthPerShare = data.get('fiveYRevenueGrowthPerShare', existing_record.fiveYRevenueGrowthPerShare)
                        existing_record.threeYRevenueGrowthPerShare = data.get('threeYRevenueGrowthPerShare', existing_record.threeYRevenueGrowthPerShare)
                        existing_record.tenYOperatingCFGrowthPerShare = data.get('tenYOperatingCFGrowthPerShare', existing_record.tenYOperatingCFGrowthPerShare)
                        existing_record.fiveYOperatingCFGrowthPerShare = data.get('fiveYOperatingCFGrowthPerShare', existing_record.fiveYOperatingCFGrowthPerShare)
                        existing_record.threeYOperatingCFGrowthPerShare = data.get('threeYOperatingCFGrowthPerShare', existing_record.threeYOperatingCFGrowthPerShare)
                        existing_record.tenYNetIncomeGrowthPerShare = data.get('tenYNetIncomeGrowthPerShare', existing_record.tenYNetIncomeGrowthPerShare)
                        existing_record.fiveYNetIncomeGrowthPerShare = data.get('fiveYNetIncomeGrowthPerShare', existing_record.fiveYNetIncomeGrowthPerShare)
                        existing_record.threeYNetIncomeGrowthPerShare = data.get('threeYNetIncomeGrowthPerShare', existing_record.threeYNetIncomeGrowthPerShare)
                        existing_record.tenYShareholdersEquityGrowthPerShare = data.get('tenYShareholdersEquityGrowthPerShare', existing_record.tenYShareholdersEquityGrowthPerShare)
                        existing_record.fiveYShareholdersEquityGrowthPerShare = data.get('fiveYShareholdersEquityGrowthPerShare', existing_record.fiveYShareholdersEquityGrowthPerShare)
                        existing_record.threeYShareholdersEquityGrowthPerShare = data.get('threeYShareholdersEquityGrowthPerShare', existing_record.threeYShareholdersEquityGrowthPerShare)
                        existing_record.tenYDividendperShareGrowthPerShare = data.get('tenYDividendperShareGrowthPerShare', existing_record.tenYDividendperShareGrowthPerShare)
                        existing_record.fiveYDividendperShareGrowthPerShare = data.get('fiveYDividendperShareGrowthPerShare', existing_record.fiveYDividendperShareGrowthPerShare)
                        existing_record.threeYDividendperShareGrowthPerShare = data.get('threeYDividendperShareGrowthPerShare', existing_record.threeYDividendperShareGrowthPerShare)
                        existing_record.receivablesGrowth = data.get('receivablesGrowth', existing_record.receivablesGrowth)
                        existing_record.inventoryGrowth = data.get('inventoryGrowth', existing_record.inventoryGrowth)
                        existing_record.assetGrowth = data.get('assetGrowth', existing_record.assetGrowth)
                        existing_record.bookValueperShareGrowth = data.get('bookValueperShareGrowth', existing_record.bookValueperShareGrowth)
                        existing_record.debtGrowth = data.get('debtGrowth', existing_record.debtGrowth)
                        existing_record.rdexpenseGrowth = data.get('rdexpenseGrowth', existing_record.rdexpenseGrowth)
                        existing_record.sgaexpensesGrowth = data.get('sgaexpensesGrowth', existing_record.sgaexpensesGrowth)

                        db.session.commit()
                        db.session.refresh(existing_record)
            
            return {"message": "Financial Growth Data Successfully Inserted."}
    except Exception as e:
        return HTTPException(status_code=403, detail=f"An Error Occurred! {e.args}")
    
# Define the function that will be scheduled
async def my_task():
    # Get the current time in US Eastern Time
    eastern_timezone = pytz.timezone('US/Eastern')
    current_time = datetime.now(eastern_timezone)
    print("task triggered")
    # current_date = datetime.now(eastern_timezone).date()
    print(f"Task is running at {current_time}!")

# Initialize the scheduler
scheduler = BackgroundScheduler(timezone=pytz.timezone('US/Eastern'))


# Function to schedule the task using CronTrigger
def Myscheduler():
    # Define the cron trigger to run every 2 hours between 9:30 AM and 4 PM
    trigger = CronTrigger(
        hour="9-16",    # Every 2 hours between 9 and 16 (9:30 AM, 11:30 AM, etc.)
        minute="*",    
        day_of_week="mon-sun",  # At minute 30 (9:30, 11:30, etc.)
        timezone="US/Eastern",
    )

    scheduler.add_job(
        Upload_Stocks,
        trigger=trigger,
        id='my_task1',  # Unique ID for this job
        replace_existing=True,
        # max_instances=2  # Replace the existing job with the same ID if it exists
    )

    scheduler.add_job(
        Upload_CompanyProfile,
        trigger=trigger,
        id='my_task2',  # Unique ID for this job
        replace_existing=True,
        # max_instances=2,
        # misfire_grace_time=60,  # Runs even if delayed by 60 sec
        # coalesce=True
    )
    scheduler.add_job(
        Upload_StocksPerformance,
        trigger=trigger,
        id='my_task3',  # Unique ID for this job
        replace_existing=True,
        # max_instances=4,
        # misfire_grace_time=60,  # Runs even if delayed by 60 sec
        # coalesce=True
    )
    scheduler.add_job(
        Upload_FinancialMetrics,
        trigger=trigger,
        id='my_task4',  # Unique ID for this job
        replace_existing=True,
        # max_instances=4,
        # misfire_grace_time=60,  # Runs even if delayed by 60 sec
        # coalesce=True
    )

    scheduler.add_job(
        Technical_Indicator,
        trigger=trigger,
        id='my_task5',  # Unique ID for this job
        replace_existing=True,
        # max_instances=2,
        # misfire_grace_time=60,  # Runs even if delayed by 60 sec
        # coalesce=True
    )

    scheduler.add_job(
        upload_financial_growth,
        trigger=trigger,
        id='my_task6',  # Unique ID for this job
        replace_existing=True,
        # max_instances=2,
        # misfire_grace_time=60,  # Runs even if delayed by 60 sec
        # coalesce=True
    )


    print("Cron job scheduled to run every 2 hours from 9:30 AM to 4 PM.")
    scheduler.start()
    print("Scheduler Started")

