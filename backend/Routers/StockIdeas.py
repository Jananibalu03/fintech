from fastapi import APIRouter,HTTPException,Query
from Models.StocksModels import Symbols, StockInfo, StockPerformance, CompanyProfile, FinancialMetrics, TechnicalIndicator, FinancialGrowth, StandardDeviation
from fastapi_sqlalchemy import db
from fastapi.responses import JSONResponse
from typing import List, Optional
from sqlalchemy import or_, and_
import pytz
from datetime import datetime, timedelta
import httpx
import os
import pandas as pd
from sqlalchemy.orm import aliased
from sqlalchemy.sql import func
from sqlalchemy import cast, Float
import pandas as pd

StockIdeaRouter = APIRouter()

def format_large_number(value):
    if value >= 1_000_000_000:
        return f"{value / 1_000_000_000:.1f} B"  # For billions
    elif value >= 1_000_000:
        return f"{value / 1_000_000:.1f} M"  # For millions
    elif value >= 1_000:
        return f"{value / 1_000:.1f} K"  # For thousands
    else:
        return str(value)  # For values less than 1,000

def RoundTheValue(val):
    if not val:
        return None
    else:
        return round(val,2)

@StockIdeaRouter.get("/stock/volatility")
async def Volatility(
    Search: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    limit: int = Query(10, le=50)
    ):
    skip = max(0, (page - 1) * limit)

#     latest_stockinfo = db.session.query(
#         StockInfo.symbol,
#         func.max(StockInfo.id).label("latest_id")  # Get latest ID instead of timestamp
#     ).group_by(StockInfo.symbol).subquery()
#  outerjoin(
#                                 latest_stockinfo, Symbols.Csymbol == latest_stockinfo.c.symbol
#                             ).outerjoin(
#                                 StockInfo, and_(
#                                     Symbols.Csymbol == StockInfo.symbol,
#                                     StockInfo.id == latest_stockinfo.c.latest_id  # Use latest ID instead of timestamp
#                                 )
#                             ).\

    query = db.session.query(Symbols.Csymbol,Symbols.Cname,StandardDeviation.std,StockInfo.price,StockInfo.changesPercentage,StockInfo.volume,StockInfo.marketCap,
                            CompanyProfile.beta,CompanyProfile.sector,StockInfo.priceAvg50,StockInfo.priceAvg200, TechnicalIndicator.rsi,
                            StockPerformance.one_day,StockPerformance.one_month,StockPerformance.one_year, FinancialMetrics.dividendYielTTM).\
                            outerjoin(StockInfo,Symbols.Csymbol == StockInfo.symbol).\
                            outerjoin(StockPerformance, Symbols.Csymbol == StockPerformance.symbol).\
                            outerjoin(FinancialMetrics, Symbols.Csymbol == FinancialMetrics.symbol).\
                            outerjoin(TechnicalIndicator, Symbols.Csymbol == TechnicalIndicator.symbol).\
                            outerjoin(StandardDeviation, Symbols.Csymbol == StandardDeviation.symbol).\
                            outerjoin(CompanyProfile, Symbols.Csymbol == CompanyProfile.symbol).order_by(StockInfo.price.desc())


    # query = query.filter(StockInfo.price > 100.00)


    if Search:
        query = query.filter(
            or_(
                Symbols.Csymbol.ilike(f"%{Search}%"),
                Symbols.Cname.ilike(f"%{Search}%"),
                CompanyProfile.sector.ilike(f"%{Search}%")  

            )
        )

        results = query.all()
        if not results:  # Check if results is empty
            return JSONResponse({
                "message": "No data found",
            }, status_code=404)
        
        result =[{ 
                "Symbol": result.Csymbol if result.Csymbol is not None else None,
                "Name": result.Cname if result.Cname is not None else None,
                "Price": f"{round(result.price,2)} USD" if result.price is not None else None,
                "Change": f"{result.changesPercentage}%" if result.changesPercentage is not None else None,
                "1DVolatility": f"{round(result.std,2)}%" if result.std is not None else None,
                "1D": result.one_day if result.one_day is not None else None,
                "1M": result.one_month if result.one_month is not None else None,
                "1Y": result.one_year if result.one_year is not None else None,
                "Volume": format_large_number(result.volume) if result.volume is not None else None,
                "MarketCap": format_large_number(result.marketCap) if result.marketCap  is not None else None,
                "SMA50": result.priceAvg50 if result.priceAvg50 is not None else None,
                "SMA200": result.priceAvg200 if result.priceAvg200 is not None else None,
                "Beta":result.beta if result.beta is not None else None,
                "DividendYieldTTM":result.dividendYielTTM if result.dividendYielTTM is not None else None, 
                "RSI": result.rsi if result.rsi is not None else None,
                "Sector": result.sector if result.sector is not None else None
            } 
            for result in results]
        
        total = query.count()
        total_pages = (total + limit - 1) // limit

        return JSONResponse({
            "data": result,
            "total_pages": total_pages,
            "total_records": total,
            "current_pages": page
            },status_code = 200)
    
    else:

        total = query.count()
        total_pages = (total + limit - 1) // limit

        results = query.offset(skip).limit(limit).all()

        result =[{ 
                    "Symbol": result.Csymbol if result.Csymbol  is not None else None,
                    "Name": result.Cname if result.Cname is not None else None,
                    "Price": f"{round(result.price,2)} USD" if result.price is not None else None,
                    "Change": f"{result.changesPercentage}%" if result.changesPercentage is not None else None,
                    "1DVolatility": f"{round(result.std,2)}%" if result.std is not None else None,
                    "1D": result.one_day if result.one_day is not None else None,
                    "1M": result.one_month if result.one_month is not None else None,
                    "1Y": result.one_year if result.one_year is not None else None,
                    "Volume": format_large_number(result.volume) if result.volume is not None else None,
                    "MarketCap": format_large_number(result.marketCap) if result.marketCap is not None else None,
                    "SMA50": result.priceAvg50 if result.priceAvg50 is not None else None,
                    "SMA200": result.priceAvg200 if result.priceAvg200 is not None else None,
                    "Beta":result.beta if result.beta is not None else None,
                    "DividendYieldTTM":result.dividendYielTTM if result.dividendYielTTM is not None else None, 
                    "RSI": result.rsi if result.rsi is not None else None,
                    "Sector": result.sector if result.sector is not None else None
                } 
                for result in results]
        
        return JSONResponse({
            "data": result,
            "total_pages": total_pages,
            "total_records": total,
            "current_pages": page
        },status_code = 200)
    
@StockIdeaRouter.get("/stock/52weekshigh")
async def YearHigh(
    Search: Optional[str] = Query(None),
    page: int = Query(1),
    limit: int = Query(10)
    ):
    skip = max(0, (page - 1) * limit)

    
    query = db.session.query(Symbols.Csymbol,Symbols.Cname,StockInfo.price,StockInfo.changesPercentage,StockInfo.volume,StockInfo.marketCap,
                            StockInfo.yearHigh,StockInfo.yearLow,CompanyProfile.beta,CompanyProfile.sector,StockInfo.priceAvg50,StockInfo.priceAvg200, 
                            StockPerformance.one_day,StockPerformance.one_month,StockPerformance.one_year, FinancialMetrics.dividendYielTTM, TechnicalIndicator.rsi).\
                            outerjoin(StockInfo,Symbols.Csymbol == StockInfo.symbol).\
                            outerjoin(StockPerformance, Symbols.Csymbol == StockPerformance.symbol).\
                            outerjoin(FinancialMetrics, Symbols.Csymbol == FinancialMetrics.symbol).\
                            outerjoin(TechnicalIndicator, Symbols.Csymbol == TechnicalIndicator.symbol).\
                            outerjoin(CompanyProfile, Symbols.Csymbol == CompanyProfile.symbol).order_by(StockInfo.price.desc())
    
    threshold = 0.95
    query = query.filter(StockInfo.price >= StockInfo.yearHigh * threshold)
 
    if Search:
        query = query.filter(
            or_(
                Symbols.Csymbol.ilike(f"%{Search}%"),
                Symbols.Cname.ilike(f"%{Search}%"),
                CompanyProfile.sector.ilike(f"%{Search}%")  
            )
        )

        results = query.all()
        if not results:  
            return JSONResponse({
                "message": "No data found"
            }, status_code=404)
        
        result =[{ 
                    "Symbol": result.Csymbol if result.Csymbol is not None else None,
                    "Name": result.Cname if result.Cname is not None else None,
                    "Price": f"{round(result.price,2)} USD" if result.price is not None else None,
                    "Change": f"{result.changesPercentage}%" if result.changesPercentage is not None else None,
                    "1D": result.one_day if result.one_day is not None else None,
                    "1M": result.one_month if result.one_month is not None else None,
                    "1Y": result.one_year if result.one_year is not None else None,
                    "Volume": format_large_number(result.volume) if result.volume is not None else None,
                    "MarketCap": format_large_number(result.marketCap) if result.marketCap is not None else None,
                    "52WeeksHigh": result.yearHigh if result.yearHigh is not None else None,
                    "52WeeksLow": result.yearLow if result.yearLow is not None else None,
                    "SMA50": result.priceAvg50 if result.priceAvg50 is not None else None,
                    "SMA200": result.priceAvg200 if result.priceAvg200 is not None else None,
                    "Beta":result.beta if result.beta is not None else None,
                    "RSI": result.rsi if result.rsi is not None else None,
                    "DividendYieldTTM": result.dividendYielTTM if result.dividendYielTTM is not None else None, 
                    "Sector": result.sector if result.sector is not None else None
                } 
            for result in results]
        
        total = query.count()
        total_pages = (total + limit - 1) // limit

        return JSONResponse({
            "data": result,
            "total_pages": total_pages,
            "total_records": total,
            "current_pages": page
            },status_code=200)
    else:
        
        total = query.count()
        total_pages = (total + limit - 1) // limit
        results = query.offset(skip).limit(limit).all()

        result =[{ 
                    "Symbol": result.Csymbol if result.Csymbol is not None else None,
                    "Name": result.Cname if result.Cname is not None else None,
                    "Price": f"{round(result.price,2)} USD" if result.price is not None else None,
                    "Change": f"{result.changesPercentage}%" if result.changesPercentage is not None else None,
                    "1D": result.one_day if result.one_day is not None else None,
                    "1M": result.one_month if result.one_month is not None else None,
                    "1Y": result.one_year if result.one_year is not None else None,
                    "Volume": format_large_number(result.volume) if result.volume is not None else None,
                    "MarketCap": format_large_number(result.marketCap) if result.marketCap is not None else None,
                    "52WeeksHigh": result.yearHigh if result.yearHigh is not None else None,
                    "52WeeksLow": result.yearLow if result.yearLow is not None else None,
                    "SMA50": result.priceAvg50 if result.priceAvg50 is not None else None,
                    "SMA200": result.priceAvg200 if result.priceAvg200 is not None else None,
                    "Beta":result.beta if result.beta is not None else None,
                    "RSI": result.rsi if result.rsi  is not None else None,
                    "DividendYieldTTM": result.dividendYielTTM if result.dividendYielTTM is not None else None, 
                    "Sector": result.sector if result.sector is not None else None
                } 
                for result in results]
        return JSONResponse({
            "data": result,
            "total_pages": total_pages,
            "total_records": total,
            "current_page": page
        },status_code = 200)

@StockIdeaRouter.get("/stock/52weekslow")
async def YearLow(
    Search: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    limit: int = Query(10, le=100)
    ):
    skip = (page - 1) * limit
    query = db.session.query(Symbols.Csymbol,Symbols.Cname,StockInfo.price,StockInfo.changesPercentage,StockInfo.volume,StockInfo.marketCap,
                            StockInfo.yearHigh,StockInfo.yearLow,CompanyProfile.beta,CompanyProfile.sector,StockInfo.priceAvg50,StockInfo.priceAvg200, 
                            StockPerformance.one_day,StockPerformance.one_month,StockPerformance.one_year,FinancialMetrics.dividendYielTTM,TechnicalIndicator.rsi).\
                            outerjoin(StockInfo,Symbols.Csymbol == StockInfo.symbol).\
                            outerjoin(StockPerformance, Symbols.Csymbol == StockPerformance.symbol).\
                            outerjoin(FinancialMetrics, Symbols.Csymbol == FinancialMetrics.symbol).\
                            outerjoin(TechnicalIndicator, Symbols.Csymbol == TechnicalIndicator.symbol).\
                            outerjoin(CompanyProfile, Symbols.Csymbol == CompanyProfile.symbol).order_by(StockInfo.price.desc())
    threshold = 1.05
    query = query.filter(StockInfo.price <= StockInfo.yearLow * threshold)

    if Search:
        query = query.filter(
            or_(
                Symbols.Csymbol.ilike(f"%{Search}%"),
                Symbols.Cname.ilike(f"%{Search}%"),
                CompanyProfile.sector.ilike(f"%{Search}%")  

            )
        )
        results = query.all()
        if not results:
            return JSONResponse({
                "message": "No data found"
            }, status_code=404)
        
        result =[{ 
                    "Symbol": result.Csymbol if result.Csymbol is not None else None,
                    "Name": result.Cname if result.Cname is not None else None,
                    "Price": f"{round(result.price,2)} USD" if result.price is not None else None,
                    "Change": f"{result.changesPercentage}%" if result.changesPercentage is not None else None,
                    "1D": result.one_day if result.one_day is not None else None,
                    "1M": result.one_month if result.one_month is not None else None,
                    "1Y": result.one_year if result.one_year is not None else None,
                    "Volume": format_large_number(result.volume) if result.volume is not None else None,
                    "Marketap": format_large_number(result.marketCap) if result.marketCap is not None else None,
                    "52WeeksHigh": result.yearHigh if result.yearHigh is not None else None,
                    "52WeeksLow": result.yearLow if result.yearLow is not None else None,
                    "SMA50": result.priceAvg50 if result.priceAvg50 is not None else None,
                    "SMA200": result.priceAvg200 if result.priceAvg200 is not None else None,
                    "Beta":result.beta if result.beta is not None else None,
                    "RSI": result.rsi if result.rsi is not None else None,
                    "DividendYieldTTM": result.dividendYielTTM if result.dividendYielTTM is not None else None, 
                    "Sector": result.sector if result.sector is not None else None
                } 
              for result in results]
        
        total = query.count()
        total_pages = (total + limit - 1) // limit

        return JSONResponse({
            "data": result,
            "total_pages": total_pages,
            "total_records": total,
            "current_pages": page
            },status_code = 200)
    else:
    # query = query.filter(StockInfo.price <= StockInfo.yearLow)
        total = query.count()
        total_pages = (total + limit - 1) // limit

       
        results = query.offset(skip).limit(limit).all()

        result =[{ 
                   "Symbol": result.Csymbol if result.Csymbol is not None else None,
                    "Name": result.Cname if result.Cname is not None else None,
                    "Price": f"{round(result.price,2)} USD" if result.price is not None  else None,
                    "Change": f"{result.changesPercentage}%" if result.changesPercentage is not None else None,
                    "1D": result.one_day if result.one_day is not None else None,
                    "1M": result.one_month if result.one_month is not None else None,
                    "1Y": result.one_year if result.one_year is not None else None,
                    "Volume": format_large_number(result.volume) if result.volume is not None else None,
                    "Marketap": format_large_number(result.marketCap) if result.marketCap is not None  else None,
                    "52WeeksHigh": result.yearHigh if result.yearHigh is not None else None,
                    "52WeeksLow": result.yearLow if result.yearLow is not None else None,
                    "SMA50": result.priceAvg50 if result.priceAvg50 is not None else None,
                    "SMA200": result.priceAvg200 if result.priceAvg200 is not None else None,
                    "Beta":result.beta if result.beta is not None else None,
                    "RSI": result.rsi if result.rsi is not None else None,
                    "DividendYieldTTM": result.dividendYielTTM if result.dividendYielTTM is not None else None, 
                    "Sector": result.sector if result.sector is not None else None
                } 
                for result in results]

        return JSONResponse({
            "data": result,
            "total_pages": total_pages,
            "total_records": total,
            "current_pages": page
            },status_code = 200)

