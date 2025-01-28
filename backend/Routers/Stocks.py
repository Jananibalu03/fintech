from fastapi import APIRouter,HTTPException,Query, Depends
from fastapi.responses import JSONResponse
from Models.StocksModels import Symbols, StockInfo, CompanyProfile, StockPerformance
from dotenv import load_dotenv
import os
import httpx
from fastapi_sqlalchemy import db
from typing import List, Optional
import datetime
import math

load_dotenv()
router = APIRouter()

Symbol_Base_URL = "https://financialmodelingprep.com/api/v3/stock/list"

Stock_Base_URL = "https://financialmodelingprep.com/api/v3/quote"

Company_Base_URL = "https://financialmodelingprep.com/api/v3/profile"

Stock_Performance_URL = "https://financialmodelingprep.com/api/v3/stock-price-change"


@router.get("/UploadSymbols")
async def Upload_Symbols():
    params = {
        "apikey": os.getenv("API_KEY2")
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

def OneDayVolatility(day_high,day_low):
    if day_high !=0 and day_low !=0:
        # Calculate 1-day volatility using the high-low method
        volatility = math.sqrt(2) * math.log(day_high / day_low)
        volatility_percentage = volatility * 100
        rounded_2_decimal = round(volatility_percentage, 2)
        return  rounded_2_decimal
    else:
        return 0

@router.get("/UploadStocks")
async def Upload_Stocks():
    params = {
        "apikey": os.getenv("API_KEY2")
    }
    try:
        print(os.getenv("API_KEY2"))
        count = 0 
        with httpx.Client() as r:
            symbol_query = db.session.query(Symbols).all()
            for symbol in symbol_query:
                count+=1
                if count >30:
                    break
                response = r.get(f"{Stock_Base_URL}/{symbol.Csymbol}", params = params)
                print(response.headers)
                res = response.json()
                for data in res:
                    # symbol_id = db.session.query(Symbols).filter_by(Csymbol=data["symbol"]).first()
                    SctockDetails = StockInfo(  symbol = data["symbol"],
                                                name = data["name"],
                                                price = data["price"],
                                                changesPercentage = data["changesPercentage"],
                                                change = data["change"],
                                                dayLow = data["dayLow"],
                                                dayHigh = data["dayHigh"],
                                                yearHigh = data["yearHigh"],
                                                yearLow = data["yearLow"],
                                                marketCap = data["marketCap"],
                                                priceAvg50 = data["priceAvg50"],
                                                priceAvg200 = data["priceAvg200"],
                                                exchange = data["exchange"],
                                                volume = data["volume"],
                                                avgVolume = data["avgVolume"],
                                                open_price = data["open"] ,
                                                previousClose = data["previousClose"],
                                                eps  = data["eps"],
                                                pe = data["pe"],
                                                onedayvolatility = OneDayVolatility(data["dayHigh"],data["dayLow"]),
                                                timestamp =  data["timestamp"]
                                            )
                    db.session.add(SctockDetails)
                    db.session.commit()
                    db.session.refresh(SctockDetails)
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
                        "timestamp" :  datetime.datetime.fromtimestamp(result.timestamp).strftime("%Y-%m-%d %H:%M:%S")
                    } for result in result]
    
        # Return paginated users and total count
        return JSONResponse(status_code = 200, content={"total": total_count, "Compines": companies})
    except Exception as e:
        return HTTPException(status_code=403,detail=f"An Error Occured! {e.args}")
    

@router.get("/UploadCompanyProfiles")
async def Upload_CompanyProfile():
    params = {
        "apikey": os.getenv("API_KEY2")
    }
    try:
        count = 0 
        with httpx.Client() as r:
            symbol_query = db.session.query(Symbols).all()
            with httpx.Client() as r:
                for symbol in symbol_query:
                    count+=1
                    if count >30:
                        break
                    response = r.get(f"{Company_Base_URL}/{symbol.Csymbol}", params = params)
                    res = response.json()
                    for data in res:
                        # symbol_id = db.session.query(Symbols).filter_by(Csymbol=data["symbol"]).first()
                        CompanyDetails = CompanyProfile(   symbol=data["symbol"],
                                                            price=data["price"],
                                                            beta=data["beta"],
                                                            volAvg=data["volAvg"],
                                                            mktCap=data["mktCap"],
                                                            lastDiv=data["lastDiv"],
                                                            price_range=data["range"],
                                                            changes=data["changes"],
                                                            companyName=data["companyName"],
                                                            currency=data["currency"],
                                                            cik=data["cik"],
                                                            isin=data["isin"],
                                                            cusip=data["cusip"],
                                                            exchange=data["exchange"],
                                                            exchangeShortName=data["exchangeShortName"],
                                                            industry=data["industry"],
                                                            website=data["website"],
                                                            description=data["description"],
                                                            ceo=data["ceo"],
                                                            sector=data["sector"],
                                                            country=data["country"],
                                                            fullTimeEmployees=data["fullTimeEmployees"],
                                                            phone=data["phone"],
                                                            address=data["address"],
                                                            city=data["city"],
                                                            state=data["state"],
                                                            zip_code=data["zip"],
                                                            dcfDiff=data["dcfDiff"],
                                                            dcf=data["dcf"],
                                                            image=data["image"],
                                                            ipoDate=data["ipoDate"],
                                                            defaultImage=data["defaultImage"],
                                                            isEtf=data["isEtf"],
                                                            isActivelyTrading=data["isActivelyTrading"],
                                                            isAdr=data["isAdr"],
                                                            isFund=data["isFund"]
                                                    )

                        db.session.add(CompanyDetails)
                        db.session.commit()
                        db.session.refresh(CompanyDetails)
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
async def Upload_StocksPerformance():
    params = {
        "apikey": os.getenv("API_KEY2")
    }
    try:
        count = 0 
        with httpx.Client() as r:
            symbol_query = db.session.query(Symbols).all()
            for symbol in symbol_query:
                count+=1
                if count >30:
                    break
                response = r.get(f"{Stock_Performance_URL}/{symbol.Csymbol}", params = params)
                res = response.json()
                for data in res:
                    # symbol_id = db.session.query(Symbols).filter_by(Csymbol=data["symbol"]).first()
                    stock_performance = StockPerformance(
                                                            symbol=data["symbol"],
                                                            one_day=data["1D"],
                                                            five_day=data["5D"],
                                                            one_month=data["1M"],
                                                            three_month=data["3M"],
                                                            six_month=data["6M"],
                                                            ytd=data["ytd"],
                                                            one_year=data["1Y"],
                                                            three_year=data["3Y"],
                                                            five_year=data["5Y"],
                                                            ten_year=data["10Y"],
                                                            max_val=data["max"],
                                                        )
                    db.session.add(stock_performance)
                    db.session.commit()
                    db.session.refresh(stock_performance)
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