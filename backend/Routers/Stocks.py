from fastapi import APIRouter,HTTPException,Query, Depends
from fastapi.responses import JSONResponse
from Models.StocksModels import Symbols, StockInfo, CompanyProfile, StockPerformance, FinancialMetrics, TechnicalIndicator
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

load_dotenv()
router = APIRouter()

Symbol_Base_URL = "https://financialmodelingprep.com/api/v3/stock/list"

Stock_Base_URL = "https://financialmodelingprep.com/api/v3/quote"

Company_Base_URL = "https://financialmodelingprep.com/api/v3/profile"

Stock_Performance_URL = "https://financialmodelingprep.com/api/v3/stock-price-change"

Stock_Ratio_URL = "https://financialmodelingprep.com/api/v3/ratios-ttm"

RSI_Technical_URL = "https://financialmodelingprep.com/api/v3/technical_indicator/1day"

@router.get("/UploadSymbols")
async def Upload_Symbols():
    params = {
        "apikey": os.getenv("API_KEY4")
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
    print("tasked assigned")
    params = {
        "apikey": os.getenv("API_KEY4")
    }
    print(os.getenv("API_KEY4"))

    try:
        count = 0 
        with db():
            with httpx.Client() as r:
                symbol_query = db.session.query(Symbols).all()
                for symbol in symbol_query:
                    count+=1
                    if count >30:
                        break
                    response = r.get(f"{Stock_Base_URL}/{symbol.Csymbol}", params = params)
                    res = response.json()
                    # print(res)
                    for data in res:
                        StockInfoData = db.session.query(StockInfo).filter(StockInfo.symbol == symbol.Csymbol).order_by(StockInfo.id.desc()).first()
                        
                        if StockInfoData:
                            if datetime.fromtimestamp(StockInfoData.timestamp).strftime("%Y-%m-%d") != datetime.fromtimestamp(data.get('timestamp')).strftime("%Y-%m-%d"):

                                # symbol_id = db.session.query(Symbols).filter_by(Csymbol=data.get("symbol")).first()
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
                                                            onedayvolatility = OneDayVolatility(data.get("dayHigh"),data.get("dayLow")),
                                                            timestamp =  data.get("timestamp")
                                                        )
                                db.session.add(SctockDetails)
                                db.session.commit()
                                db.session.refresh(SctockDetails)
                            else:
                                # symbol_id = db.session.query(Symbols).filter_by(Csymbol=data.get("symbol")).first()
                                StockInfoData.symbol = data.get("symbol")
                                StockInfoData.name = data.get("name")
                                StockInfoData.price = data.get("price")
                                StockInfoData.changesPercentage = data.get("changesPercentage")
                                StockInfoData.change = data.get("change")
                                StockInfoData.dayLow = data.get("dayLow")
                                StockInfoData.dayHigh = data.get("dayHigh")
                                StockInfoData.yearHigh = data.get("yearHigh")
                                StockInfoData.yearLow = data.get("yearLow")
                                StockInfoData.marketCap = data.get("marketCap")
                                StockInfoData.priceAvg50 = data.get("priceAvg50")
                                StockInfoData.priceAvg200 = data.get("priceAvg200")
                                StockInfoData.exchange = data.get("exchange")
                                StockInfoData.volume = data.get("volume")
                                StockInfoData.avgVolume = data.get("avgVolume")
                                StockInfoData.open_price = data.get("open") 
                                StockInfoData.previousClose = data.get("previousClose")
                                StockInfoData.eps  = data.get("eps")
                                StockInfoData.pe = data.get("pe")
                                StockInfoData.onedayvolatility = OneDayVolatility(data.get("dayHigh"),data.get("dayLow"))
                                StockInfoData.timestamp =  data.get("timestamp")
                                db.session.commit()
                                db.session.refresh(StockInfoData)
                        else:
                            print("elseblock")
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
                                                        onedayvolatility = OneDayVolatility(data.get("dayHigh"),data.get("dayLow")),
                                                        timestamp =  data.get("timestamp")
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
                        "timestamp" :  datetime.fromtimestamp(result.timestamp).strftime("%Y-%m-%d %H:%M:%S")
                    } for result in result]
    
        # Return paginated users and total count
        return JSONResponse(status_code = 200, content={"total": total_count, "Compines": companies})
    except Exception as e:
        return HTTPException(status_code=403,detail=f"An Error Occured! {e.args}")
    

@router.get("/UploadCompanyProfiles")
async def Upload_CompanyProfile():
    params = {
        "apikey": os.getenv("API_KEY4")
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
                        # symbol_id = db.session.query(Symbols).filter_by(Csymbol=data.get("symbol")).first()
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
        "apikey": os.getenv("API_KEY4")
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
                    # symbol_id = db.session.query(Symbols).filter_by(Csymbol=data.get("symbol")).first()
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
async def Upload_FinancialMetrics():
    params = {
        "apikey": os.getenv("API_KEY4")
    }
    try:
        count = 0 
        with httpx.Client() as r:
            symbol_query = db.session.query(Symbols).all()
            for symbol in symbol_query:
                count+=1
                if count >30:
                    break
                response = r.get(f"{Stock_Ratio_URL}/{symbol.Csymbol}", params = params)
                res = response.json()
                for data in res:
                    # symbol_id = db.session.query(Symbols).filter_by(Csymbol=data.get("symbol")).first()
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
        return JSONResponse(status_code=200,content={"message": "Data Successfully Inserted."})
    except Exception as e:
        return HTTPException(status_code=403,detail=f"An Error Occured! {e.args}")

@router.get("/UploadTechnicalIndicator")
async def Technical_Indicator():
    params = {
        "type": "rsi",
        "period": 10,
        "apikey": os.getenv("API_KEY4")
    }
    try:
        count = 0 
        with httpx.Client() as r:
            symbol_query = db.session.query(Symbols).all()
            for symbol in symbol_query:
                count+=1
                if count >30:
                    break
                response = r.get(f"{RSI_Technical_URL}/{symbol.Csymbol}", params = params)
                res = response.json()
                data = res[0]
                # print(data)
                TechnicaldData = TechnicalIndicator(
                    symbol = symbol.Csymbol,
                    date = data.get("date"),
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

        return JSONResponse(status_code=200,content={"message": "Data Successfully Inserted."})
    except Exception as e:
        return HTTPException(status_code=403,detail=f"An Error Occured! {e.args}")

# Define the function that will be scheduled
async def my_task():
    # Get the current time in US Eastern Time
    eastern_timezone = pytz.timezone('US/Eastern')
    current_time = datetime.now(eastern_timezone)
    print("task triggered")
    # current_date = datetime.now(eastern_timezone).date()
    print(f"Task is running at {current_time}!")

# Initialize the scheduler
scheduler = BackgroundScheduler()


# Function to schedule the task using CronTrigger
# def Myscheduler():
#     # Define the cron trigger to run every 2 hours between 9:30 AM and 4 PM
#     trigger = CronTrigger(
#         hour="20-23",    # Every 2 hours between 9 and 16 (9:30 AM, 11:30 AM, etc.)
#         minute="45,46,47,48",    
#         day_of_week="mon-fri",  # At minute 30 (9:30, 11:30, etc.)
#         timezone="US/Eastern"
#     )

#     scheduler.add_job(
#         Upload_Stocks,
#         trigger=trigger,
#         id='my_task',  # Unique ID for this job
#         replace_existing=True  # Replace the existing job with the same ID if it exists
#     )
#     print("Cron job scheduled to run every 2 hours from 9:30 AM to 4 PM.")
#     scheduler.start()
#     print("Scheduler Started")