@StockIdeaRouter.get("/stock/undertendollar")
async def UnderTen_Dollar(
    Search: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    limit: int = Query(10, le=100)
    ):
    skip = (page - 1) * limit
    query = db.session.query(Symbols.Csymbol,Symbols.Cname,StockInfo.price,StandardDeviation.std,StockInfo.changesPercentage,StockInfo.volume,StockInfo.marketCap,
                            StockInfo.pe,StockInfo.eps,StockInfo.yearHigh,StockInfo.yearLow,CompanyProfile.beta,CompanyProfile.sector,StockInfo.priceAvg50,StockInfo.priceAvg200, 
                            StockPerformance.one_day,StockPerformance.one_month,StockPerformance.one_year,TechnicalIndicator.rsi).\
                            outerjoin(StockInfo,Symbols.Csymbol == StockInfo.symbol).\
                            outerjoin(StockPerformance, Symbols.Csymbol == StockPerformance.symbol).\
                            outerjoin(TechnicalIndicator, Symbols.Csymbol == TechnicalIndicator.symbol).\
                            outerjoin(StandardDeviation, Symbols.Csymbol == StandardDeviation.symbol).\
                            outerjoin(CompanyProfile, Symbols.Csymbol == CompanyProfile.symbol).order_by(StockInfo.price.desc())
    
    query = query.filter(StockInfo.price <= 10.0)

    if Search:
        query = query.filter(
            or_(
                Symbols.Csymbol.ilike(f"%{Search}%"),
                Symbols.Cname.ilike(f"%{Search}%"),
                CompanyProfile.sector.ilike(f"%{Search}%")  

            )
        )
        results = query.all()
        if not results:  # Check if results is empty
            return JSONResponse({
                "message": "No data found",
                
            }, status_code=404)
            
        result =[{ 
                    "Symbol": result.Csymbol if result.Csymbol is not None else None,
                    "Name": result.Cname if result.Cname is not None else None,
                    "Price": f"{round(result.price,2)} USD" if result.price is not None  else None,
                    "Change": f"{result.changesPercentage}%" if result.changesPercentage is not None else None,
                    "1DVolatility": f"{round(result.std,2)}%" if result.std is not None else None,
                    "1D": result.one_day if result.one_day is not None else None,
                    "1M": result.one_month if result.one_month is not None else None,
                    "1Y": result.one_year if result.one_year is not None  else None,
                    "Volume": format_large_number(result.volume) if result.volume is not None else None,
                    "MarketCap": format_large_number(result.marketCap) if result.marketCap is not None else None,
                    "SMA50": result.priceAvg50 if result.priceAvg50 is not None else None,
                    "SMA200": result.priceAvg200 if result.priceAvg200 is not None else None,
                    "Beta":result.beta if result.beta is not None else None,
                    "RSI": result.rsi if result.rsi is not None else None,
                    "PERatio": result.pe if result.pe is not None else None,
                    "EPS": result.eps if result.eps is not None else None,
                    "Sector": result.sector if result.sector is not None else None
                } 
              for result in results]
        
        total = query.count()
        total_pages = (total + limit - 1) // limit

        return JSONResponse({
            "data": result,
            "total_pages": total_pages,
            "total_records": total,
            "current_pages": page
            },status_code = 200)

    else:
        
        total = query.count()
        total_pages = (total + limit - 1) // limit

        # query = query.filter(StockInfo.price <= StockInfo.yearLow)

        results = query.offset(skip).limit(limit).all()

        result =[{ 
                    "Symbol": result.Csymbol if result.Csymbol is not None else None,
                    "Name": result.Cname if result.Cname is not None else None,
                    "Price": f"{round(result.price,2)} USD" if result.price is not None else None,
                    "Change": f"{result.changesPercentage}%" if result.changesPercentage is not None else None,
                    "1DVolatility": f"{round(result.std,2)}%" if result.std is not None else None,
                    "1D": result.one_day if result.one_day is not None else None,
                    "1M": result.one_month if result.one_month is not None else None,
                    "1Y": result.one_year if result.one_year is not None else None,
                    "Volume": format_large_number(result.volume) if result.volume is not None else None,
                    "MarketCap": format_large_number(result.marketCap) if result.marketCap is not None else None,
                    "SMA50": result.priceAvg50 if result.priceAvg50 is not None else None,
                    "SMA200": result.priceAvg200 if result.priceAvg200 is not None else None,
                    "Beta":result.beta if result.beta is not None else None,
                    "RSI": result.rsi if result.rsi is not None else None,
                    "PERatio": result.pe if result.pe is not None else None,
                    "EPS": result.eps if result.eps is not None else None,
                    "Sector": result.sector if result.sector is not None else None
                } 
                for result in results]

        return JSONResponse({
            "data": result,
            "total_pages": total_pages,
            "total_records": total,
            "current_pages": page
            },status_code = 200)

@StockIdeaRouter.get("/stock/abovetendoller")
async def AboveTen_Dollar(
    Search: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    limit: int = Query(10, le=100)
    ):
    skip = (page - 1) * limit
    query = db.session.query(Symbols.Csymbol,Symbols.Cname,StockInfo.price,StandardDeviation.std,StockInfo.changesPercentage,StockInfo.volume,StockInfo.marketCap,
                            StockInfo.pe,StockInfo.eps,StockInfo.yearHigh,StockInfo.yearLow,CompanyProfile.beta,CompanyProfile.sector,StockInfo.priceAvg50,StockInfo.priceAvg200, 
                            StockPerformance.one_day,StockPerformance.one_month,StockPerformance.one_year,TechnicalIndicator.rsi).\
                            outerjoin(StockInfo,Symbols.Csymbol == StockInfo.symbol).\
                            outerjoin(StockPerformance, Symbols.Csymbol == StockPerformance.symbol).\
                            outerjoin(TechnicalIndicator, Symbols.Csymbol == TechnicalIndicator.symbol).\
                            outerjoin(StandardDeviation, Symbols.Csymbol == StandardDeviation.symbol).\
                            outerjoin(CompanyProfile, Symbols.Csymbol == CompanyProfile.symbol).order_by(StockInfo.price.desc())
    
    query = query.filter(StockInfo.price <= 50.0)

    if Search:
        query = query.filter(
            or_(
                Symbols.Csymbol.ilike(f"%{Search}%"),
                Symbols.Cname.ilike(f"%{Search}%"),
                CompanyProfile.sector.ilike(f"%{Search}%")  

            )
        )
        results = query.all()
        if not results:  # Check if results is empty
            return JSONResponse({
                "message": "No data found"
            
            }, status_code=404)
        
        result =[{ 
                    "Symbol": result.Csymbol if result.Csymbol else None,
                    "Name": result.Cname if result.Cname else None,
                    "Price": f"{round(result.price,2)} USD" if result.price is not None else None,
                    "Change": f"{result.changesPercentage}%" if result.changesPercentage is not None else None,
                    "1DVolatility": f"{round(result.std,2)}%" if result.std is not None else None,
                    "1D": result.one_day if result.one_day is not None else None,
                    "1M": result.one_month if result.one_month is not None else None,
                    "1Y": result.one_year if result.one_year is not None else None,
                    "Volume": format_large_number(result.volume) if result.volume is not None else None,
                    "MarketCap": format_large_number(result.marketCap) if result.marketCap is not None else None,
                    "SMA50": result.priceAvg50 if result.priceAvg50 is not None else None,
                    "SMA200": result.priceAvg200 if result.priceAvg200 is not None else None,
                    "Beta": result.beta if result.beta is not None else None,
                    "RSI": result.rsi if result.rsi is not None else None,
                    "PERatio": result.pe if result.pe is not None else None,
                    "EPS": result.eps if result.eps is not None else None,
                    "Sector": result.sector if result.sector is not None else None
                } 
              for result in results]
        
        total = query.count()
        total_pages = (total + limit - 1) // limit

        return JSONResponse({
            "data": result,
            "total_pages": total_pages,
            "total_records": total,
            "current_pages": page
        }, status_code = 200)

    else:

        total = query.count()
        total_pages = (total + limit - 1) // limit

        # query = query.filter(StockInfo.price <= StockInfo.yearLow)

        results = query.offset(skip).limit(limit).all()

        result =[{ 
                   "Symbol": result.Csymbol if result.Csymbol is not None else None,
                    "Name": result.Cname if result.Cname is not None else None,
                    "Price": f"{round(result.price,2)} USD" if result.price is not None else None,
                    "Change": f"{result.changesPercentage}%" if result.changesPercentage is not None else None,
                    "1DVolatility": f"{round(result.std,2)}%" if result.std is not None else None,
                    "1D": result.one_day if result.one_day is not None else None,
                    "1M": result.one_month if result.one_month is not None else None,
                    "1Y": result.one_year if result.one_year is not None else None,
                    "Volume": format_large_number(result.volume) if result.volume is not None else None,
                    "MarketCap": format_large_number(result.marketCap) if result.marketCap is not None else None,
                    "SMA50": result.priceAvg50 if result.priceAvg50 is not None else None,
                    "SMA200": result.priceAvg200 if result.priceAvg200 is not None else None,
                    "Beta": result.beta if result.beta is not None else None,
                    "RSI": result.rsi if result.rsi is not None else None,
                    "PERatio": result.pe if result.pe is not None else None,
                    "EPS": result.eps if result.eps is not None else None,
                    "Sector": result.sector if result.sector is not None else None
                } 
                for result in results]

        return JSONResponse({
            "data": result,
            "total_pages": total_pages,
            "total_records": total,
            "current_pages": page
        },status_code = 200)

@StockIdeaRouter.get("/stock/negativebeta")
async def NegativeBeta(
    Search: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    limit: int = Query(10, le=100)
    ):
    skip = (page - 1) * limit
    query = db.session.query(Symbols.Csymbol,Symbols.Cname,StockInfo.price,StandardDeviation.std,StockInfo.changesPercentage,StockInfo.volume,StockInfo.marketCap,
                            StockInfo.pe,StockInfo.eps,StockInfo.yearHigh,StockInfo.yearLow,CompanyProfile.beta,CompanyProfile.sector,StockInfo.priceAvg50,StockInfo.priceAvg200, 
                            StockPerformance.one_day,StockPerformance.one_month,StockPerformance.one_year,TechnicalIndicator.rsi).\
                            outerjoin(StockInfo,Symbols.Csymbol == StockInfo.symbol).\
                            outerjoin(StockPerformance, Symbols.Csymbol == StockPerformance.symbol).\
                            outerjoin(TechnicalIndicator, Symbols.Csymbol == TechnicalIndicator.symbol).\
                            outerjoin(StandardDeviation, Symbols.Csymbol == StandardDeviation.symbol).\
                            outerjoin(CompanyProfile, Symbols.Csymbol == CompanyProfile.symbol).order_by(StockInfo.price.desc())

    query = query.filter(CompanyProfile.beta < 0)

    if Search:
        query = query.filter(
            or_(
                Symbols.Csymbol.ilike(f"%{Search}%"),
                Symbols.Cname.ilike(f"%{Search}%"),
             
                CompanyProfile.sector.ilike(f"%{Search}%")  

            )
        )
        results = query.all()
        if not results:  # Check if results is empty
            return JSONResponse({
                "message": "No data found"
            }, status_code=404)
        
        result =[{ 
                    "Symbol": result.Csymbol if result.Csymbol is not None else None,
                    "Name": result.Cname if result.Cname is not None else None,
                    "Price": f"{round(result.price,2)} USD" if result.price is not None else None,
                    "Change": f"{result.changesPercentage}%" if result.changesPercentage is not None else None,
                    "1DVolatility": f"{round(result.std,2)}%" if result.std is not None else None,
                    "1D": result.one_day if result.one_day is not None else None,
                    "1M": result.one_month if result.one_month is not None else None,
                    "1Y": result.one_year if result.one_year is not None else None,
                    "Volume": format_large_number(result.volume) if result.volume is not None else None,
                    "MarketCap": format_large_number(result.marketCap) if result.marketCap is not None else None,
                    "52WeeksHigh": result.yearHigh if result.yearHigh is not None else None,
                    "52WeeksLow": result.yearLow if result.yearLow is not None else None,
                    "SMA50": result.priceAvg50 if result.priceAvg50 is not None else None,
                    "SMA200": result.priceAvg200 if result.priceAvg200 is not None else None,
                    "Beta": result.beta if result.beta is not None else None,
                    "RSI": result.rsi if result.rsi is not None else None,
                    "Sector": result.sector if result.sector is not None else None
                }
              for result in results]
        
        total = query.count()
        total_pages = (total + limit - 1) // limit

        return JSONResponse({
            "data": result,
            "total_pages": total_pages,
            "total_records": total,
            "current_pages": page
        },status_code = 200)
    else:

        total = query.count()
        total_pages = (total + limit - 1) // limit

        # query = query.filter(StockInfo.price <= StockInfo.yearLow)

        results = query.offset(skip).limit(limit).all()

        result =[{ 
                    "Symbol": result.Csymbol if result.Csymbol is not None else None,
                    "Name": result.Cname if result.Cname is not None else None,
                    "Price": f"{round(result.price,2)} USD" if result.price is not None else None,
                    "Change": f"{result.changesPercentage}%" if result.changesPercentage is not None else None,
                    "1DVolatility": f"{round(result.std,2)}%" if result.std is not None else None,
                    "1D": result.one_day if result.one_day is not None else None,
                    "1M": result.one_month if result.one_month is not None else None,
                    "1Y": result.one_year if result.one_year is not None else None,
                    "Volume": format_large_number(result.volume) if result.volume is not None else None,
                    "MarketCap": format_large_number(result.marketCap) if result.marketCap is not None else None,
                    "52WeeksHigh": result.yearHigh if result.yearHigh is not None else None,
                    "52WeeksLow": result.yearLow if result.yearLow is not None else None,
                    "SMA50": result.priceAvg50 if result.priceAvg50 is not None else None,
                    "SMA200": result.priceAvg200 if result.priceAvg200 is not None else None,
                    "Beta": result.beta if result.beta is not None else None,
                    "RSI": result.rsi if result.rsi is not None else None,
                    "Sector": result.sector if result.sector is not None else None
                } 
                for result in results]

        return JSONResponse({
            "data": result,
            "total_pages": total_pages,
            "total_records": total,
            "current_pages": page
        },status_code = 200)

@StockIdeaRouter.get("/stock/lowbeta")
async def LowBeta(
    Search: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    limit: int = Query(10, le=100)
    ):
    skip = (page - 1) * limit
    query = db.session.query(Symbols.Csymbol,Symbols.Cname,StockInfo.price,StandardDeviation.std,StockInfo.changesPercentage,StockInfo.volume,StockInfo.marketCap,
                            StockInfo.pe,StockInfo.eps,StockInfo.yearHigh,StockInfo.yearLow,CompanyProfile.beta,CompanyProfile.sector,StockInfo.priceAvg50,StockInfo.priceAvg200, 
                            StockPerformance.one_day,StockPerformance.one_month,StockPerformance.one_year,TechnicalIndicator.rsi).\
                            outerjoin(StockInfo,Symbols.Csymbol == StockInfo.symbol).\
                            outerjoin(StockPerformance, Symbols.Csymbol == StockPerformance.symbol).\
                            outerjoin(TechnicalIndicator, Symbols.Csymbol == TechnicalIndicator.symbol).\
                            outerjoin(StandardDeviation, Symbols.Csymbol == StandardDeviation.symbol).\
                            outerjoin(CompanyProfile, Symbols.Csymbol == CompanyProfile.symbol).order_by(StockInfo.price.desc())

    query = query.filter(or_(
        CompanyProfile.beta <= 0,
        CompanyProfile.beta < 1
    ))

    if Search:
        query = query.filter(
            or_(
                Symbols.Csymbol.ilike(f"%{Search}%"),
                Symbols.Cname.ilike(f"%{Search}%"),
                CompanyProfile.sector.ilike(f"%{Search}%")  

            )
        )
        results = query.all()

        if not results:  # Check if results is empty
            return JSONResponse({
                "message": "No data found"
            }, status_code=404)
        
        result =[{ 
                    "Symbol": result.Csymbol if result.Csymbol is not None else None,
                    "Name": result.Cname if result.Cname is not None else None,
                    "Price": f"{round(result.price,2)} USD" if result.price is not None else None,
                    "Change": f"{result.changesPercentage}%" if result.changesPercentage is not None else None,
                    "1DVolatility": f"{round(result.std,2)}%" if result.std is not None else None,
                    "1D": result.one_day if result.one_day is not None else None,
                    "1M": result.one_month if result.one_month is not None else None,
                    "1Y": result.one_year if result.one_year is not None else None,
                    "Volume": format_large_number(result.volume) if result.volume is not None else None,
                    "MarketCap": format_large_number(result.marketCap) if result.marketCap is not None else None,
                    "52WeeksHigh": result.yearHigh if result.yearHigh is not None else None,
                    "52WeeksLow": result.yearLow if result.yearLow is not None else None,
                    "SMA50": result.priceAvg50 if result.priceAvg50 is not None else None,
                    "SMA200": result.priceAvg200 if result.priceAvg200 is not None else None,
                    "Beta": result.beta if result.beta is not None else None,
                    "RSI": result.rsi if result.rsi is not None else None,
                    "Sector": result.sector if result.sector is not None else None,
                } 
              for result in results]
        
        total = query.count()
        total_pages = (total + limit - 1) // limit

        return JSONResponse({
            "data": result,
            "total_pages": total_pages,
            "total_records": total,
            "current_pages": page
        },status_code = 200)
    else:
        total = query.count()
        total_pages = (total + limit - 1) // limit

        # query = query.filter(StockInfo.price <= StockInfo.yearLow)

        results = query.offset(skip).limit(limit).all()

        result =[{ 
                    "Symbol": result.Csymbol if result.Csymbol is not None else None,
                    "Name": result.Cname if result.Cname is not None else None,
                    "Price": f"{round(result.price,2)} USD" if result.price is not None else None,
                    "Change": f"{result.changesPercentage}%" if result.changesPercentage is not None else None,
                    "1DVolatility": f"{round(result.std)}" if result.std is not None else None,
                    "1D": result.one_day if result.one_day is not None else None,
                    "1M": result.one_month if result.one_month is not None else None,
                    "1Y": result.one_year if result.one_year is not None else None,
                    "Volume": format_large_number(result.volume) if result.volume is not None else None,
                    "MarketCap": format_large_number(result.marketCap) if result.marketCap is not None else None,
                    "52WeeksHigh": result.yearHigh if result.yearHigh is not None else None,
                    "52WeeksLow": result.yearLow if result.yearLow is not None else None,
                    "SMA50": result.priceAvg50 if result.priceAvg50 is not None else None,
                    "SMA200": result.priceAvg200 if result.priceAvg200 is not None else None,
                    "Beta": result.beta if result.beta is not None else None,
                    "RSI": result.rsi if result.rsi is not None else None,
                    "Sector": result.sector if result.sector is not None else None,
                } 
                for result in results]

        
        return JSONResponse({
            "data": result,
            "total_pages": total_pages,
            "total_records": total,
            "current_pages": page
        },status_code = 200)

@StockIdeaRouter.get("/stock/highriskandreward")
async def HighRisk_Reward(
    Search: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    limit: int = Query(10, le=100)
    ):
    skip = (page - 1) * limit
    query = db.session.query(Symbols.Csymbol,Symbols.Cname,StockInfo.price,StandardDeviation.std,StockInfo.changesPercentage,StockInfo.volume,StockInfo.marketCap,
                            StockInfo.pe,StockInfo.eps,StockInfo.yearHigh,StockInfo.yearLow,CompanyProfile.beta,CompanyProfile.sector,StockInfo.priceAvg50,StockInfo.priceAvg200, 
                            StockPerformance.one_day,StockPerformance.one_month,StockPerformance.one_year,FinancialMetrics.priceBookValueRatioTTM,FinancialMetrics.debtEquityRatioTTM,\
                            FinancialMetrics.dividendYielTTM,FinancialMetrics.priceEarningsRatioTTM,TechnicalIndicator.rsi).\
                            outerjoin(StockInfo,Symbols.Csymbol == StockInfo.symbol).\
                            outerjoin(StockPerformance, Symbols.Csymbol == StockPerformance.symbol).\
                            outerjoin(FinancialMetrics, Symbols.Csymbol == FinancialMetrics.symbol).\
                            outerjoin(TechnicalIndicator, Symbols.Csymbol == TechnicalIndicator.symbol).\
                            outerjoin(StandardDeviation, Symbols.Csymbol == StandardDeviation.symbol).\
                            outerjoin(CompanyProfile, Symbols.Csymbol == CompanyProfile.symbol).order_by(StockInfo.price.desc())
    
    #  # Query for high-risk, high-reward stocks
    query = query.filter(
        or_(

            StandardDeviation.std > 5,  # Filter for high volatility, e.g., daily volatility > 5%
            StockInfo.marketCap < 1000000000,  # Filter for small market cap (less than 1 billion)
            CompanyProfile.beta > 1,  # Filter for high beta stocks (greater than 1)
            StockInfo.pe > 20  # Filter for high P/E ratio (indicative of high growth potential)
        )
    )
    
    if Search:
        query = query.filter(
            or_(
                Symbols.Csymbol.ilike(f"%{Search}%"),
                Symbols.Cname.ilike(f"%{Search}%"),
                CompanyProfile.sector.ilike(f"%{Search}%")  

            )
        )
        results = query.all()

        if not results:  # Check if results is empty
            return JSONResponse({
                "message": "No data found"
            }, status_code=404)
        
        result =[{ 
                    "Symbol": result.Csymbol if result.Csymbol is not None else None,
                    "Name": result.Cname if result.Cname is not None else None,
                    "Price": f"{round(result.price,2)} USD" if result.price is not None else None,
                    "Change": f"{result.changesPercentage}%" if result.changesPercentage is not None else None,
                    "1DVolatility": f"{round(result.std,2)}%" if result.std is not None else None,
                    "1D": result.one_day if result.one_day is not None else None,
                    "1M": result.one_month if result.one_month is not None else None,
                    "1Y": result.one_year if result.one_year is not None else None,
                    "Volume": format_large_number(result.volume) if result.volume is not None else None,
                    "MarketCap": format_large_number(result.marketCap) if result.marketCap is not None else None,
                    "52WeeksHigh": result.yearHigh if result.yearHigh is not None else None,
                    "52WeeksLow": result.yearLow if result.yearLow is not None else None,
                    "SMA50": result.priceAvg50 if result.priceAvg50 is not None else None,
                    "SMA200": result.priceAvg200 if result.priceAvg200 is not None else None,
                    "Beta": result.beta if result.beta is not None else None,
                    "RSI": result.rsi if result.rsi is not None else None,
                    "PERatio": result.pe if result.pe is not None else None,
                    "PBRatioTTM": result.priceBookValueRatioTTM if result.priceBookValueRatioTTM is not None else None,
                    "EarningGrowthTTM": result.priceEarningsRatioTTM if result.priceEarningsRatioTTM is not None else None,
                    "DebttoEquityTTM": result.debtEquityRatioTTM if result.debtEquityRatioTTM is not None else None,
                    "RisktoRewardRatioTTM": "pending",  # Keeping as "pending" since it's hardcoded
                    "DividendYieldTTM": result.dividendYielTTM if result.dividendYielTTM is not None else None,
                    "Sector": result.sector if result.sector is not None else None
                } 
              for result in results]
        
        total = query.count()
        total_pages = (total + limit - 1) // limit

        return JSONResponse({
            "data": result,
            "total_pages": total_pages,
            "total_records": total,
            "current_pages": page
        },status_code = 200)
    
    else:
                
        total = query.count()
        total_pages = (total + limit - 1) // limit

        # query = query.filter(StockInfo.price <= StockInfo.yearLow)

        results = query.offset(skip).limit(limit).all()

        result =[{ 
                    "Symbol": result.Csymbol if result.Csymbol is not None else None ,
                    "Name": result.Cname if result.Cname is not None else None,
                    "Price": f"{round(result.price,2)} USD" if result.price is not None else None,
                    "Change": f"{result.changesPercentage}%" if result.changesPercentage is not None else None,
                    "1DVolatility": f"{round(result.std,2)}%" if result.std is not None else None,
                    "1D": result.one_day if result.one_day is not None else None,
                    "1M": result.one_month if result.one_month is not None else None,
                    "1Y": result.one_year if result.one_year is not None else None,
                    "Volume": format_large_number(result.volume) if result.volume is not None else None,
                    "MarketCap": format_large_number(result.marketCap) if result.marketCap is not None else None,
                    "52WeeksHigh": result.yearHigh if result.yearHigh is not None else None,
                    "52WeeksLow": result.yearLow if result.yearLow is not None else None,
                    "SMA50": result.priceAvg50 if result.priceAvg50 is not None else None,
                    "SMA200": result.priceAvg200 if result.priceAvg200 is not None else None,
                    "Beta": result.beta if result.beta is not None else None,
                    "RSI": result.rsi if result.rsi is not None else None,
                    "PERatio": result.pe if result.pe is not None else None,
                    "PBRatioTTM": result.priceBookValueRatioTTM if result.priceBookValueRatioTTM is not None else None,
                    "EarningGrowthTTM": result.priceEarningsRatioTTM if result.priceEarningsRatioTTM is not None else None,
                    "DebttoEquityTTM": result.debtEquityRatioTTM if result.debtEquityRatioTTM is not None else None,
                    "RisktoRewardRatioTTM": "pending",  # Keeping as "pending" since it's hardcoded
                    "DividendYieldTTM": result.dividendYielTTM if result.dividendYielTTM is not None else None,
                    "Sector": result.sector if result.sector is not None else None
                } 
                for result in results]


        return JSONResponse({
            "data": result,
            "total_pages": total_pages,
            "total_records": total,
            "current_pages": page
        },status_code = 200)

@StockIdeaRouter.get("/stock/debtfreestocks")
async def DebtFree_Stocks(
    Search: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    limit: int = Query(10, le=100)
    ):
    skip = (page - 1) * limit
    query = db.session.query(Symbols.Csymbol,Symbols.Cname,StockInfo.price,StandardDeviation.std,StockInfo.changesPercentage,StockInfo.volume,StockInfo.marketCap,
                            StockInfo.pe,StockInfo.eps,StockInfo.yearHigh,StockInfo.yearLow,CompanyProfile.beta,CompanyProfile.sector,StockInfo.priceAvg50,StockInfo.priceAvg200, 
                            StockPerformance.one_day,StockPerformance.one_month,StockPerformance.one_year,FinancialMetrics.currentRatioTTM,FinancialMetrics.quickRatioTTM,FinancialMetrics.freeCashFlowPerShareTTM,
                            FinancialMetrics.payoutRatioTTM,FinancialMetrics.netProfitMarginTTM,FinancialGrowth.revenueGrowth,FinancialMetrics.debtEquityRatioTTM).\
                            outerjoin(StockInfo,Symbols.Csymbol == StockInfo.symbol).\
                            outerjoin(StockPerformance, Symbols.Csymbol == StockPerformance.symbol).\
                            outerjoin(FinancialMetrics, Symbols.Csymbol == FinancialMetrics.symbol).\
                            outerjoin(FinancialGrowth, Symbols.Csymbol == FinancialGrowth.symbol).\
                            outerjoin(StandardDeviation, Symbols.Csymbol == StandardDeviation.symbol).\
                            outerjoin(CompanyProfile, Symbols.Csymbol == CompanyProfile.symbol).order_by(StockInfo.price.desc())
    
    query = query.filter(FinancialMetrics.debtEquityRatioTTM == 0)
    if Search:
        query = query.filter(
            or_(
                Symbols.Csymbol.ilike(f"%{Search}%"),
                Symbols.Cname.ilike(f"%{Search}%"),
                CompanyProfile.sector.ilike(f"%{Search}%")  

            )
        )
        results = query.all()
        
        if not results:
            return JSONResponse({"message": "data not found"},status_code=404)
        
        result =[{ 
                    "Symbol": result.Csymbol if result.Csymbol is not None else None,
                    "Name": result.Cname if result.Cname is not None else None,
                    "Price": f"{round(result.price,2)} USD" if result.price is not None else None,
                    "Change": f"{result.changesPercentage}%" if result.changesPercentage is not None else None,
                    "1DVolatility": f"{round(result.std,2)}%" if result.std is not None else None,
                    "Volume": format_large_number(result.volume) if result.volume is not None else None,
                    "MarketCap": format_large_number(result.marketCap) if result.marketCap is not None else None,
                    "Beta": result.beta if result.beta is not None else None,
                    "PERatio": result.pe if result.pe is not None else None,
                    "CurrentRatioTTM": result.currentRatioTTM if result.currentRatioTTM is not None else None,
                    "QuickRatioTTM": result.quickRatioTTM if result.quickRatioTTM is not None else None,
                    "FreeCashFlowTTM": result.freeCashFlowPerShareTTM if result.freeCashFlowPerShareTTM is not None else None,
                    "ProfitMarginsTTM": result.netProfitMarginTTM if result.netProfitMarginTTM is not None else None,
                    "DividendPayoutRatioTTM": result.payoutRatioTTM if result.payoutRatioTTM is not None else None,
                    "RevenueGrowthTTM": result.revenueGrowth if result.revenueGrowth is not None else None,
                    "debtEquityRatioTTM": result.debtEquityRatioTTM if result.debtEquityRatioTTM is not None else None,
                    "Sector": result.sector if result.sector is not None else None
              } 
              for result in results]
        
        total = query.count()
        total_pages = (total + limit - 1) // limit

        return JSONResponse({
            "data": result,
            "total_pages": total_pages,
            "total_records": total,
            "current_pages": page
        },status_code = 200)
    else:
        total = query.count()
        total_pages = (total + limit - 1) // limit

        # query = query.filter(StockInfo.price <= StockInfo.yearLow)

        results = query.offset(skip).limit(limit).all()

        result =[{ 
                    "Symbol": result.Csymbol if result.Csymbol is not None else None,
                    "Name": result.Cname if result.Cname is not None else None,
                    "Price": f"{round(result.price,2)} USD" if result.price is not None else None,
                    "Change": f"{result.changesPercentage}%" if result.changesPercentage is not None else None,
                    "1DVolatility": f"{round(result.std,2)}%" if result.std is not None else None,
                    "Volume": format_large_number(result.volume) if result.volume is not None else None,
                    "MarketCap": format_large_number(result.marketCap) if result.marketCap is not None else None,
                    "Beta": result.beta if result.beta is not None else None,
                    "PERatio": result.pe if result.pe is not None else None,
                    "CurrentRatioTTM": result.currentRatioTTM if result.currentRatioTTM is not None else None,
                    "QuickRatioTTM": result.quickRatioTTM if result.quickRatioTTM is not None else None,
                    "FreeCashFlowTTM": result.freeCashFlowPerShareTTM if result.freeCashFlowPerShareTTM is not None else None,
                    "ProfitMarginsTTM": result.netProfitMarginTTM if result.netProfitMarginTTM is not None else None,
                    "DividendPayoutRatioTTM": result.payoutRatioTTM if result.payoutRatioTTM is not None else None,
                    "RevenueGrowthTTM": result.revenueGrowth if result.revenueGrowth is not None else None,
                    "Sector": result.sector if result.sector is not None else None
                } 
                for result in results]

        return JSONResponse({
            "data": result,
            "total_pages": total_pages,
            "total_records": total,
            "current_pages": page
        },status_code = 200)

@StockIdeaRouter.get("/stock/dividend")
async def Dividend(
    Search: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    limit: int = Query(10, le=100)
    ):
    skip = (page - 1) * limit
    query = db.session.query(Symbols.Csymbol,Symbols.Cname,StockInfo.price,StandardDeviation.std,StockInfo.changesPercentage,StockInfo.volume,StockInfo.marketCap,
                            StockInfo.pe,StockInfo.eps,StockInfo.yearHigh,StockInfo.yearLow,CompanyProfile.beta,CompanyProfile.sector,StockInfo.priceAvg50,StockInfo.priceAvg200, 
                            StockPerformance.one_day,StockPerformance.one_month,StockPerformance.one_year,FinancialMetrics.freeCashFlowPerShareTTM,FinancialMetrics.payoutRatioTTM,
                            FinancialMetrics.netProfitMarginTTM,FinancialMetrics.dividendYielTTM,FinancialGrowth.revenueGrowth,FinancialMetrics.dividendYielPercentageTTM).\
                            outerjoin(StockInfo,Symbols.Csymbol == StockInfo.symbol).\
                            outerjoin(StockPerformance, Symbols.Csymbol == StockPerformance.symbol).\
                            outerjoin(FinancialMetrics, Symbols.Csymbol == FinancialMetrics.symbol).\
                            outerjoin(FinancialGrowth, Symbols.Csymbol == FinancialGrowth.symbol).\
                            outerjoin(StandardDeviation, Symbols.Csymbol == StandardDeviation.symbol).\
                            outerjoin(CompanyProfile, Symbols.Csymbol == CompanyProfile.symbol).order_by(StockInfo.price.desc())

    query = query.filter(FinancialMetrics.dividendYielPercentageTTM >= 3 )

    if Search:
        query = query.filter(
            or_(
                Symbols.Csymbol.ilike(f"%{Search}%"),
                Symbols.Cname.ilike(f"%{Search}%"),
                CompanyProfile.sector.ilike(f"%{Search}%")  

            )
        )
        results = query.all()
        if not results:
            return JSONResponse({"message": "data not found"},status_code = 404)
        result =[{ 
                    "Symbol": result.Csymbol if result.Csymbol is not None else None,
                    "Name": result.Cname if result.Cname is not None else None,
                    "Price": f"{round(result.price,2)} USD" if result.price is not None else None,
                    "Change": f"{result.changesPercentage}%" if result.changesPercentage is not None else None,
                    "1DVolatility": f"{round(result.std,2)}%" if result.std is not None else None,
                    "Volume": format_large_number(result.volume) if result.volume is not None else None,
                    "MarketCap": format_large_number(result.marketCap) if result.marketCap is not None else None,
                    "DividendYieldTTM": result.dividendYielTTM if result.dividendYielTTM is not None else None,
                    "EPS": result.eps if result.eps is not None else None,
                    "Beta": result.beta if result.beta is not None else None,
                    "PERatio": result.pe if result.pe is not None else None,
                    "FreeCashFlowTTM": result.freeCashFlowPerShareTTM if result.freeCashFlowPerShareTTM is not None else None,
                    "ProfitMarginsTTM": result.netProfitMarginTTM if result.netProfitMarginTTM is not None else None,
                    "DividendPayoutRatioTTM": result.payoutRatioTTM if result.payoutRatioTTM is not None else None,
                    "RevenueGrowthTTM": result.revenueGrowth if result.revenueGrowth is not None else None,
                    "Sector": result.sector if result.sector is not None else None
                } 
            for result in results]
        
        total = query.count()
        total_pages = (total + limit - 1) // limit

        return JSONResponse({
            "data": result,
            "total_pages": total_pages,
            "total_records": total,
            "current_pages": page
        },status_code = 200)
    
    else:

        total = query.count()
        total_pages = (total + limit - 1) // limit

        # query = query.filter(StockInfo.price <= StockInfo.yearLow)

        results = query.offset(skip).limit(limit).all()

        result =[{ 
                    "Symbol": result.Csymbol if result.Csymbol is not None else None,
                    "Name": result.Cname if result.Cname is not None else None,
                    "Price": f"{round(result.price,2)} USD" if result.price is not None else None,
                    "Change": f"{result.changesPercentage}%" if result.changesPercentage is not None else None,
                    "1DVolatility": f"{round(result.std,2)}%" if result.std is not None else None,
                    "Volume": format_large_number(result.volume) if result.volume is not None else None,
                    "MarketCap": format_large_number(result.marketCap) if result.marketCap is not None else None,
                    "DividendYieldTTM": result.dividendYielTTM if result.dividendYielTTM is not None else None,
                    "EPS": result.eps if result.eps is not None else None,
                    "Beta": result.beta if result.beta is not None else None,
                    "PERatio": result.pe if result.pe is not None else None,
                    "FreeCashFlowTTM": result.freeCashFlowPerShareTTM if result.freeCashFlowPerShareTTM is not None else None,
                    "ProfitMarginsTTM": result.netProfitMarginTTM if result.netProfitMarginTTM is not None else None,
                    "DividendPayoutRatioTTM": result.payoutRatioTTM if result.payoutRatioTTM is not None else None,
                    "RevenueGrowthTTM": result.revenueGrowth if result.revenueGrowth is not None else None,
                    "Sector": result.sector if result.sector is not None else None
                } 
                for result in results]

        return JSONResponse({
            "data": result,
            "total_pages": total_pages,
            "total_records": total,
            "current_pages": page
        },status_code = 200)

@StockIdeaRouter.get("/stock/lowperatio")
async def LowPERatio(
    Search: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    limit: int = Query(10, le=100)
    ):
    skip = (page - 1) * limit
    query = db.session.query(Symbols.Csymbol,Symbols.Cname,StockInfo.price,StockInfo.changesPercentage,StockInfo.volume,StockInfo.marketCap,
                            StockInfo.pe,StockInfo.eps,StockInfo.yearHigh,StockInfo.yearLow,CompanyProfile.beta,CompanyProfile.sector,StockInfo.priceAvg50,StockInfo.priceAvg200, 
                            StockPerformance.one_day,StockPerformance.one_month,StockPerformance.one_year,FinancialMetrics.freeCashFlowPerShareTTM,
                            FinancialMetrics.payoutRatioTTM,FinancialMetrics.debtEquityRatioTTM,FinancialMetrics.priceToBookRatioTTM,
                            FinancialMetrics.netProfitMarginTTM,FinancialGrowth.revenueGrowth).\
                            outerjoin(StockInfo,Symbols.Csymbol == StockInfo.symbol).\
                            outerjoin(StockPerformance, Symbols.Csymbol == StockPerformance.symbol).\
                            outerjoin(FinancialMetrics, Symbols.Csymbol == FinancialMetrics.symbol).\
                            outerjoin(FinancialGrowth, Symbols.Csymbol == FinancialGrowth.symbol).\
                            outerjoin(CompanyProfile, Symbols.Csymbol == CompanyProfile.symbol).order_by(StockInfo.price.desc())

    query = query.filter(StockInfo.pe < 15)

    if Search:
        query = query.filter(
            or_(
                Symbols.Csymbol.ilike(f"%{Search}%"),
                Symbols.Cname.ilike(f"%{Search}%"),
                CompanyProfile.sector.ilike(f"%{Search}%")  

            )
        )
        results = query.all()

        if not results:
            return JSONResponse({"message": "data not found"},status_code = 404)
            
        result =[{ 
                    "Symbol": result.Csymbol if result.Csymbol is not None else None,
                    "Name": result.Cname if result.Cname is not None else None,
                    "Price": f"{round(result.price,2)} USD" if result.price is not None else None,
                    "Change": f"{result.changesPercentage}%" if result.changesPercentage is not None else None,
                    "Volume": format_large_number(result.volume) if result.volume is not None else None,
                    "MarketCap": format_large_number(result.marketCap) if result.marketCap is not None else None,
                    "Beta": result.beta if result.beta is not None else None,
                    "PERatio": result.pe if result.pe is not None else None,
                    "FreeCashFlowTTM": result.freeCashFlowPerShareTTM if result.freeCashFlowPerShareTTM is not None else None,
                    "ProfitMarginsTTM": result.netProfitMarginTTM if result.netProfitMarginTTM is not None else None,
                    "DividendPayoutRatioTTM": result.payoutRatioTTM if result.payoutRatioTTM is not None else None,
                    "RevenueGrowthTTM": result.revenueGrowth if result.revenueGrowth is not None else None,
                    "DebtToEquityRatioTTM": result.debtEquityRatioTTM if result.debtEquityRatioTTM is not None else None,
                    "PriceToBookRatioTTM": result.priceToBookRatioTTM if result.priceToBookRatioTTM is not None else None,
                    "Sector": result.sector if result.sector is not None else None
              } 
              for result in results]
        
        total = query.count()
        total_pages = (total + limit - 1) // limit

        return JSONResponse({
            "data": result,
            "total_pages": total_pages,
            "total_records": total,
            "current_pages": page
        },status_code = 200)
    else:
        total = query.count()
        total_pages = (total + limit - 1) // limit
        # query = query.filter(StockInfo.price <= StockInfo.yearLow)

        results = query.offset(skip).limit(limit).all()

        result =[{ 
                    "Symbol": result.Csymbol if result.Csymbol is not None else None,
                    "Name": result.Cname if result.Cname is not None else None,
                    "Price": f"{round(result.price,2)} USD" if result.price is not None else None,
                    "Change": f"{result.changesPercentage}%" if result.changesPercentage is not None else None,
                    "Volume": format_large_number(result.volume) if result.volume is not None else None,
                    "MarketCap": format_large_number(result.marketCap) if result.marketCap is not None else None,
                    "Beta": result.beta if result.beta is not None else None,
                    "PERatio": result.pe if result.pe is not None else None,
                    "FreeCashFlowTTM": result.freeCashFlowPerShareTTM if result.freeCashFlowPerShareTTM is not None else None,
                    "ProfitMarginsTTM": result.netProfitMarginTTM if result.netProfitMarginTTM is not None else None,
                    "DividendPayoutRatioTTM": result.payoutRatioTTM if result.payoutRatioTTM is not None else None,
                    "RevenueGrowthTTM": result.revenueGrowth if result.revenueGrowth is not None else None,
                    "DebtToEquityRatioTTM": result.debtEquityRatioTTM if result.debtEquityRatioTTM is not None else None,
                    "PriceToBookRatioTTM": result.priceToBookRatioTTM if result.priceToBookRatioTTM is not None else None,
                    "Sector": result.sector if result.sector is not None else None
                } 
                for result in results]


        return JSONResponse({
            "data": result,
            "total_pages": total_pages,
            "total_records": total,
            "current_pages": page
        },status_code = 200)

@StockIdeaRouter.get("/stock/todaytopgain")
async def TodayTopGain(
    Search: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    limit: int = Query(10, le=100)
    ):
    skip = (page - 1) * limit
    query = db.session.query(Symbols.Csymbol,Symbols.Cname,StockInfo.price,StockInfo.changesPercentage,StockInfo.volume,StockInfo.marketCap,StockInfo.previousClose,
                            StockInfo.pe,StockInfo.eps,StockInfo.yearHigh,StockInfo.yearLow,CompanyProfile.beta,CompanyProfile.sector,StockInfo.priceAvg50,StockInfo.priceAvg200,StockInfo.dayHigh,StockInfo.dayLow,
                            StockPerformance.one_day,StockPerformance.one_month,StockPerformance.one_year,FinancialMetrics.freeCashFlowPerShareTTM,FinancialMetrics.payoutRatioTTM,
                            TechnicalIndicator.rsi, FinancialMetrics.netProfitMarginTTM,FinancialGrowth.revenueGrowth).\
                            outerjoin(StockInfo,Symbols.Csymbol == StockInfo.symbol).\
                            outerjoin(StockPerformance, Symbols.Csymbol == StockPerformance.symbol).\
                            outerjoin(FinancialMetrics, Symbols.Csymbol == FinancialMetrics.symbol).\
                            outerjoin(TechnicalIndicator, Symbols.Csymbol == TechnicalIndicator.symbol).\
                            outerjoin(FinancialGrowth, Symbols.Csymbol == FinancialGrowth.symbol).\
                            outerjoin(CompanyProfile, Symbols.Csymbol == CompanyProfile.symbol).order_by(StockInfo.price.desc())

    query = query.filter(
        StockInfo.previousClose != None,
        StockInfo.price != None,
        StockInfo.price >= 0,  # Filter by price range
        StockInfo.price <= 10000,  # Filter by price range
        ((StockInfo.price - StockInfo.previousClose) / StockInfo.previousClose * 100) >= 0,  # Filter by percentage change range
        ((StockInfo.price - StockInfo.previousClose) / StockInfo.previousClose * 100) <= 100 
    )
    if Search:
        query = query.filter(
            or_(
                Symbols.Csymbol.ilike(f"%{Search}%"),
                Symbols.Cname.ilike(f"%{Search}%"),
                CompanyProfile.sector.ilike(f"%{Search}%")  

            )
        )
        results = query.all()

        if not results:
            return JSONResponse({"message": "data not found"},status_code = 404)
        
        result =[{ 
                    "Symbol": result.Csymbol if result.Csymbol is not None else None,
                    "Name": result.Cname if result.Cname is not None else None,
                    "Price": f"{round(result.price,2)} USD" if result.price is not None else None,
                    "Change": f"{result.changesPercentage}%" if result.changesPercentage is not None else None,
                    "Volume": format_large_number(result.volume) if result.volume is not None else None,
                    "MarketCap": format_large_number(result.marketCap) if result.marketCap is not None else None,
                    "DayHigh": result.dayHigh if result.dayHigh is not None else None,
                    "DayLow": result.dayLow if result.dayLow is not None else None,
                    "52WeeksHigh": result.yearHigh if result.yearHigh is not None else None,
                    "52WeeksLow": result.yearLow if result.yearLow is not None else None,
                    "SMA50": result.priceAvg50 if result.priceAvg50 is not None else None,
                    "SMA200": result.priceAvg200 if result.priceAvg200 is not None else None,
                    "Beta": result.beta if result.beta is not None else None,
                    "PERatio": result.pe if result.pe is not None else None,
                    "RSI": result.rsi if result.rsi is not None else None,
                    "FreeCashFlowTTM": result.freeCashFlowPerShareTTM if result.freeCashFlowPerShareTTM is not None else None,
                    "ProfitMarginsTTM": result.netProfitMarginTTM if result.netProfitMarginTTM is not None else None,
                    "DividendPayoutRatioTTM": result.payoutRatioTTM if result.payoutRatioTTM is not None else None,
                    "RevenueGrowthTTM": result.revenueGrowth if result.revenueGrowth is not None else None,
                    "Sector": result.sector if result.sector is not None else None
            } 
            for result in results]
        
        total = query.count()
        total_pages = (total + limit - 1) // limit

        return JSONResponse({
            "data": result,
            "total_pages": total_pages,
            "total_records": total,
            "current_pages": page
        },status_code = 200)
    else: 
        total = query.count()
        total_pages = (total + limit - 1) // limit

        # query = query.filter(StockInfo.price <= StockInfo.yearLow)

        results = query.offset(skip).limit(limit).all()

        result =[{ 
                    "Symbol": result.Csymbol if result.Csymbol is not None else None,
                    "Name": result.Cname if result.Cname is not None else None,
                    "Price": f"{round(result.price,2)} USD" if result.price is not None else None,
                    "Change": f"{result.changesPercentage}%" if result.changesPercentage is not None else None,
                    "Volume": format_large_number(result.volume) if result.volume is not None else None,
                    "MarketCap": format_large_number(result.marketCap) if result.marketCap is not None else None,
                    "DayHigh": result.dayHigh if result.dayHigh is not None else None,
                    "DayLow": result.dayLow if result.dayLow is not None else None,
                    "52WeeksHigh": result.yearHigh if result.yearHigh is not None else None,
                    "52WeeksLow": result.yearLow if result.yearLow is not None else None,
                    "SMA50": result.priceAvg50 if result.priceAvg50 is not None else None,
                    "SMA200": result.priceAvg200 if result.priceAvg200 is not None else None,
                    "Beta": result.beta if result.beta is not None else None,
                    "PERatio": result.pe if result.pe is not None else None,
                    "RSI": result.rsi if result.rsi is not None else None,
                    "FreeCashFlowTTM": result.freeCashFlowPerShareTTM if result.freeCashFlowPerShareTTM is not None else None,
                    "ProfitMarginsTTM": result.netProfitMarginTTM if result.netProfitMarginTTM is not None else None,
                    "DividendPayoutRatioTTM": result.payoutRatioTTM if result.payoutRatioTTM is not None else None,
                    "RevenueGrowthTTM": result.revenueGrowth if result.revenueGrowth is not None else None,
                    "Sector": result.sector if result.sector is not None else None
                } 
                for result in results]

        return JSONResponse({
            "data": result,
            "total_pages": total_pages,
            "total_records": total,
            "current_pages": page
        },status_code = 200)

@StockIdeaRouter.get("/stock/todaytoploss")
async def TodayTopLoss(
    Search: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    limit: int = Query(10, le=100)
    ):
    skip = (page - 1) * limit
    query = db.session.query(Symbols.Csymbol,Symbols.Cname,StockInfo.price,StockInfo.changesPercentage,StockInfo.volume,StockInfo.marketCap,
                            StockInfo.pe,StockInfo.eps,StockInfo.yearHigh,StockInfo.yearLow,CompanyProfile.beta,CompanyProfile.sector,StockInfo.priceAvg50,StockInfo.priceAvg200,StockInfo.dayHigh,StockInfo.dayLow,
                            StockPerformance.one_day,StockPerformance.one_month,StockPerformance.one_year,FinancialMetrics.freeCashFlowPerShareTTM,FinancialMetrics.payoutRatioTTM,TechnicalIndicator.rsi,
                            FinancialMetrics.netProfitMarginTTM,FinancialGrowth.revenueGrowth).\
                            outerjoin(StockInfo,Symbols.Csymbol == StockInfo.symbol).\
                            outerjoin(StockPerformance, Symbols.Csymbol == StockPerformance.symbol).\
                            outerjoin(FinancialMetrics, Symbols.Csymbol == FinancialMetrics.symbol).\
                            outerjoin(TechnicalIndicator, Symbols.Csymbol == TechnicalIndicator.symbol).\
                            outerjoin(FinancialGrowth, Symbols.Csymbol == FinancialGrowth.symbol).\
                            outerjoin(CompanyProfile, Symbols.Csymbol == CompanyProfile.symbol).order_by(StockInfo.price.desc())

    query = query.filter(
        StockInfo.previousClose != None,
        StockInfo.price != None,
        StockInfo.price >= 0, 
        StockInfo.price <= 10000, 
        ((StockInfo.price - StockInfo.previousClose) / StockInfo.previousClose * 100) < 0, 
        ((StockInfo.price - StockInfo.previousClose) / StockInfo.previousClose * 100) >= -100  
    )

    if Search:
        query = query.filter(
            or_(
                Symbols.Csymbol.ilike(f"%{Search}%"),
                Symbols.Cname.ilike(f"%{Search}%"),
                CompanyProfile.sector.ilike(f"%{Search}%")  

            )
        )
        results = query.all()

        if not results:
            return JSONResponse({"message": "data not found"},status_code = 404)
        
        result =[{ 
                    
                    "Symbol": result.Csymbol if result.Csymbol is not None else None,
                    "Name": result.Cname if result.Cname is not None else None,
                    "Price": f"{round(result.price,2)} USD" if result.price is not None else None,
                    "Change": f"{result.changesPercentage}%" if result.changesPercentage is not None else None,
                    "Volume": format_large_number(result.volume) if result.volume is not None else None,
                    "MarketCap": format_large_number(result.marketCap) if result.marketCap is not None else None,
                    "DayHigh": result.dayHigh if result.dayHigh is not None else None,
                    "DayLow": result.dayLow if result.dayLow is not None else None,
                    "52WeeksHigh": result.yearHigh if result.yearHigh is not None else None,
                    "52WeeksLow": result.yearLow if result.yearLow is not None else None,
                    "SMA50": result.priceAvg50 if result.priceAvg50 is not None else None,
                    "SMA200": result.priceAvg200 if result.priceAvg200 is not None else None,
                    "Beta": result.beta if result.beta is not None else None,
                    "PERatio": result.pe if result.pe is not None else None,
                    "RSI": result.rsi if result.rsi is not None else None,
                    "FreeCashFlowTTM": result.freeCashFlowPerShareTTM if result.freeCashFlowPerShareTTM is not None else None,
                    "ProfitMarginsTTM": result.netProfitMarginTTM if result.netProfitMarginTTM is not None else None,
                    "DividendPayoutRatioTTM": result.payoutRatioTTM if result.payoutRatioTTM is not None else None,
                    "RevenueGrowthTTM": result.revenueGrowth if result.revenueGrowth is not None else None,
                    "Sector": result.sector if result.sector is not None else None
            } 
            for result in results]
        
        total = query.count()
        total_pages = (total + limit - 1) // limit

        return JSONResponse({
            "data": result,
            "total_pages": total_pages,
            "total_records": total,
            "current_pages": page
            },status_code = 200)
    else:
        total = query.count()
        total_pages = (total + limit - 1) // limit

        # query = query.filter(StockInfo.price <= StockInfo.yearLow)

        results = query.offset(skip).limit(limit).all()

        result =[{ 
                    "Symbol": result.Csymbol if result.Csymbol is not None else None,
                    "Name": result.Cname if result.Cname is not None else None,
                    "Price": f"{round(result.price,2)} USD" if result.price is not None else None,
                    "Change": f"{result.changesPercentage}%" if result.changesPercentage is not None else None,
                    "Volume": format_large_number(result.volume) if result.volume is not None else None,
                    "MarketCap": format_large_number(result.marketCap) if result.marketCap is not None else None,
                    "DayHigh": result.dayHigh if result.dayHigh is not None else None,
                    "DayLow": result.dayLow if result.dayLow is not None else None,
                    "52WeeksHigh": result.yearHigh if result.yearHigh is not None else None,
                    "52WeeksLow": result.yearLow if result.yearLow is not None else None,
                    "SMA50": result.priceAvg50 if result.priceAvg50 is not None else None,
                    "SMA200": result.priceAvg200 if result.priceAvg200 is not None else None,
                    "Beta": result.beta if result.beta is not None else None,
                    "PERatio": result.pe if result.pe is not None else None,
                    "RSI": result.rsi if result.rsi is not None else None,
                    "FreeCashFlowTTM": result.freeCashFlowPerShareTTM if result.freeCashFlowPerShareTTM is not None else None,
                    "ProfitMarginsTTM": result.netProfitMarginTTM if result.netProfitMarginTTM is not None else None,
                    "DividendPayoutRatioTTM": result.payoutRatioTTM if result.payoutRatioTTM is not None else None,
                    "RevenueGrowthTTM": result.revenueGrowth if result.revenueGrowth is not None else None,
                    "Sector": result.sector if result.sector is not None else None
                } 
                for result in results]

        return JSONResponse({
            "data": result,
            "total_pages": total_pages,
            "total_records": total,
            "current_pages": page
            },status_code = 200)

@StockIdeaRouter.get("/stock/topperformance")
async def TopPerformance(
    Search: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    limit: int = Query(10, le=100)
    ):
    skip = (page - 1) * limit
    query = db.session.query(Symbols.Csymbol,Symbols.Cname,StockInfo.price,StockInfo.changesPercentage,StockInfo.volume,StockInfo.marketCap,
                            StockInfo.pe,StockInfo.eps,StockInfo.yearHigh,StockInfo.yearLow,CompanyProfile.beta,CompanyProfile.sector,StockInfo.priceAvg50,StockInfo.priceAvg200,StockInfo.dayHigh,StockInfo.dayLow,
                            StockPerformance.one_day,StockPerformance.one_month,StockPerformance.one_year,FinancialMetrics.freeCashFlowPerShareTTM,FinancialMetrics.dividendYielTTM,TechnicalIndicator.rsi,
                            FinancialMetrics.netProfitMarginTTM,FinancialGrowth.revenueGrowth).\
                            outerjoin(StockInfo,Symbols.Csymbol == StockInfo.symbol).\
                            outerjoin(StockPerformance, Symbols.Csymbol == StockPerformance.symbol).\
                            outerjoin(FinancialMetrics, Symbols.Csymbol == FinancialMetrics.symbol).\
                            outerjoin(TechnicalIndicator, Symbols.Csymbol == TechnicalIndicator.symbol).\
                            outerjoin(FinancialGrowth, Symbols.Csymbol == FinancialGrowth.symbol).\
                            outerjoin(CompanyProfile, Symbols.Csymbol == CompanyProfile.symbol).order_by(StockInfo.price.desc())

    query = query.filter(
        StockInfo.previousClose != None,
        StockInfo.price != None,
        ((StockInfo.price - StockInfo.previousClose) / StockInfo.previousClose * 100) > 0,  
        ((StockInfo.price - StockInfo.previousClose) / StockInfo.previousClose * 100) <= 100  
    ).order_by(
        ((StockInfo.price - StockInfo.previousClose) / StockInfo.previousClose * 100).desc()
    )


    if Search:
        query = query.filter(
            or_(
                Symbols.Csymbol.ilike(f"%{Search}%"),
                Symbols.Cname.ilike(f"%{Search}%"),
                CompanyProfile.sector.ilike(f"%{Search}%")  

            )
        )
        results = query.all()
        if not results:
            return JSONResponse({"message": "data not found"},status_code = 404)
        
        result =[{ 
                    "Symbol": result.Csymbol if result.Csymbol is not None else None,
                    "Name": result.Cname if result.Cname is not None else None,
                    "Price": f"{round(result.price, 2)} USD" if result.price is not None else None,
                    "Change": f"{result.changesPercentage}%" if result.changesPercentage is not None else None,
                    "Volume": format_large_number(result.volume) if result.volume is not None else None,
                    "MarketCap": format_large_number(result.marketCap) if result.marketCap is not None else None,
                    "DayHigh": result.dayHigh if result.dayHigh is not None else None,
                    "DayLow": result.dayLow if result.dayLow is not None else None,
                    "1D": result.one_day if result.one_day is not None else None,
                    "1M": result.one_month if result.one_month is not None else None,
                    "1Y": result.one_year if result.one_year is not None else None,
                    "52WeeksHigh": result.yearHigh if result.yearHigh is not None else None,
                    "52WeeksLow": result.yearLow if result.yearLow is not None else None,
                    "SMA50": result.priceAvg50 if result.priceAvg50 is not None else None,
                    "SMA200": result.priceAvg200 if result.priceAvg200 is not None else None,
                    "Beta": result.beta if result.beta is not None else None,
                    "PERatio": result.pe if result.pe is not None else None,
                    "EPS": result.eps if result.eps is not None else None,
                    "RSI": result.rsi if result.rsi is not None else None,
                    "FreeCashFlowTTM": result.freeCashFlowPerShareTTM if result.freeCashFlowPerShareTTM is not None else None,
                    "ProfitMarginsTTM": result.netProfitMarginTTM if result.netProfitMarginTTM is not None else None,
                    "DividendYieldTTM": result.dividendYielTTM if result.dividendYielTTM is not None else None,
                    "RevenueGrowthTTM": result.revenueGrowth if result.revenueGrowth is not None else None,
                    "Sector": result.sector if result.sector is not None else None

              } 
              for result in results]
        
        total = query.count()
        total_pages = (total + limit - 1) // limit

        return JSONResponse({
            "data": result,
            "total_pages": total_pages,
            "total_records": total,
            "current_pages": page
            },status_code = 200)


    else:
        total = query.count()
        total_pages = (total + limit - 1) // limit
        # query = query.filter(StockInfo.price <= StockInfo.yearLow)

        results = query.offset(skip).limit(limit).all()

        result =[{ 
                    "Symbol": result.Csymbol if result.Csymbol is not None else None,
                    "Name": result.Cname if result.Cname is not None else None,
                    "Price": f"{round(result.price, 2)} USD" if result.price is not None else None,
                    "Change": f"{result.changesPercentage}%" if result.changesPercentage is not None else None,
                    "Volume": format_large_number(result.volume) if result.volume is not None else None,
                    "MarketCap": format_large_number(result.marketCap) if result.marketCap is not None else None,
                    "DayHigh": result.dayHigh if result.dayHigh is not None else None,
                    "DayLow": result.dayLow if result.dayLow is not None else None,
                    "1D": result.one_day if result.one_day is not None else None,
                    "1M": result.one_month if result.one_month is not None else None,
                    "1Y": result.one_year if result.one_year is not None else None,
                    "52WeeksHigh": result.yearHigh if result.yearHigh is not None else None,
                    "52WeeksLow": result.yearLow if result.yearLow is not None else None,
                    "SMA50": result.priceAvg50 if result.priceAvg50 is not None else None,
                    "SMA200": result.priceAvg200 if result.priceAvg200 is not None else None,
                    "Beta": result.beta if result.beta is not None else None,
                    "PERatio": result.pe if result.pe is not None else None,
                    "EPS": result.eps if result.eps is not None else None,
                    "RSI": result.rsi if result.rsi is not None else None,
                    "FreeCashFlowTTM": result.freeCashFlowPerShareTTM if result.freeCashFlowPerShareTTM is not None else None,
                    "ProfitMarginsTTM": result.netProfitMarginTTM if result.netProfitMarginTTM is not None else None,
                    "DividendYieldTTM": result.dividendYielTTM if result.dividendYielTTM is not None else None,
                    "RevenueGrowthTTM": result.revenueGrowth if result.revenueGrowth is not None else None,
                    "Sector": result.sector if result.sector is not None else None
                } 
                for result in results]
        
        return JSONResponse({
            "data": result,
            "total_pages": total_pages,
            "total_records": total,
            "current_pages": page
        },status_code = 200)

@StockIdeaRouter.get("/stock/highdividendyield")
async def HighDividendYield(
    Search: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    limit: int = Query(10, le=100)
    ):
    skip = (page - 1) * limit
    query = db.session.query(Symbols.Csymbol,Symbols.Cname,StockInfo.price,StockInfo.changesPercentage,StockInfo.volume,StockInfo.marketCap,
                            StockInfo.pe,StockInfo.eps,StockInfo.yearHigh,StockInfo.yearLow,CompanyProfile.beta,CompanyProfile.sector,StockInfo.priceAvg50,StockInfo.priceAvg200,StockInfo.dayHigh,StockInfo.dayLow,
                            StockPerformance.one_day,StockPerformance.one_month,StockPerformance.one_year,FinancialMetrics.payoutRatioTTM,FinancialMetrics.dividendYielTTM,FinancialMetrics.dividendPerShareTTM,
                            FinancialMetrics.freeCashFlowPerShareTTM,FinancialGrowth.revenueGrowth,FinancialGrowth.netIncomeGrowth).\
                            outerjoin(StockInfo,Symbols.Csymbol == StockInfo.symbol).\
                            outerjoin(StockPerformance, Symbols.Csymbol == StockPerformance.symbol).\
                            outerjoin(FinancialMetrics, Symbols.Csymbol == FinancialMetrics.symbol).\
                            outerjoin(FinancialGrowth, Symbols.Csymbol == FinancialGrowth.symbol).\
                            outerjoin(CompanyProfile, Symbols.Csymbol == CompanyProfile.symbol).order_by(StockInfo.price.desc())

    query = query.filter(
        FinancialMetrics.dividendYielTTM != None,  
        FinancialMetrics.dividendYielTTM > 0, 
    ).order_by(
        FinancialMetrics.dividendYielTTM.desc() 
    )
    if Search:
        query = query.filter(
            or_(
                Symbols.Csymbol.ilike(f"%{Search}%"),
                Symbols.Cname.ilike(f"%{Search}%"),
                CompanyProfile.sector.ilike(f"%{Search}%")  

            )
        )

        results = query.all()
        
        if not results:
            return JSONResponse({"message": "data not found"},status_code = 404)
        
        result =[{ 
                    "Symbol": result.Csymbol,
                    "Name": result.Cname,
                    "Price": f"{round(result.price, 2)} USD" if result.price is not None else None,
                    "Change": f"{result.changesPercentage}%" if result.changesPercentage is not None else None,
                    "Volume": format_large_number(result.volume) if result.volume is not None else None,
                    "MarketCap": format_large_number(result.marketCap) if result.marketCap is not None else None,
                    "52WeeksHigh": result.yearHigh if result.yearHigh is not None else None,
                    "52WeeksLow": result.yearLow if result.yearLow is not None else None,
                    "Beta": result.beta if result.beta is not None else None,
                    "PERatio": result.pe if result.pe is not None else None,
                    "EPS": result.eps if result.eps is not None else None,
                    "PayoutRatioTTM": result.payoutRatioTTM if result.payoutRatioTTM is not None else None,
                    "DividendYieldTTM": result.dividendYielTTM if result.dividendYielTTM is not None else None,
                    "DividendPerShareTTM": result.dividendPerShareTTM if result.dividendPerShareTTM is not None else None,
                    "RevenueGrowthTTM": result.revenueGrowth if result.revenueGrowth is not None else None,
                    "NetIncomeGrowth": result.netIncomeGrowth if result.netIncomeGrowth is not None else None,
                    "FreeCashFlowTTM": result.freeCashFlowPerShareTTM if result.freeCashFlowPerShareTTM is not None else None,
                    "Sector": result.sector if result.sector is not None else None
              } 
              for result in results]
        
        total = query.count()
        total_pages = (total + limit - 1) // limit

        return JSONResponse({
            "data": result,
            "total_pages": total_pages,
            "total_records": total,
            "current_pages": page
        },status_code = 200)
    
    else:
        total = query.count()
        total_pages = (total + limit - 1) // limit

        # query = query.filter(StockInfo.price <= StockInfo.yearLow)

        results = query.offset(skip).limit(limit).all()

        result =[{ 
                    "Symbol": result.Csymbol,
                    "Name": result.Cname,
                    "Price": f"{round(result.price, 2)} USD" if result.price is not None else None,
                    "Change": f"{result.changesPercentage}%" if result.changesPercentage is not None else None,
                    "Volume": format_large_number(result.volume) if result.volume is not None else None,
                    "MarketCap": format_large_number(result.marketCap) if result.marketCap is not None else None,
                    "52WeeksHigh": result.yearHigh if result.yearHigh is not None else None,
                    "52WeeksLow": result.yearLow if result.yearLow is not None else None,
                    "Beta": result.beta if result.beta is not None else None,
                    "PERatio": result.pe if result.pe is not None else None,
                    "EPS": result.eps if result.eps is not None else None,
                    "PayoutRatioTTM": result.payoutRatioTTM if result.payoutRatioTTM is not None else None,
                    "DividendYieldTTM": result.dividendYielTTM if result.dividendYielTTM is not None else None,
                    "DividendPerShareTTM": result.dividendPerShareTTM if result.dividendPerShareTTM is not None else None,
                    "RevenueGrowthTTM": result.revenueGrowth if result.revenueGrowth is not None else None,
                    "NetIncomeGrowth": result.netIncomeGrowth if result.netIncomeGrowth is not None else None,
                    "FreeCashFlowTTM": result.freeCashFlowPerShareTTM if result.freeCashFlowPerShareTTM is not None else None,
                    "Sector": result.sector if result.sector is not None else None
                } 
                for result in results]
        
        return JSONResponse({
            "data": result,
            "total_pages": total_pages,
            "total_records": total,
            "current_pages": page
        },status_code = 200)

@StockIdeaRouter.get("/stock/Search")
async def SearchSymbols(symbol: str):

    query = db.session.query(Symbols.Csymbol,Symbols.Cname).order_by(Symbols.Csymbol.asc())

    if symbol:
        query = query.filter(
            or_(

                Symbols.Csymbol.ilike(f"%{symbol}%"),
                Symbols.Cname.ilike(f"%{symbol}%"),
            )

        )

    results = query.all()
    if not results:
        return JSONResponse({"message": "Symbol Not Found!"},status_code=404)
    
    result =[{ 
                "Symbol": result.Csymbol,
                "Name": result.Cname,
                
              } 
              for result in results]
    return JSONResponse(result)

@StockIdeaRouter.get("/stock/graph")
async def GraphData(symbol: str,range_type: str):
    
    eastern = pytz.timezone('US/Eastern')
    today = datetime.now(eastern).date()  
    
    if range_type == "1d":
        today = today - timedelta(days=1)
        params ={
            "from": today,
            "to": today,
            "apikey": os.getenv("API_KEY")
        }
        URL = f"https://financialmodelingprep.com/api/v3/historical-chart/5min/{symbol}"
        with httpx.Client() as r:
            response = r.get(URL, params = params )
            query = db.session.query(Symbols.Csymbol,
                                    Symbols.Cname,
                                    StockInfo.price,
                                    StockInfo.changesPercentage,
                                    StockInfo.dayLow,
                                    StockInfo.dayHigh,
                                    StockInfo.yearHigh,
                                    StockInfo.yearLow,
                                    StockInfo.marketCap,
                                    StockInfo.priceAvg50,
                                    StockInfo.priceAvg200,
                                    StockInfo.exchange,
                                    StockInfo.volume,
                                    StockInfo.avgVolume,
                                    StockInfo.open_price,
                                    StockInfo.previousClose,
                                    StockInfo.eps,
                                    StockInfo.pe,
                                    StandardDeviation.std,
                                    CompanyProfile.sector,
                                    CompanyProfile.description,
                                    CompanyProfile.beta,
                                    StockPerformance.one_day,
                                    StockPerformance.five_day,
                                    StockPerformance.one_month,
                                    StockPerformance.three_month,
                                    StockPerformance.six_month,
                                    StockPerformance.ytd,
                                    StockPerformance.one_year,
                                    FinancialMetrics.dividendYielTTM,
                                    FinancialMetrics.payoutRatioTTM,
                                    FinancialMetrics.currentRatioTTM,
                                    FinancialMetrics.quickRatioTTM,
                                    FinancialMetrics.debtRatioTTM,
                                    FinancialMetrics.debtEquityRatioTTM,
                                    FinancialMetrics.freeCashFlowPerShareTTM,
                                    FinancialMetrics.priceToBookRatioTTM,
                                    FinancialMetrics.netProfitMarginTTM,
                                    FinancialMetrics.priceEarningsRatioTTM,
                                    FinancialGrowth.revenueGrowth,
                                    FinancialGrowth.netIncomeGrowth,
                                    FinancialGrowth.revenueGrowth,
                                    TechnicalIndicator.rsi                                    
                                    ).outerjoin(StockInfo, Symbols.Csymbol == StockInfo.symbol) \
                                    .outerjoin(CompanyProfile, Symbols.Csymbol == CompanyProfile.symbol) \
                                    .outerjoin(StockPerformance, Symbols.Csymbol == StockPerformance.symbol) \
                                    .outerjoin(FinancialMetrics, Symbols.Csymbol == FinancialMetrics.symbol) \
                                    .outerjoin(TechnicalIndicator, Symbols.Csymbol == TechnicalIndicator.symbol) \
                                    .outerjoin(StandardDeviation, Symbols.Csymbol == StandardDeviation.symbol)\
                                    .outerjoin(FinancialGrowth, Symbols.Csymbol == FinancialGrowth.symbol)\
                                    .filter(Symbols.Csymbol == symbol.upper()).order_by(Symbols.id.desc())

            result = [{
                        "Symbol": data.Csymbol if data.Csymbol is not None else None,
                        "Name": data.Cname if data.Cname is not None else None,
                        "Price": f"{round(data.price, 2)} USD" if data.price is not None else None,
                        "ChangePercentage": f"{data.changesPercentage}%" if data.changesPercentage is not None else None,
                        "DayLow": data.dayLow if data.dayLow is not None else None,
                        "DayHigh": data.dayHigh if data.dayHigh is not None else None,
                        "YearHigh": data.yearHigh if data.yearHigh is not None else None,
                        "YearLow": data.yearLow if data.yearLow is not None else None,
                        "MarketCap": format_large_number(data.marketCap) if data.marketCap is not None else None,
                        "SMA50": data.priceAvg50 if data.priceAvg50 is not None else None,
                        "SMA200": data.priceAvg200 if data.priceAvg200 is not None else None,
                        "Exchange": data.exchange if data.exchange is not None else None,
                        "Volume": format_large_number(data.volume) if data.volume is not None else None,
                        "AvgVolume": format_large_number(data.avgVolume) if data.avgVolume is not None else None,
                        "OpenPrice": data.open_price if data.open_price is not None else None,
                        "PreviousClose": data.previousClose if data.previousClose is not None else None,
                        "EPS": data.eps if data.eps is not None else None,
                        "PE": data.pe if data.pe is not None else None,
                        "OneDayVolatility": f"{round(data.std,2)}%" if data.std is not None else None,
                        "Sector": data.sector if data.sector is not None else None,
                        "Description": data.description if data.description is not None else None,
                        "Beta": data.beta if data.beta is not None else None,
                        "1D": data.one_day if data.one_day is not None else None,
                        "5D": data.five_day if data.five_day is not None else None,
                        "1M": data.one_month if data.one_month is not None else None,
                        "3M": data.three_month if data.three_month is not None else None,
                        "6M": data.six_month if data.six_month is not None else None,
                        "YTD": data.ytd if data.ytd is not None else None,
                        "1Y": data.one_year if data.one_year is not None else None,
                        "DividendYieldTTM": data.dividendYielTTM if data.dividendYielTTM is not None else None,
                        "PayoutRatioTTM": data.payoutRatioTTM if data.payoutRatioTTM is not None else None,
                        "CurrentRatioTTM": data.currentRatioTTM if data.currentRatioTTM is not None else None,
                        "QuickRatioTTM": data.quickRatioTTM if data.quickRatioTTM is not None else None,
                        "DebtRatioTTM": data.debtRatioTTM if data.debtRatioTTM is not None else None,
                        "DebtEquityRatioTTM": data.debtEquityRatioTTM if data.debtEquityRatioTTM is not None else None,
                        "FreeCashFlowPerShareTTM": data.freeCashFlowPerShareTTM if data.freeCashFlowPerShareTTM is not None else None,
                        "PriceToBookRatioTTM": data.priceToBookRatioTTM if data.priceToBookRatioTTM is not None else None,
                        "ProfitMarginsTTM": data.netProfitMarginTTM if data.netProfitMarginTTM is not None else None,
                        "EarningGrowthTTM": data.priceEarningsRatioTTM if data.priceEarningsRatioTTM is not None else None,
                        "NetIncomeGrowth": data.netIncomeGrowth if data.netIncomeGrowth is not None else None,
                        "revenueGrowth": data.revenueGrowth if data.revenueGrowth is not None else None,
                        "RSI": data.rsi if data.rsi is not None else None
                    } for data in query]
        return JSONResponse({"graph_data": response.json(),"full_data":result})
    
    elif range_type == "1w":
        one_weeks = today - timedelta(days=7)
        params ={
            "from": one_weeks,
            "to": today,
            "apikey": os.getenv("API_KEY")
        }
        URL = f"https://financialmodelingprep.com/api/v3/historical-price-full/{symbol}"
        with httpx.Client() as r:
            response = r.get(URL, params = params )
            query = db.session.query(Symbols.Csymbol,
                                    Symbols.Cname,
                                    StockInfo.price,
                                    StockInfo.changesPercentage,
                                    StockInfo.dayLow,
                                    StockInfo.dayHigh,
                                    StockInfo.yearHigh,
                                    StockInfo.yearLow,
                                    StockInfo.marketCap,
                                    StockInfo.priceAvg50,
                                    StockInfo.priceAvg200,
                                    StockInfo.exchange,
                                    StockInfo.volume,
                                    StockInfo.avgVolume,
                                    StockInfo.open_price,
                                    StockInfo.previousClose,
                                    StockInfo.eps,
                                    StockInfo.pe,
                                    StandardDeviation.std,
                                    CompanyProfile.sector,
                                    CompanyProfile.description,
                                    CompanyProfile.beta,
                                    StockPerformance.one_day,
                                    StockPerformance.five_day,
                                    StockPerformance.one_month,
                                    StockPerformance.three_month,
                                    StockPerformance.six_month,
                                    StockPerformance.ytd,
                                    StockPerformance.one_year,
                                    FinancialMetrics.dividendYielTTM,
                                    FinancialMetrics.payoutRatioTTM,
                                    FinancialMetrics.currentRatioTTM,
                                    FinancialMetrics.quickRatioTTM,
                                    FinancialMetrics.debtRatioTTM,
                                    FinancialMetrics.debtEquityRatioTTM,
                                    FinancialMetrics.freeCashFlowPerShareTTM,
                                    FinancialMetrics.priceToBookRatioTTM,
                                    FinancialMetrics.netProfitMarginTTM,
                                    FinancialMetrics.priceEarningsRatioTTM,
                                    FinancialGrowth.revenueGrowth,
                                    FinancialGrowth.netIncomeGrowth,
                                    FinancialGrowth.revenueGrowth,
                                    TechnicalIndicator.rsi                                    
                                    ).outerjoin(StockInfo, Symbols.Csymbol == StockInfo.symbol) \
                                    .outerjoin(CompanyProfile, Symbols.Csymbol == CompanyProfile.symbol) \
                                    .outerjoin(StockPerformance, Symbols.Csymbol == StockPerformance.symbol) \
                                    .outerjoin(FinancialMetrics, Symbols.Csymbol == FinancialMetrics.symbol) \
                                    .outerjoin(TechnicalIndicator, Symbols.Csymbol == TechnicalIndicator.symbol) \
                                    .outerjoin(FinancialGrowth, Symbols.Csymbol == FinancialGrowth.symbol)\
                                    .outerjoin(StandardDeviation, Symbols.Csymbol == StandardDeviation.symbol)\
                                    .filter(Symbols.Csymbol == symbol.upper()).order_by(Symbols.id.desc())

            result = [{
                        "Symbol": data.Csymbol if data.Csymbol is not None else None,
                        "Name": data.Cname if data.Cname is not None else None,
                        "Price": f"{round(data.price, 2)} USD" if data.price is not None else None,
                        "ChangePercentage": f"{data.changesPercentage}%" if data.changesPercentage is not None else None,
                        "DayLow": data.dayLow if data.dayLow is not None else None,
                        "DayHigh": data.dayHigh if data.dayHigh is not None else None,
                        "YearHigh": data.yearHigh if data.yearHigh is not None else None,
                        "YearLow": data.yearLow if data.yearLow is not None else None,
                        "MarketCap": format_large_number(data.marketCap) if data.marketCap is not None else None,
                        "SMA50": data.priceAvg50 if data.priceAvg50 is not None else None,
                        "SMA200": data.priceAvg200 if data.priceAvg200 is not None else None,
                        "Exchange": data.exchange if data.exchange is not None else None,
                        "Volume": format_large_number(data.volume) if data.volume is not None else None,
                        "AvgVolume": format_large_number(data.avgVolume) if data.avgVolume is not None else None,
                        "OpenPrice": data.open_price if data.open_price is not None else None,
                        "PreviousClose": data.previousClose if data.previousClose is not None else None,
                        "EPS": data.eps if data.eps is not None else None,
                        "PE": data.pe if data.pe is not None else None,
                        "OneDayVolatility": f"{round(data.std,2)}%" if data.std is not None else None,
                        "Sector": data.sector if data.sector is not None else None,
                        "Description": data.description if data.description is not None else None,
                        "Beta": data.beta if data.beta is not None else None,
                        "1D": data.one_day if data.one_day is not None else None,
                        "5D": data.five_day if data.five_day is not None else None,
                        "1M": data.one_month if data.one_month is not None else None,
                        "3M": data.three_month if data.three_month is not None else None,
                        "6M": data.six_month if data.six_month is not None else None,
                        "YTD": data.ytd if data.ytd is not None else None,
                        "1Y": data.one_year if data.one_year is not None else None,
                        "DividendYieldTTM": data.dividendYielTTM if data.dividendYielTTM is not None else None,
                        "PayoutRatioTTM": data.payoutRatioTTM if data.payoutRatioTTM is not None else None,
                        "CurrentRatioTTM": data.currentRatioTTM if data.currentRatioTTM is not None else None,
                        "QuickRatioTTM": data.quickRatioTTM if data.quickRatioTTM is not None else None,
                        "DebtRatioTTM": data.debtRatioTTM if data.debtRatioTTM is not None else None,
                        "DebtEquityRatioTTM": data.debtEquityRatioTTM if data.debtEquityRatioTTM is not None else None,
                        "FreeCashFlowPerShareTTM": data.freeCashFlowPerShareTTM if data.freeCashFlowPerShareTTM is not None else None,
                        "PriceToBookRatioTTM": data.priceToBookRatioTTM if data.priceToBookRatioTTM is not None else None,
                        "ProfitMarginsTTM": data.netProfitMarginTTM if data.netProfitMarginTTM is not None else None,
                        "EarningGrowthTTM": data.priceEarningsRatioTTM if data.priceEarningsRatioTTM is not None else None,
                        "NetIncomeGrowth": data.netIncomeGrowth if data.netIncomeGrowth is not None else None,
                        "revenueGrowth": data.revenueGrowth if data.revenueGrowth is not None else None,
                        "RSI": data.rsi if data.rsi is not None else None
                    } for data in query]
        return JSONResponse({"graph_data": response.json()['historical'],"full_data":result})
    
    elif range_type == "1m":
        one_month = today - timedelta(days=30)
        params ={
            "from": one_month,
            "to": today,
            "apikey": os.getenv("API_KEY")
        }
        URL = f"https://financialmodelingprep.com/api/v3/historical-price-full/{symbol}"
        with httpx.Client() as r:
            response = r.get(URL, params = params )
            query = db.session.query(Symbols.Csymbol,
                                    Symbols.Cname,
                                    StockInfo.price,
                                    StockInfo.changesPercentage,
                                    StockInfo.dayLow,
                                    StockInfo.dayHigh,
                                    StockInfo.yearHigh,
                                    StockInfo.yearLow,
                                    StockInfo.marketCap,
                                    StockInfo.priceAvg50,
                                    StockInfo.priceAvg200,
                                    StockInfo.exchange,
                                    StockInfo.volume,
                                    StockInfo.avgVolume,
                                    StockInfo.open_price,
                                    StockInfo.previousClose,
                                    StockInfo.eps,
                                    StockInfo.pe,
                                    StandardDeviation.std,
                                    CompanyProfile.sector,
                                    CompanyProfile.description,
                                    CompanyProfile.beta,
                                    StockPerformance.one_day,
                                    StockPerformance.five_day,
                                    StockPerformance.one_month,
                                    StockPerformance.three_month,
                                    StockPerformance.six_month,
                                    StockPerformance.ytd,
                                    StockPerformance.one_year,
                                    FinancialMetrics.dividendYielTTM,
                                    FinancialMetrics.payoutRatioTTM,
                                    FinancialMetrics.currentRatioTTM,
                                    FinancialMetrics.quickRatioTTM,
                                    FinancialMetrics.debtRatioTTM,
                                    FinancialMetrics.debtEquityRatioTTM,
                                    FinancialMetrics.freeCashFlowPerShareTTM,
                                    FinancialMetrics.priceToBookRatioTTM,
                                    FinancialMetrics.netProfitMarginTTM,
                                    FinancialMetrics.priceEarningsRatioTTM,
                                    FinancialGrowth.revenueGrowth,
                                    FinancialGrowth.netIncomeGrowth,
                                    FinancialGrowth.revenueGrowth,
                                    TechnicalIndicator.rsi                                    
                                    ).outerjoin(StockInfo, Symbols.Csymbol == StockInfo.symbol) \
                                    .outerjoin(CompanyProfile, Symbols.Csymbol == CompanyProfile.symbol) \
                                    .outerjoin(StockPerformance, Symbols.Csymbol == StockPerformance.symbol) \
                                    .outerjoin(FinancialMetrics, Symbols.Csymbol == FinancialMetrics.symbol) \
                                    .outerjoin(TechnicalIndicator, Symbols.Csymbol == TechnicalIndicator.symbol) \
                                    .outerjoin(FinancialGrowth, Symbols.Csymbol == FinancialGrowth.symbol)\
                                    .outerjoin(StandardDeviation, Symbols.Csymbol == StandardDeviation.symbol)\
                                    .filter(Symbols.Csymbol == symbol.upper()).order_by(Symbols.id.desc())

            result = [{
                        "Symbol": data.Csymbol if data.Csymbol is not None else None,
                        "Name": data.Cname if data.Cname is not None else None,
                        "Price": f"{round(data.price, 2)} USD" if data.price is not None else None,
                        "ChangePercentage": f"{data.changesPercentage}%" if data.changesPercentage is not None else None,
                        "DayLow": data.dayLow if data.dayLow is not None else None,
                        "DayHigh": data.dayHigh if data.dayHigh is not None else None,
                        "YearHigh": data.yearHigh if data.yearHigh is not None else None,
                        "YearLow": data.yearLow if data.yearLow is not None else None,
                        "MarketCap": format_large_number(data.marketCap) if data.marketCap is not None else None,
                        "SMA50": data.priceAvg50 if data.priceAvg50 is not None else None,
                        "SMA200": data.priceAvg200 if data.priceAvg200 is not None else None,
                        "Exchange": data.exchange if data.exchange is not None else None,
                        "Volume": format_large_number(data.volume) if data.volume is not None else None,
                        "AvgVolume": format_large_number(data.avgVolume) if data.avgVolume is not None else None,
                        "OpenPrice": data.open_price if data.open_price is not None else None,
                        "PreviousClose": data.previousClose if data.previousClose is not None else None,
                        "EPS": data.eps if data.eps is not None else None,
                        "PE": data.pe if data.pe is not None else None,
                        "OneDayVolatility": f"{round(data.std,2)}%" if data.std is not None else None,
                        "Sector": data.sector if data.sector is not None else None,
                        "Description": data.description if data.description is not None else None,
                        "Beta": data.beta if data.beta is not None else None,
                        "1D": data.one_day if data.one_day is not None else None,
                        "5D": data.five_day if data.five_day is not None else None,
                        "1M": data.one_month if data.one_month is not None else None,
                        "3M": data.three_month if data.three_month is not None else None,
                        "6M": data.six_month if data.six_month is not None else None,
                        "YTD": data.ytd if data.ytd is not None else None,
                        "1Y": data.one_year if data.one_year is not None else None,
                        "DividendYieldTTM": data.dividendYielTTM if data.dividendYielTTM is not None else None,
                        "PayoutRatioTTM": data.payoutRatioTTM if data.payoutRatioTTM is not None else None,
                        "CurrentRatioTTM": data.currentRatioTTM if data.currentRatioTTM is not None else None,
                        "QuickRatioTTM": data.quickRatioTTM if data.quickRatioTTM is not None else None,
                        "DebtRatioTTM": data.debtRatioTTM if data.debtRatioTTM is not None else None,
                        "DebtEquityRatioTTM": data.debtEquityRatioTTM if data.debtEquityRatioTTM is not None else None,
                        "FreeCashFlowPerShareTTM": data.freeCashFlowPerShareTTM if data.freeCashFlowPerShareTTM is not None else None,
                        "PriceToBookRatioTTM": data.priceToBookRatioTTM if data.priceToBookRatioTTM is not None else None,
                        "ProfitMarginsTTM": data.netProfitMarginTTM if data.netProfitMarginTTM is not None else None,
                        "EarningGrowthTTM": data.priceEarningsRatioTTM if data.priceEarningsRatioTTM is not None else None,
                        "NetIncomeGrowth": data.netIncomeGrowth if data.netIncomeGrowth is not None else None,
                        "revenueGrowth": data.revenueGrowth if data.revenueGrowth is not None else None,
                        "RSI": data.rsi if data.rsi is not None else None
                    } for data in query]
        return JSONResponse({"graph_data": response.json()['historical'],"full_data":result})
       
    elif range_type == "1y":
        one_year = today - timedelta(days=365)
        params ={
            "from": one_year,
            "to": today,
            "apikey": os.getenv("API_KEY")
        }
        URL = f"https://financialmodelingprep.com/api/v3/historical-price-full/{symbol}"
        with httpx.Client() as r:
            response = r.get(URL, params = params )

            df = pd.DataFrame(response.json()['historical'])

            df["date"] = pd.to_datetime(df["date"])

            # Extract year-month
            df["month"] = df["date"].dt.to_period("M")
            # Group by month
            monthly_data = df.groupby("month").agg(
                open=("open", "first"),         # First open price of the month
                high=("high", "max"),           # Maximum high price in the month
                low=("low", "min"),             # Minimum low price in the month
                close=("close", "last"),        # Last close price of the month
                volume=("volume", "sum"),       # Total volume of the month
                vwap=("vwap", "mean")           # Average VWAP
            ).reset_index()

           
            # Convert month back to string
            monthly_data["month"] = monthly_data["month"].astype(str)

            # Convert DataFrame to list of dictionaries

            query = db.session.query(Symbols.Csymbol,
                                    Symbols.Cname,
                                    StockInfo.price,
                                    StockInfo.changesPercentage,
                                    StockInfo.dayLow,
                                    StockInfo.dayHigh,
                                    StockInfo.yearHigh,
                                    StockInfo.yearLow,
                                    StockInfo.marketCap,
                                    StockInfo.priceAvg50,
                                    StockInfo.priceAvg200,
                                    StockInfo.exchange,
                                    StockInfo.volume,
                                    StockInfo.avgVolume,
                                    StockInfo.open_price,
                                    StockInfo.previousClose,
                                    StockInfo.eps,
                                    StockInfo.pe,
                                    StandardDeviation.std,
                                    CompanyProfile.sector,
                                    CompanyProfile.description,
                                    CompanyProfile.beta,
                                    StockPerformance.one_day,
                                    StockPerformance.five_day,
                                    StockPerformance.one_month,
                                    StockPerformance.three_month,
                                    StockPerformance.six_month,
                                    StockPerformance.ytd,
                                    StockPerformance.one_year,
                                    FinancialMetrics.dividendYielTTM,
                                    FinancialMetrics.payoutRatioTTM,
                                    FinancialMetrics.currentRatioTTM,
                                    FinancialMetrics.quickRatioTTM,
                                    FinancialMetrics.debtRatioTTM,
                                    FinancialMetrics.debtEquityRatioTTM,
                                    FinancialMetrics.freeCashFlowPerShareTTM,
                                    FinancialMetrics.priceToBookRatioTTM,
                                    FinancialMetrics.netProfitMarginTTM,
                                    FinancialMetrics.priceEarningsRatioTTM,
                                    FinancialGrowth.revenueGrowth,
                                    FinancialGrowth.netIncomeGrowth,
                                    FinancialGrowth.revenueGrowth,
                                    TechnicalIndicator.rsi                                    
                                    ).outerjoin(StockInfo, Symbols.Csymbol == StockInfo.symbol) \
                                    .outerjoin(CompanyProfile, Symbols.Csymbol == CompanyProfile.symbol) \
                                    .outerjoin(StockPerformance, Symbols.Csymbol == StockPerformance.symbol) \
                                    .outerjoin(FinancialMetrics, Symbols.Csymbol == FinancialMetrics.symbol) \
                                    .outerjoin(TechnicalIndicator, Symbols.Csymbol == TechnicalIndicator.symbol) \
                                    .outerjoin(FinancialGrowth, Symbols.Csymbol == FinancialGrowth.symbol)\
                                    .outerjoin(StandardDeviation, Symbols.Csymbol == StandardDeviation.symbol)\
                                    .filter(Symbols.Csymbol == symbol.upper()).order_by(Symbols.id.desc())

            result = [{
                        "Symbol": data.Csymbol if data.Csymbol is not None else None,
                        "Name": data.Cname if data.Cname is not None else None,
                        "Price": f"{round(data.price, 2)} USD" if data.price is not None else None,
                        "ChangePercentage": f"{data.changesPercentage}%" if data.changesPercentage is not None else None,
                        "DayLow": data.dayLow if data.dayLow is not None else None,
                        "DayHigh": data.dayHigh if data.dayHigh is not None else None,
                        "YearHigh": data.yearHigh if data.yearHigh is not None else None,
                        "YearLow": data.yearLow if data.yearLow is not None else None,
                        "MarketCap": format_large_number(data.marketCap) if data.marketCap is not None else None,
                        "SMA50": data.priceAvg50 if data.priceAvg50 is not None else None,
                        "SMA200": data.priceAvg200 if data.priceAvg200 is not None else None,
                        "Exchange": data.exchange if data.exchange is not None else None,
                        "Volume": format_large_number(data.volume) if data.volume is not None else None,
                        "AvgVolume": format_large_number(data.avgVolume) if data.avgVolume is not None else None,
                        "OpenPrice": data.open_price if data.open_price is not None else None,
                        "PreviousClose": data.previousClose if data.previousClose is not None else None,
                        "EPS": data.eps if data.eps is not None else None,
                        "PE": data.pe if data.pe is not None else None,
                        "OneDayVolatility": f"{round(data.std,2)}%" if data.std is not None else None,
                        "Sector": data.sector if data.sector is not None else None,
                        "Description": data.description if data.description is not None else None,
                        "Beta": data.beta if data.beta is not None else None,
                        "1D": data.one_day if data.one_day is not None else None,
                        "5D": data.five_day if data.five_day is not None else None,
                        "1M": data.one_month if data.one_month is not None else None,
                        "3M": data.three_month if data.three_month is not None else None,
                        "6M": data.six_month if data.six_month is not None else None,
                        "YTD": data.ytd if data.ytd is not None else None,
                        "1Y": data.one_year if data.one_year is not None else None,
                        "DividendYieldTTM": data.dividendYielTTM if data.dividendYielTTM is not None else None,
                        "PayoutRatioTTM": data.payoutRatioTTM if data.payoutRatioTTM is not None else None,
                        "CurrentRatioTTM": data.currentRatioTTM if data.currentRatioTTM is not None else None,
                        "QuickRatioTTM": data.quickRatioTTM if data.quickRatioTTM is not None else None,
                        "DebtRatioTTM": data.debtRatioTTM if data.debtRatioTTM is not None else None,
                        "DebtEquityRatioTTM": data.debtEquityRatioTTM if data.debtEquityRatioTTM is not None else None,
                        "FreeCashFlowPerShareTTM": data.freeCashFlowPerShareTTM if data.freeCashFlowPerShareTTM is not None else None,
                        "PriceToBookRatioTTM": data.priceToBookRatioTTM if data.priceToBookRatioTTM is not None else None,
                        "ProfitMarginsTTM": data.netProfitMarginTTM if data.netProfitMarginTTM is not None else None,
                        "EarningGrowthTTM": data.priceEarningsRatioTTM if data.priceEarningsRatioTTM is not None else None,
                        "NetIncomeGrowth": data.netIncomeGrowth if data.netIncomeGrowth is not None else None,
                        "revenueGrowth": data.revenueGrowth if data.revenueGrowth is not None else None,
                        "RSI": data.rsi if data.rsi is not None else None
                    } for data in query]
        return JSONResponse({"graph_data": monthly_data.to_dict(orient="records"),"full_data":result})
    
    elif range_type == "max":
        params ={
            "apikey": os.getenv("API_KEY")
        }
        URL = f"https://financialmodelingprep.com/api/v3/historical-price-full/{symbol}"
        with httpx.Client() as r:
            response = r.get(URL, params = params )

            df = pd.DataFrame(response.json()['historical'])

            df["date"] = pd.to_datetime(df["date"])

            # Extract year-month
            df["month"] = df["date"].dt.to_period("M")
            # Group by month
            monthly_data = df.groupby("month").agg(
                open=("open", "first"),         # First open price of the month
                high=("high", "max"),           # Maximum high price in the month
                low=("low", "min"),             # Minimum low price in the month
                close=("close", "last"),        # Last close price of the month
                volume=("volume", "sum"),       # Total volume of the month
                vwap=("vwap", "mean")           # Average VWAP
            ).reset_index()

           
            # Convert month back to string
            monthly_data["month"] = monthly_data["month"].astype(str)

            query = db.session.query(Symbols.Csymbol,
                                    Symbols.Cname,
                                    StockInfo.price,
                                    StockInfo.changesPercentage,
                                    StockInfo.dayLow,
                                    StockInfo.dayHigh,
                                    StockInfo.yearHigh,
                                    StockInfo.yearLow,
                                    StockInfo.marketCap,
                                    StockInfo.priceAvg50,
                                    StockInfo.priceAvg200,
                                    StockInfo.exchange,
                                    StockInfo.volume,
                                    StockInfo.avgVolume,
                                    StockInfo.open_price,
                                    StockInfo.previousClose,
                                    StockInfo.eps,
                                    StockInfo.pe,
                                    StandardDeviation.std,
                                    CompanyProfile.sector,
                                    CompanyProfile.description,
                                    CompanyProfile.beta,
                                    StockPerformance.one_day,
                                    StockPerformance.five_day,
                                    StockPerformance.one_month,
                                    StockPerformance.three_month,
                                    StockPerformance.six_month,
                                    StockPerformance.ytd,
                                    StockPerformance.one_year,
                                    FinancialMetrics.dividendYielTTM,
                                    FinancialMetrics.payoutRatioTTM,
                                    FinancialMetrics.currentRatioTTM,
                                    FinancialMetrics.quickRatioTTM,
                                    FinancialMetrics.debtRatioTTM,
                                    FinancialMetrics.debtEquityRatioTTM,
                                    FinancialMetrics.freeCashFlowPerShareTTM,
                                    FinancialMetrics.priceToBookRatioTTM,
                                    FinancialMetrics.netProfitMarginTTM,
                                    FinancialMetrics.priceEarningsRatioTTM,
                                    FinancialGrowth.revenueGrowth,
                                    FinancialGrowth.netIncomeGrowth,
                                    FinancialGrowth.revenueGrowth,
                                    TechnicalIndicator.rsi                                    
                                    ).outerjoin(StockInfo, Symbols.Csymbol == StockInfo.symbol) \
                                    .outerjoin(CompanyProfile, Symbols.Csymbol == CompanyProfile.symbol) \
                                    .outerjoin(StockPerformance, Symbols.Csymbol == StockPerformance.symbol) \
                                    .outerjoin(FinancialMetrics, Symbols.Csymbol == FinancialMetrics.symbol) \
                                    .outerjoin(TechnicalIndicator, Symbols.Csymbol == TechnicalIndicator.symbol) \
                                    .outerjoin(FinancialGrowth, Symbols.Csymbol == FinancialGrowth.symbol)\
                                    .outerjoin(StandardDeviation, Symbols.Csymbol == StandardDeviation.symbol)\
                                    .filter(Symbols.Csymbol == symbol.upper()).order_by(Symbols.id.desc())

            result = [{
                         "Symbol": data.Csymbol if data.Csymbol is not None else None,
                        "Name": data.Cname if data.Cname is not None else None,
                        "Price": f"{round(data.price, 2)} USD" if data.price is not None else None,
                        "ChangePercentage": f"{data.changesPercentage}%" if data.changesPercentage is not None else None,
                        "DayLow": data.dayLow if data.dayLow is not None else None,
                        "DayHigh": data.dayHigh if data.dayHigh is not None else None,
                        "YearHigh": data.yearHigh if data.yearHigh is not None else None,
                        "YearLow": data.yearLow if data.yearLow is not None else None,
                        "MarketCap": format_large_number(data.marketCap) if data.marketCap is not None else None,
                        "SMA50": data.priceAvg50 if data.priceAvg50 is not None else None,
                        "SMA200": data.priceAvg200 if data.priceAvg200 is not None else None,
                        "Exchange": data.exchange if data.exchange is not None else None,
                        "Volume": format_large_number(data.volume) if data.volume is not None else None,
                        "AvgVolume": format_large_number(data.avgVolume) if data.avgVolume is not None else None,
                        "OpenPrice": data.open_price if data.open_price is not None else None,
                        "PreviousClose": data.previousClose if data.previousClose is not None else None,
                        "EPS": data.eps if data.eps is not None else None,
                        "PE": data.pe if data.pe is not None else None,
                        "OneDayVolatility": f"{round(data.std)}" if data.std is not None else None,
                        "Sector": data.sector if data.sector is not None else None,
                        "Description": data.description if data.description is not None else None,
                        "Beta": data.beta if data.beta is not None else None,
                        "1D": data.one_day if data.one_day is not None else None,
                        "5D": data.five_day if data.five_day is not None else None,
                        "1M": data.one_month if data.one_month is not None else None,
                        "3M": data.three_month if data.three_month is not None else None,
                        "6M": data.six_month if data.six_month is not None else None,
                        "YTD": data.ytd if data.ytd is not None else None,
                        "1Y": data.one_year if data.one_year is not None else None,
                        "DividendYieldTTM": data.dividendYielTTM if data.dividendYielTTM is not None else None,
                        "PayoutRatioTTM": data.payoutRatioTTM if data.payoutRatioTTM is not None else None,
                        "CurrentRatioTTM": data.currentRatioTTM if data.currentRatioTTM is not None else None,
                        "QuickRatioTTM": data.quickRatioTTM if data.quickRatioTTM is not None else None,
                        "DebtRatioTTM": data.debtRatioTTM if data.debtRatioTTM is not None else None,
                        "DebtEquityRatioTTM": data.debtEquityRatioTTM if data.debtEquityRatioTTM is not None else None,
                        "FreeCashFlowPerShareTTM": data.freeCashFlowPerShareTTM if data.freeCashFlowPerShareTTM is not None else None,
                        "PriceToBookRatioTTM": data.priceToBookRatioTTM if data.priceToBookRatioTTM is not None else None,
                        "ProfitMarginsTTM": data.netProfitMarginTTM if data.netProfitMarginTTM is not None else None,
                        "EarningGrowthTTM": data.priceEarningsRatioTTM if data.priceEarningsRatioTTM is not None else None,
                        "NetIncomeGrowth": data.netIncomeGrowth if data.netIncomeGrowth is not None else None,
                        "revenueGrowth": data.revenueGrowth if data.revenueGrowth is not None else None,
                        "RSI": data.rsi if data.rsi is not None else None
                    } for data in query]
        return JSONResponse({"graph_data": monthly_data.to_dict(orient="records"),"full_data":result})


@StockIdeaRouter.get("/gemini/chatbot")
def ChatBot(symbol : str):
    query = db.session.query(Symbols.Csymbol,
                                    Symbols.Cname,
                                    StockInfo.price,
                                    StockInfo.changesPercentage,
                                    StockInfo.dayLow,
                                    StockInfo.dayHigh,
                                    StockInfo.yearHigh,
                                    StockInfo.yearLow,
                                    StockInfo.marketCap,
                                    StockInfo.priceAvg50,
                                    StockInfo.priceAvg200,
                                    StockInfo.exchange,
                                    StockInfo.volume,
                                    StockInfo.avgVolume,
                                    StockInfo.open_price,
                                    StockInfo.previousClose,
                                    StockInfo.eps,
                                    StockInfo.pe,
                                    StandardDeviation.std,
                                    CompanyProfile.sector,
                                    CompanyProfile.beta,
                                    StockPerformance.one_day,
                                    StockPerformance.five_day,
                                    StockPerformance.one_month,
                                    StockPerformance.three_month,
                                    StockPerformance.six_month,
                                    StockPerformance.ytd,
                                    StockPerformance.one_year,
                                    FinancialMetrics.dividendYielTTM,
                                    FinancialMetrics.payoutRatioTTM,
                                    FinancialMetrics.currentRatioTTM,
                                    FinancialMetrics.quickRatioTTM,
                                    FinancialMetrics.debtRatioTTM,
                                    FinancialMetrics.debtEquityRatioTTM,
                                    FinancialMetrics.freeCashFlowPerShareTTM,
                                    FinancialMetrics.priceToBookRatioTTM,
                                    FinancialMetrics.netProfitMarginTTM,
                                    FinancialMetrics.priceEarningsRatioTTM,
                                    FinancialGrowth.revenueGrowth,
                                    FinancialGrowth.netIncomeGrowth,
                                    FinancialGrowth.revenueGrowth,
                                    TechnicalIndicator.rsi                                    
                                    ).outerjoin(StockInfo, Symbols.Csymbol == StockInfo.symbol) \
                                    .outerjoin(CompanyProfile, Symbols.Csymbol == CompanyProfile.symbol) \
                                    .outerjoin(StockPerformance, Symbols.Csymbol == StockPerformance.symbol) \
                                    .outerjoin(FinancialMetrics, Symbols.Csymbol == FinancialMetrics.symbol) \
                                    .outerjoin(TechnicalIndicator, Symbols.Csymbol == TechnicalIndicator.symbol) \
                                    .outerjoin(FinancialGrowth, Symbols.Csymbol == FinancialGrowth.symbol)\
                                    .outerjoin(StandardDeviation, Symbols.Csymbol == StandardDeviation.symbol)\
                                    .filter(Symbols.Csymbol == symbol)

    result = [{
                "Symbol": data.Csymbol if data.Csymbol is not None else None,
                "Name": data.Cname if data.Cname is not None else None,
                "Price": f"{round(data.price, 2)} USD" if data.price is not None else None,
                "ChangePercentage": f"{data.changesPercentage}%" if data.changesPercentage is not None else None,
                "DayLow": data.dayLow if data.dayLow is not None else None,
                "DayHigh": data.dayHigh if data.dayHigh is not None else None,
                "YearHigh": data.yearHigh if data.yearHigh is not None else None,
                "YearLow": data.yearLow if data.yearLow is not None else None,
                "MarketCap": format_large_number(data.marketCap) if data.marketCap is not None else None,
                "SMA50": data.priceAvg50 if data.priceAvg50 is not None else None,
                "SMA200": data.priceAvg200 if data.priceAvg200 is not None else None,
                "Exchange": data.exchange if data.exchange is not None else None,
                "Volume": format_large_number(data.volume) if data.volume is not None else None,
                "AvgVolume": format_large_number(data.avgVolume) if data.avgVolume is not None else None,
                "OpenPrice": data.open_price if data.open_price is not None else None,
                "PreviousClose": data.previousClose if data.previousClose is not None else None,
                "EPS": data.eps if data.eps is not None else None,
                "PE": data.pe if data.pe is not None else None,
                "OneDayVolatility": f"{round(data.std,2)}%" if data.std is not None else None,
                "Sector": data.sector if data.sector is not None else None,
                "Beta": data.beta if data.beta is not None else None,
                "1D": data.one_day if data.one_day is not None else None,
                "5D": data.five_day if data.five_day is not None else None,
                "1M": data.one_month if data.one_month is not None else None,
                "3M": data.three_month if data.three_month is not None else None,
                "6M": data.six_month if data.six_month is not None else None,
                "YTD": data.ytd if data.ytd is not None else None,
                "1Y": data.one_year if data.one_year is not None else None,
                "DividendYieldTTM": data.dividendYielTTM if data.dividendYielTTM is not None else None,
                "PayoutRatioTTM": data.payoutRatioTTM if data.payoutRatioTTM is not None else None,
                "CurrentRatioTTM": data.currentRatioTTM if data.currentRatioTTM is not None else None,
                "QuickRatioTTM": data.quickRatioTTM if data.quickRatioTTM is not None else None,
                "DebtRatioTTM": data.debtRatioTTM if data.debtRatioTTM is not None else None,
                "DebtEquityRatioTTM": data.debtEquityRatioTTM if data.debtEquityRatioTTM is not None else None,
                "FreeCashFlowPerShareTTM": data.freeCashFlowPerShareTTM if data.freeCashFlowPerShareTTM is not None else None,
                "PriceToBookRatioTTM": data.priceToBookRatioTTM if data.priceToBookRatioTTM is not None else None,
                "ProfitMarginsTTM": data.netProfitMarginTTM if data.netProfitMarginTTM is not None else None,
                "EarningGrowthTTM": data.priceEarningsRatioTTM if data.priceEarningsRatioTTM is not None else None,
                "NetIncomeGrowth": data.netIncomeGrowth if data.netIncomeGrowth is not None else None,
                "revenueGrowth": data.revenueGrowth if data.revenueGrowth is not None else None,
                "RSI": data.rsi if data.rsi is not None else None
            } for data in query]
    return result