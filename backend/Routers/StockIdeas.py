from fastapi import APIRouter,HTTPException,Query
from Models.StocksModels import Symbols, StockInfo, StockPerformance, CompanyProfile, FinancialMetrics, TechnicalIndicator, FinancialGrowth
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

    query = db.session.query(CompanyProfile.image,Symbols.Csymbol,Symbols.Cname,StockInfo.onedayvolatility,StockInfo.price,StockInfo.changesPercentage,StockInfo.volume,StockInfo.marketCap,
                            CompanyProfile.beta,CompanyProfile.sector,StockInfo.priceAvg50,StockInfo.priceAvg200, TechnicalIndicator.rsi,
                            StockPerformance.one_day,StockPerformance.one_month,StockPerformance.one_year, FinancialMetrics.dividendYielTTM).\
                            outerjoin(StockInfo,Symbols.Csymbol == StockInfo.symbol).\
                            outerjoin(StockPerformance, Symbols.Csymbol == StockPerformance.symbol).\
                            outerjoin(FinancialMetrics, Symbols.Csymbol == FinancialMetrics.symbol).\
                            outerjoin(TechnicalIndicator, Symbols.Csymbol == TechnicalIndicator.symbol).\
                            outerjoin(CompanyProfile, Symbols.Csymbol == CompanyProfile.symbol).order_by(StockInfo.price.desc())


    # query = query.filter(StockInfo.price > 500.00)


    if Search:
        query = query.filter(
            or_(
                Symbols.Csymbol.ilike(f"%{Search}%"),
                Symbols.Cname.ilike(f"%{Search}%"),
                
                CompanyProfile.sector.ilike(f"%{Search}%")  

            )
        )

        results = query.all()
        result =[{ 
                "Symbol": result.Csymbol,
                "Name": result.Cname,
                "Price": f"{round(result.price,2)} USD",
                "Change": f"{result.changesPercentage}%",
                "1DVolatility": result.onedayvolatility,
                "1D": result.one_day,
                "1M": result.one_month,
                "1Y": result.one_year,
                "Volume": format_large_number(result.volume),
                "MarketCap": format_large_number(result.marketCap),
                "SMA50": result.priceAvg50,
                "SMA200": result.priceAvg200,
                "Beta":result.beta,
                "DividendYieldTTM": RoundTheValue(result.dividendYielTTM), 
                "RSI": result.rsi,
                "Sector": result.sector
            } 
            for result in results]
        
        total = query.count()
        total_pages = (total + limit - 1) // limit

        return JSONResponse({
            "data": result,
            "total_pages": total_pages,
            "total_records": total,
            "current_pages": page
            })
    
    else:

        total = query.count()
        total_pages = (total + limit - 1) // limit

        results = query.offset(skip).limit(limit).all()

        result =[{ 
                    "Symbol": result.Csymbol,
                    "Name": result.Cname,
                    "Price": f"{round(result.price,2)} USD",
                    "Change": f"{result.changesPercentage}%",
                    "1DVolatility": result.onedayvolatility,
                    "1D": result.one_day,
                    "1M": result.one_month,
                    "1Y": result.one_year,
                    "Volume": format_large_number(result.volume),
                    "MarketCap": format_large_number(result.marketCap),
                    "SMA50": result.priceAvg50,
                    "SMA200": result.priceAvg200,
                    "Beta":result.beta,
                    "DividendYieldTTM": RoundTheValue(result.dividendYielTTM), 
                    "RSI": result.rsi,
                    "Sector": result.sector
                } 
                for result in results]
        
        return JSONResponse({
            "data": result,
            "total_pages": total_pages,
            "total_records": total,
            "current_pages": page
        })
    


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
                            outerjoin(CompanyProfile, Symbols.Csymbol == CompanyProfile.symbol)


    if Search:
        query = query.filter(
            or_(
                Symbols.Csymbol.ilike(f"%{Search}%"),
                Symbols.Cname.ilike(f"%{Search}%"),
                CompanyProfile.sector.ilike(f"%{Search}%")  

            )
        )

        results = query.all()
        result =[{ 
            "Symbol": result.Csymbol,
            "Name": result.Cname,
            "Price": f"{round(result.price,2)} USD",
            "Change": f"{result.changesPercentage}%",
            "1D": result.one_day,
            "1M": result.one_month,
            "1Y": result.one_year,
            "Volume": format_large_number(result.volume),
            "MarketCap": format_large_number(result.marketCap),
            "52WeeksHigh": result.yearHigh,
            "52WeeksLow": result.yearLow,
            "SMA50": result.priceAvg50,
            "SMA200": result.priceAvg200,
            "Beta":result.beta,
            "RSI": result.rsi,
            "DividendYieldTTM": RoundTheValue(result.dividendYielTTM), 
            "Sector": result.sector
            } 
            for result in results]
        
        total = query.count()
        total_pages = (total + limit - 1) // limit

        return JSONResponse({
            "data": result,
            "total_pages": total_pages,
            "total_records": total,
            "current_pages": page
            })
    else:
        
        total = query.count()
        total_pages = (total + limit - 1) // limit
        results = query.offset(skip).limit(limit).all()

        result =[{ 
                    "Symbol": result.Csymbol,
                    "Name": result.Cname,
                    "Price": f"{round(result.price,2)} USD",
                    "Change": f"{result.changesPercentage}%",
                    "1D": result.one_day,
                    "1M": result.one_month,
                    "1Y": result.one_year,
                    "Volume": format_large_number(result.volume),
                    "MarketCap": format_large_number(result.marketCap),
                    "52WeeksHigh": result.yearHigh,
                    "52WeeksLow": result.yearLow,
                    "SMA50": result.priceAvg50,
                    "SMA200": result.priceAvg200,
                    "Beta":result.beta,
                    "RSI": result.rsi,
                    "DividendYieldTTM": RoundTheValue(result.dividendYielTTM), 
                    "Sector": result.sector
                } 
                for result in results]
        return JSONResponse({
            "data": result,
            "total_pages": total_pages,
            "total_records": total,
            "current_page": page
        })

@StockIdeaRouter.get("/stock/52weekslow")
async def YearLow(
    Search: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    limit: int = Query(10, le=100)
    ):
    skip = (page - 1) * limit
    query = db.session.query(CompanyProfile.image,Symbols.Csymbol,Symbols.Cname,StockInfo.price,StockInfo.changesPercentage,StockInfo.volume,StockInfo.marketCap,
                            StockInfo.yearHigh,StockInfo.yearLow,CompanyProfile.beta,CompanyProfile.sector,StockInfo.priceAvg50,StockInfo.priceAvg200, 
                            StockPerformance.one_day,StockPerformance.one_month,StockPerformance.one_year,FinancialMetrics.dividendYielTTM,TechnicalIndicator.rsi).\
                            outerjoin(StockInfo,Symbols.Csymbol == StockInfo.symbol).\
                            outerjoin(StockPerformance, Symbols.Csymbol == StockPerformance.symbol).\
                            outerjoin(FinancialMetrics, Symbols.Csymbol == FinancialMetrics.symbol).\
                            outerjoin(TechnicalIndicator, Symbols.Csymbol == TechnicalIndicator.symbol).\
                            outerjoin(CompanyProfile, Symbols.Csymbol == CompanyProfile.symbol).order_by(StockInfo.price.desc())

    if Search:
        query = query.filter(
            or_(
                Symbols.Csymbol.ilike(f"%{Search}%"),
                Symbols.Cname.ilike(f"%{Search}%"),
               
                CompanyProfile.sector.ilike(f"%{Search}%")  

            )
        )
        results = query.all()
        result =[{ 
                "Symbol": result.Csymbol,
                "Name": result.Cname,
                "Price": f"{round(result.price,2)} USD",
                "Change": f"{result.changesPercentage}%",
                "1D": result.one_day,
                "1M": result.one_month,
                "1Y": result.one_year,
                "Volume": format_large_number(result.volume),
                "Marketap": format_large_number(result.marketCap),
                "52WeeksHigh": result.yearHigh,
                "52WeeksLow": result.yearLow,
                "SMA50": result.priceAvg50,
                "SMA200": result.priceAvg200,
                "Beta":result.beta,
                "RSI": result.rsi,
                "DividendYieldTTM": RoundTheValue(result.dividendYielTTM), 
                "Sector": result.sector
              } 
              for result in results]
        
        total = query.count()
        total_pages = (total + limit - 1) // limit

        return JSONResponse({
            "data": result,
            "total_pages": total_pages,
            "total_records": total,
            "current_pages": page
            })
    else:
    # query = query.filter(StockInfo.price <= StockInfo.yearLow)
        total = query.count()
        total_pages = (total + limit - 1) // limit

       
        results = query.offset(skip).limit(limit).all()

        result =[{ 
                    "Symbol": result.Csymbol,
                    "Name": result.Cname,
                    "Price": f"{round(result.price,2)} USD",
                    "Change": f"{result.changesPercentage}%",
                    "1D": result.one_day,
                    "1M": result.one_month,
                    "1Y": result.one_year,
                    "Volume": format_large_number(result.volume),
                    "Marketap": format_large_number(result.marketCap),
                    "52WeeksHigh": result.yearHigh,
                    "52WeeksLow": result.yearLow,
                    "SMA50": result.priceAvg50,
                    "SMA200": result.priceAvg200,
                    "Beta":result.beta,
                    "RSI": result.rsi,
                    "DividendYieldTTM": RoundTheValue(result.dividendYielTTM), 
                    "Sector": result.sector
                } 
                for result in results]

        return JSONResponse({
            "data": result,
            "total_pages": total_pages,
            "total_records": total,
            "current_pages": page
            })



@StockIdeaRouter.get("/stock/undertendollar")
async def UnderTen_Dollar(
    Search: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    limit: int = Query(10, le=100)
    ):
    skip = (page - 1) * limit
    query = db.session.query(CompanyProfile.image,Symbols.Csymbol,Symbols.Cname,StockInfo.price,StockInfo.onedayvolatility,StockInfo.changesPercentage,StockInfo.volume,StockInfo.marketCap,
                            StockInfo.pe,StockInfo.eps,StockInfo.yearHigh,StockInfo.yearLow,CompanyProfile.beta,CompanyProfile.sector,StockInfo.priceAvg50,StockInfo.priceAvg200, 
                            StockPerformance.one_day,StockPerformance.one_month,StockPerformance.one_year,TechnicalIndicator.rsi).\
                            outerjoin(StockInfo,Symbols.Csymbol == StockInfo.symbol).\
                            outerjoin(StockPerformance, Symbols.Csymbol == StockPerformance.symbol).\
                            outerjoin(TechnicalIndicator, Symbols.Csymbol == TechnicalIndicator.symbol).\
                            outerjoin(CompanyProfile, Symbols.Csymbol == CompanyProfile.symbol).order_by(StockInfo.price.desc())
    # query = query.filter(StockInfo.price <= 10)
    if Search:
        query = query.filter(
            or_(
                Symbols.Csymbol.ilike(f"%{Search}%"),
                Symbols.Cname.ilike(f"%{Search}%"),
               
                CompanyProfile.sector.ilike(f"%{Search}%")  

            )
        )
        results = query.all()
        result =[{ 
                "Symbol": result.Csymbol,
                "Name": result.Cname,
                "Price": f"{round(result.price,2)} USD",
                "Change": f"{result.changesPercentage}%",
                "1DVolatility": result.onedayvolatility,
                "1D": result.one_day,
                "1M": result.one_month,
                "1Y": result.one_year,
                "Volume": format_large_number(result.volume),
                "MarketCap": format_large_number(result.marketCap),
                "SMA50": result.priceAvg50,
                "SMA200": result.priceAvg200,
                "Beta":result.beta,
                "RSI": result.rsi,
                "PERatio": result.pe,
                "EPS": result.eps,
                "Sector": result.sector
              } 
              for result in results]
        
        total = query.count()
        total_pages = (total + limit - 1) // limit

        return JSONResponse({
            "data": result,
            "total_pages": total_pages,
            "total_records": total,
            "current_pages": page
            })

    else:
        
        total = query.count()
        total_pages = (total + limit - 1) // limit

        # query = query.filter(StockInfo.price <= StockInfo.yearLow)

        results = query.offset(skip).limit(limit).all()

        result =[{ 
                    "Symbol": result.Csymbol,
                    "Name": result.Cname,
                    "Price": f"{round(result.price,2)} USD",
                    "Change": f"{result.changesPercentage}%",
                    "1DVolatility": result.onedayvolatility,
                    "1D": result.one_day,
                    "1M": result.one_month,
                    "1Y": result.one_year,
                    "Volume": format_large_number(result.volume),
                    "MarketCap": format_large_number(result.marketCap),
                    "SMA50": result.priceAvg50,
                    "SMA200": result.priceAvg200,
                    "Beta":result.beta,
                    "RSI": result.rsi,
                    "PERatio": result.pe,
                    "EPS": result.eps,
                    "Sector": result.sector
                } 
                for result in results]

        return JSONResponse({
            "data": result,
            "total_pages": total_pages,
            "total_records": total,
            "current_pages": page
            })



@StockIdeaRouter.get("/stock/abovetendoller")
async def AboveTen_Dollar(
    Search: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    limit: int = Query(10, le=100)
    ):
    skip = (page - 1) * limit
    query = db.session.query(CompanyProfile.image,Symbols.Csymbol,Symbols.Cname,StockInfo.price,StockInfo.onedayvolatility,StockInfo.changesPercentage,StockInfo.volume,StockInfo.marketCap,
                            StockInfo.pe,StockInfo.eps,StockInfo.yearHigh,StockInfo.yearLow,CompanyProfile.beta,CompanyProfile.sector,StockInfo.priceAvg50,StockInfo.priceAvg200, 
                            StockPerformance.one_day,StockPerformance.one_month,StockPerformance.one_year,TechnicalIndicator.rsi).\
                            outerjoin(StockInfo,Symbols.Csymbol == StockInfo.symbol).\
                            outerjoin(StockPerformance, Symbols.Csymbol == StockPerformance.symbol).\
                            outerjoin(TechnicalIndicator, Symbols.Csymbol == TechnicalIndicator.symbol).\
                            outerjoin(CompanyProfile, Symbols.Csymbol == CompanyProfile.symbol).order_by(StockInfo.price.desc())
    # query = query.filter(StockInfo.price >= 10)
    if Search:
        query = query.filter(
            or_(
                Symbols.Csymbol.ilike(f"%{Search}%"),
                Symbols.Cname.ilike(f"%{Search}%"),
                CompanyProfile.sector.ilike(f"%{Search}%")  

            )
        )
        results = query.all()
        result =[{ 
                "Symbol": result.Csymbol,
                "Name": result.Cname,
                "Price": f"{round(result.price,2)} USD",
                "Change": f"{result.changesPercentage}%",
                "1DVolatility": result.onedayvolatility,
                "1D": result.one_day,
                "1M": result.one_month,
                "1Y": result.one_year,
                "Volume": format_large_number(result.volume),
                "MarketCap": format_large_number(result.marketCap),
                "SMA50": result.priceAvg50,
                "SMA200": result.priceAvg200,
                "Beta":result.beta,
                "RSI": result.rsi,
                "PERatio": result.pe,
                "EPS": result.eps,
                "Sector": result.sector
              } 
              for result in results]
        
        total = query.count()
        total_pages = (total + limit - 1) // limit

        return JSONResponse({
            "data": result,
            "total_pages": total_pages,
            "total_records": total,
            "current_pages": page
        })

    else:

        total = query.count()
        total_pages = (total + limit - 1) // limit

        # query = query.filter(StockInfo.price <= StockInfo.yearLow)

        results = query.offset(skip).limit(limit).all()

        result =[{ 
                    "Symbol": result.Csymbol,
                    "Name": result.Cname,
                    "Price": f"{round(result.price,2)} USD",
                    "Change": f"{result.changesPercentage}%",
                    "1DVolatility": result.onedayvolatility,
                    "1D": result.one_day,
                    "1M": result.one_month,
                    "1Y": result.one_year,
                    "Volume": format_large_number(result.volume),
                    "MarketCap": format_large_number(result.marketCap),
                    "SMA50": result.priceAvg50,
                    "SMA200": result.priceAvg200,
                    "Beta":result.beta,
                    "RSI": result.rsi,
                    "PERatio": result.pe,
                    "EPS": result.eps,
                    "Sector": result.sector
                } 
                for result in results]

        return JSONResponse({
            "data": result,
            "total_pages": total_pages,
            "total_records": total,
            "current_pages": page
        })


@StockIdeaRouter.get("/stock/negativebeta")
async def NegativeBeta(
    Search: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    limit: int = Query(10, le=100)
    ):
    skip = (page - 1) * limit
    query = db.session.query(CompanyProfile.image,Symbols.Csymbol,Symbols.Cname,StockInfo.price,StockInfo.onedayvolatility,StockInfo.changesPercentage,StockInfo.volume,StockInfo.marketCap,
                            StockInfo.pe,StockInfo.eps,StockInfo.yearHigh,StockInfo.yearLow,CompanyProfile.beta,CompanyProfile.sector,StockInfo.priceAvg50,StockInfo.priceAvg200, 
                            StockPerformance.one_day,StockPerformance.one_month,StockPerformance.one_year,TechnicalIndicator.rsi).\
                            outerjoin(StockInfo,Symbols.Csymbol == StockInfo.symbol).\
                            outerjoin(StockPerformance, Symbols.Csymbol == StockPerformance.symbol).\
                            outerjoin(TechnicalIndicator, Symbols.Csymbol == TechnicalIndicator.symbol).\
                            outerjoin(CompanyProfile, Symbols.Csymbol == CompanyProfile.symbol).order_by(StockInfo.price.desc())
    # query = query.filter(CompanyProfile.beta < 0)
    if Search:
        query = query.filter(
            or_(
                Symbols.Csymbol.ilike(f"%{Search}%"),
                Symbols.Cname.ilike(f"%{Search}%"),
             
                CompanyProfile.sector.ilike(f"%{Search}%")  

            )
        )
        results = query.all()
        result =[{ 
                "Symbol": result.Csymbol,
                "Name": result.Cname,
                "Price": f"{round(result.price,2)} USD",
                "Change": f"{result.changesPercentage}%",
                "1DVolatility": result.onedayvolatility,
                "1D": result.one_day,
                "1M": result.one_month,
                "1Y": result.one_year,
                "Volume": format_large_number(result.volume),
                "MarketCap": format_large_number(result.marketCap),
                "52WeeksHigh": result.yearHigh,
                "52WeeksLow": result.yearLow,
                "SMA50": result.priceAvg50,
                "SMA200": result.priceAvg200,
                "Beta":result.beta,
                "RSI": result.rsi,
                "Sector": result.sector
              } 
              for result in results]
        
        total = query.count()
        total_pages = (total + limit - 1) // limit

        return JSONResponse({
            "data": result,
            "total_pages": total_pages,
            "total_records": total,
            "current_pages": page
        })
    else:

        total = query.count()
        total_pages = (total + limit - 1) // limit

        # query = query.filter(StockInfo.price <= StockInfo.yearLow)

        results = query.offset(skip).limit(limit).all()

        result =[{ 
                    "Symbol": result.Csymbol,
                    "Name": result.Cname,
                    "Price": f"{round(result.price,2)} USD",
                    "Change": f"{result.changesPercentage}%",
                    "1DVolatility": result.onedayvolatility,
                    "1D": result.one_day,
                    "1M": result.one_month,
                    "1Y": result.one_year,
                    "Volume": format_large_number(result.volume),
                    "MarketCap": format_large_number(result.marketCap),
                    "52WeeksHigh": result.yearHigh,
                    "52WeeksLow": result.yearLow,
                    "SMA50": result.priceAvg50,
                    "SMA200": result.priceAvg200,
                    "Beta":result.beta,
                    "RSI": result.rsi,
                    "Sector": result.sector
                } 
                for result in results]

        return JSONResponse({
            "data": result,
            "total_pages": total_pages,
            "total_records": total,
            "current_pages": page
        })

@StockIdeaRouter.get("/stock/lowbeta")
async def LowBeta(
    Search: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    limit: int = Query(10, le=100)
    ):
    skip = (page - 1) * limit
    query = db.session.query(CompanyProfile.image,Symbols.Csymbol,Symbols.Cname,StockInfo.price,StockInfo.onedayvolatility,StockInfo.changesPercentage,StockInfo.volume,StockInfo.marketCap,
                            StockInfo.pe,StockInfo.eps,StockInfo.yearHigh,StockInfo.yearLow,CompanyProfile.beta,CompanyProfile.sector,StockInfo.priceAvg50,StockInfo.priceAvg200, 
                            StockPerformance.one_day,StockPerformance.one_month,StockPerformance.one_year,TechnicalIndicator.rsi).\
                            outerjoin(StockInfo,Symbols.Csymbol == StockInfo.symbol).\
                            outerjoin(StockPerformance, Symbols.Csymbol == StockPerformance.symbol).\
                            outerjoin(TechnicalIndicator, Symbols.Csymbol == TechnicalIndicator.symbol).\
                            outerjoin(CompanyProfile, Symbols.Csymbol == CompanyProfile.symbol).order_by(StockInfo.price.desc())
    # query = query.filter(CompanyProfile.beta < 1)
    if Search:
        query = query.filter(
            or_(
                Symbols.Csymbol.ilike(f"%{Search}%"),
                Symbols.Cname.ilike(f"%{Search}%"),
              
                CompanyProfile.sector.ilike(f"%{Search}%")  

            )
        )
        results = query.all()
        result =[{ 
                "Symbol": result.Csymbol,
                "Name": result.Cname,
                "Price": f"{round(result.price,2)} USD",
                "Change": f"{result.changesPercentage}%",
                "1DVolatility": result.onedayvolatility,
                "1D": result.one_day,
                "1M": result.one_month,
                "1Y": result.one_year,
                "Volume": format_large_number(result.volume),
                "MarketCap": format_large_number(result.marketCap),
                "52WeeksHigh": result.yearHigh,
                "52WeeksLow": result.yearLow,
                "SMA50": result.priceAvg50,
                "SMA200": result.priceAvg200,
                "Beta":result.beta,
                "RSI": result.rsi,
                "Sector": result.sector
              } 
              for result in results]
        
        total = query.count()
        total_pages = (total + limit - 1) // limit

        return JSONResponse({
            "data": result,
            "total_pages": total_pages,
            "total_records": total,
            "current_pages": page
        })
    else:
        total = query.count()
        total_pages = (total + limit - 1) // limit

        # query = query.filter(StockInfo.price <= StockInfo.yearLow)

        results = query.offset(skip).limit(limit).all()

        result =[{ 
                    "Symbol": result.Csymbol,
                    "Name": result.Cname,
                    "Price": f"{round(result.price,2)} USD",
                    "Change": f"{result.changesPercentage}%",
                    "1DVolatility": result.onedayvolatility,
                    "1D": result.one_day,
                    "1M": result.one_month,
                    "1Y": result.one_year,
                    "Volume": format_large_number(result.volume),
                    "MarketCap": format_large_number(result.marketCap),
                    "52WeeksHigh": result.yearHigh,
                    "52WeeksLow": result.yearLow,
                    "SMA50": result.priceAvg50,
                    "SMA200": result.priceAvg200,
                    "Beta":result.beta,
                    "RSI": result.rsi,
                    "Sector": result.sector
                } 
                for result in results]

        
        return JSONResponse({
            "data": result,
            "total_pages": total_pages,
            "total_records": total,
            "current_pages": page
        })


@StockIdeaRouter.get("/stock/highriskandreward")
async def HighRisk_Reward(
    Search: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    limit: int = Query(10, le=100)
    ):
    skip = (page - 1) * limit
    query = db.session.query(Symbols.Csymbol,Symbols.Cname,StockInfo.price,StockInfo.onedayvolatility,StockInfo.changesPercentage,StockInfo.volume,StockInfo.marketCap,
                            StockInfo.pe,StockInfo.eps,StockInfo.yearHigh,StockInfo.yearLow,CompanyProfile.beta,CompanyProfile.sector,StockInfo.priceAvg50,StockInfo.priceAvg200, 
                            StockPerformance.one_day,StockPerformance.one_month,StockPerformance.one_year,FinancialMetrics.priceBookValueRatioTTM,FinancialMetrics.debtEquityRatioTTM,\
                            FinancialMetrics.dividendYielTTM,FinancialMetrics.priceEarningsRatioTTM,TechnicalIndicator.rsi).\
                            outerjoin(StockInfo,Symbols.Csymbol == StockInfo.symbol).\
                            outerjoin(StockPerformance, Symbols.Csymbol == StockPerformance.symbol).\
                            outerjoin(FinancialMetrics, Symbols.Csymbol == FinancialMetrics.symbol).\
                            outerjoin(TechnicalIndicator, Symbols.Csymbol == TechnicalIndicator.symbol).\
                            outerjoin(CompanyProfile, Symbols.Csymbol == CompanyProfile.symbol).order_by(StockInfo.price.desc())
    
    #  # Query for high-risk, high-reward stocks
    # query = query.filter(
    #     or_(

    #         StockInfo.onedayvolatility > 5,  # Filter for high volatility, e.g., daily volatility > 5%
    #         StockInfo.marketCap < 1000000000,  # Filter for small market cap (less than 1 billion)
    #         CompanyProfile.beta > 1,  # Filter for high beta stocks (greater than 1)
    #         StockInfo.pe > 20  # Filter for high P/E ratio (indicative of high growth potential)
    #     )
    # )
    
    if Search:
        query = query.filter(
            or_(
                Symbols.Csymbol.ilike(f"%{Search}%"),
                Symbols.Cname.ilike(f"%{Search}%"),
                CompanyProfile.sector.ilike(f"%{Search}%")  

            )
        )
        results = query.all()
        result =[{ 
                "Symbol": result.Csymbol,
                "Name": result.Cname,
                "Price": f"{round(result.price,2)} USD",
                "Change": f"{result.changesPercentage}%",
                "1DVolatility": result.onedayvolatility,
                "1D": result.one_day,
                "1M": result.one_month,
                "1Y": result.one_year,
                "Volume": format_large_number(result.volume),
                "MarketCap": format_large_number(result.marketCap),
                "52WeeksHigh": result.yearHigh,
                "52WeeksLow": result.yearLow,
                "SMA50": result.priceAvg50,
                "SMA200": result.priceAvg200,
                "Beta":result.beta,
                "RSI": result.rsi,
                "PERatio": result.pe,
                "PBRatioTTM": result.priceBookValueRatioTTM, 
                "EarningGrowthTTM": result.priceEarningsRatioTTM, 
                "DebttoEquityTTM": result.debtEquityRatioTTM, 
                "RisktoRewardRatioTTM": "pending", 
                "DividendYieldTTM": RoundTheValue(result.dividendYielTTM), 
                "Sector": result.sector
              } 
              for result in results]
        
    else:
                
        total = query.count()
        total_pages = (total + limit - 1) // limit

        # query = query.filter(StockInfo.price <= StockInfo.yearLow)

        results = query.offset(skip).limit(limit).all()

        result =[{ 
                    "Symbol": result.Csymbol,
                    "Name": result.Cname,
                    "Price": f"{round(result.price,2)} USD",
                    "Change": f"{result.changesPercentage}%",
                    "1DVolatility": result.onedayvolatility,
                    "1D": result.one_day,
                    "1M": result.one_month,
                    "1Y": result.one_year,
                    "Volume": format_large_number(result.volume),
                    "MarketCap": format_large_number(result.marketCap),
                    "52WeeksHigh": result.yearHigh,
                    "52WeeksLow": result.yearLow,
                    "SMA50": result.priceAvg50,
                    "SMA200": result.priceAvg200,
                    "Beta":result.beta,
                    "RSI": result.rsi,
                    "PERatio": result.pe,
                    "PBRatioTTM": result.priceBookValueRatioTTM, 
                    "EarningGrowthTTM": result.priceEarningsRatioTTM, 
                    "DebttoEquityTTM": result.debtEquityRatioTTM, 
                    "RisktoRewardRatioTTM": "pending", 
                    "DividendYieldTTM": RoundTheValue(result.dividendYielTTM), 
                    "Sector": result.sector
                } 
                for result in results]


        return JSONResponse({
            "data": result,
            "total_pages": total_pages,
            "total_records": total,
            "current_pages": page
        })



@StockIdeaRouter.get("/stock/debtfreestocks")
async def DebtFree_Stocks(
    Search: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    limit: int = Query(10, le=100)
    ):
    skip = (page - 1) * limit
    query = db.session.query(Symbols.Csymbol,Symbols.Cname,StockInfo.price,StockInfo.onedayvolatility,StockInfo.changesPercentage,StockInfo.volume,StockInfo.marketCap,
                            StockInfo.pe,StockInfo.eps,StockInfo.yearHigh,StockInfo.yearLow,CompanyProfile.beta,CompanyProfile.sector,StockInfo.priceAvg50,StockInfo.priceAvg200, 
                            StockPerformance.one_day,StockPerformance.one_month,StockPerformance.one_year,FinancialMetrics.currentRatioTTM,FinancialMetrics.quickRatioTTM,FinancialMetrics.freeCashFlowPerShareTTM,
                            FinancialMetrics.payoutRatioTTM,FinancialMetrics.netProfitMarginTTM,FinancialGrowth.revenueGrowth).\
                            outerjoin(StockInfo,Symbols.Csymbol == StockInfo.symbol).\
                            outerjoin(StockPerformance, Symbols.Csymbol == StockPerformance.symbol).\
                            outerjoin(FinancialMetrics, Symbols.Csymbol == FinancialMetrics.symbol).\
                            outerjoin(FinancialGrowth, Symbols.Csymbol == FinancialGrowth.symbol).\
                            outerjoin(CompanyProfile, Symbols.Csymbol == CompanyProfile.symbol).order_by(StockInfo.price.desc())
 
    if Search:
        query = query.filter(
            or_(
                Symbols.Csymbol.ilike(f"%{Search}%"),
                Symbols.Cname.ilike(f"%{Search}%"),
               
                CompanyProfile.sector.ilike(f"%{Search}%")  

            )
        )
        results = query.all()
        
        result =[{ 
                "Symbol": result.Csymbol,
                "Name": result.Cname,
                "Price": f"{round(result.price,2)} USD",
                "Change": f"{result.changesPercentage}%",
                "1DVolatility": result.onedayvolatility,
                "Volume": format_large_number(result.volume),
                "MarketCap": format_large_number(result.marketCap),
                "Beta":result.beta,
                "PERatio": result.pe,
                "CurrentRatioTTM": result.currentRatioTTM, 
                "QuickRatioTTM": result.quickRatioTTM,
                "FreeCashFlowTTM": result.freeCashFlowPerShareTTM,
                "ProfitMarginsTTM": result.netProfitMarginTTM,
                "DividendPayoutRatioTTM": result.payoutRatioTTM,
                "RevenueGrowthTTM": result.revenueGrowth,
                "Sector": result.sector
              } 
              for result in results]
        
        total = query.count()
        total_pages = (total + limit - 1) // limit

        return JSONResponse({
            "data": result,
            "total_pages": total_pages,
            "total_records": total,
            "current_pages": page
        })
    else:
        total = query.count()
        total_pages = (total + limit - 1) // limit

        # query = query.filter(StockInfo.price <= StockInfo.yearLow)

        results = query.offset(skip).limit(limit).all()

        result =[{ 
                    "Symbol": result.Csymbol,
                    "Name": result.Cname,
                    "Price": f"{round(result.price,2)} USD",
                    "Change": f"{result.changesPercentage}%",
                    "1DVolatility": result.onedayvolatility,
                    "Volume": format_large_number(result.volume),
                    "MarketCap": format_large_number(result.marketCap),
                    "Beta":result.beta,
                    "PERatio": result.pe,
                    "CurrentRatioTTM": result.currentRatioTTM, 
                    "QuickRatioTTM": result.quickRatioTTM,
                    "FreeCashFlowTTM": result.freeCashFlowPerShareTTM,
                    "ProfitMarginsTTM": result.netProfitMarginTTM,
                    "DividendPayoutRatioTTM": result.payoutRatioTTM,
                    "RevenueGrowthTTM": result.revenueGrowth,
                    "Sector": result.sector
                } 
                for result in results]

        return JSONResponse({
            "data": result,
            "total_pages": total_pages,
            "total_records": total,
            "current_pages": page
        })


@StockIdeaRouter.get("/stock/dividend")
async def Dividend(
    Search: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    limit: int = Query(10, le=100)
    ):
    skip = (page - 1) * limit
    query = db.session.query(Symbols.Csymbol,Symbols.Cname,StockInfo.price,StockInfo.onedayvolatility,StockInfo.changesPercentage,StockInfo.volume,StockInfo.marketCap,
                            StockInfo.pe,StockInfo.eps,StockInfo.yearHigh,StockInfo.yearLow,CompanyProfile.beta,CompanyProfile.sector,StockInfo.priceAvg50,StockInfo.priceAvg200, 
                            StockPerformance.one_day,StockPerformance.one_month,StockPerformance.one_year,FinancialMetrics.freeCashFlowPerShareTTM,FinancialMetrics.payoutRatioTTM,
                            FinancialMetrics.netProfitMarginTTM,FinancialMetrics.dividendYielTTM,FinancialGrowth.revenueGrowth).\
                            outerjoin(StockInfo,Symbols.Csymbol == StockInfo.symbol).\
                            outerjoin(StockPerformance, Symbols.Csymbol == StockPerformance.symbol).\
                            outerjoin(FinancialMetrics, Symbols.Csymbol == FinancialMetrics.symbol).\
                            outerjoin(FinancialGrowth, Symbols.Csymbol == FinancialGrowth.symbol).\
                            outerjoin(CompanyProfile, Symbols.Csymbol == CompanyProfile.symbol).order_by(StockInfo.price.desc())
    
    
    
    if Search:
        query = query.filter(
            or_(
                Symbols.Csymbol.ilike(f"%{Search}%"),
                Symbols.Cname.ilike(f"%{Search}%"),
              
                CompanyProfile.sector.ilike(f"%{Search}%")  

            )
        )
        results = query.all()

        result =[{ 
            "Symbol": result.Csymbol,
            "Name": result.Cname,
            "Price": f"{round(result.price,2)} USD",
            "Change": f"{result.changesPercentage}%",
            "1DVolatility": result.onedayvolatility,
            "Volume": format_large_number(result.volume),
            "MarketCap": format_large_number(result.marketCap),
            "DividendYieldTTM": result.dividendYielTTM,
            "EPS": result.eps,
            "Beta":result.beta,
            "PERatio": result.pe,
            "FreeCashFlowTTM": result.freeCashFlowPerShareTTM,
            "ProfitMarginsTTM": result.netProfitMarginTTM,
            "DividendPayoutRatioTTM": result.payoutRatioTTM,
            "RevenueGrowthTTM": result.revenueGrowth,
            "Sector": result.sector
            } 
            for result in results]
        
        total = query.count()
        total_pages = (total + limit - 1) // limit

        return JSONResponse({
            "data": result,
            "total_pages": total_pages,
            "total_records": total,
            "current_pages": page
        })
    
    else:

        total = query.count()
        total_pages = (total + limit - 1) // limit

        # query = query.filter(StockInfo.price <= StockInfo.yearLow)

        results = query.offset(skip).limit(limit).all()

        result =[{ 
                    "Symbol": result.Csymbol,
                    "Name": result.Cname,
                    "Price": f"{round(result.price,2)} USD",
                    "Change": f"{result.changesPercentage}%",
                    "1DVolatility": result.onedayvolatility,
                    "Volume": format_large_number(result.volume),
                    "MarketCap": format_large_number(result.marketCap),
                    "DividendYieldTTM": result.dividendYielTTM,
                    "EPS": result.eps,
                    "Beta":result.beta,
                    "PERatio": result.pe,
                    "FreeCashFlowTTM": result.freeCashFlowPerShareTTM,
                    "ProfitMarginsTTM": result.netProfitMarginTTM,
                    "DividendPayoutRatioTTM": result.payoutRatioTTM,
                    "RevenueGrowthTTM": result.revenueGrowth,
                    "Sector": result.sector
                } 
                for result in results]

        return JSONResponse({
            "data": result,
            "total_pages": total_pages,
            "total_records": total,
            "current_pages": page
        })



@StockIdeaRouter.get("/stock/lowperatio")
async def LowPERatio(
    Search: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    limit: int = Query(10, le=100)
    ):
    skip = (page - 1) * limit
    query = db.session.query(Symbols.Csymbol,Symbols.Cname,StockInfo.price,StockInfo.onedayvolatility,StockInfo.changesPercentage,StockInfo.volume,StockInfo.marketCap,
                            StockInfo.pe,StockInfo.eps,StockInfo.yearHigh,StockInfo.yearLow,CompanyProfile.beta,CompanyProfile.sector,StockInfo.priceAvg50,StockInfo.priceAvg200, 
                            StockPerformance.one_day,StockPerformance.one_month,StockPerformance.one_year,FinancialMetrics.freeCashFlowPerShareTTM,
                            FinancialMetrics.payoutRatioTTM,FinancialMetrics.debtEquityRatioTTM,FinancialMetrics.priceToBookRatioTTM,
                            FinancialMetrics.netProfitMarginTTM,FinancialGrowth.revenueGrowth).\
                            outerjoin(StockInfo,Symbols.Csymbol == StockInfo.symbol).\
                            outerjoin(StockPerformance, Symbols.Csymbol == StockPerformance.symbol).\
                            outerjoin(FinancialMetrics, Symbols.Csymbol == FinancialMetrics.symbol).\
                            outerjoin(FinancialGrowth, Symbols.Csymbol == FinancialGrowth.symbol).\
                            outerjoin(CompanyProfile, Symbols.Csymbol == CompanyProfile.symbol).order_by(StockInfo.price.desc())
    
    
    
    if Search:
        query = query.filter(
            or_(
                Symbols.Csymbol.ilike(f"%{Search}%"),
                Symbols.Cname.ilike(f"%{Search}%"),

                CompanyProfile.sector.ilike(f"%{Search}%")  

            )
        )
        results = query.all()

        result =[{ 
                "Symbol": result.Csymbol,
                "Name": result.Cname,
                "Price": f"{round(result.price,2)} USD",
                "Change": f"{result.changesPercentage}%",
                "Volume": format_large_number(result.volume),
                "MarketCap": format_large_number(result.marketCap),
                "Beta":result.beta,
                "PERatio": result.pe,
                "FreeCashFlowTTM": result.freeCashFlowPerShareTTM,
                "ProfitMarginsTTM":  result.netProfitMarginTTM,
                "DividendPayoutRatioTTM": result.payoutRatioTTM,
                "RevenueGrowthTTM": result.revenueGrowth,
                "DebtToEquityRatioTTM": result.debtEquityRatioTTM,
                "PriceToBookRatioTTM": result.priceToBookRatioTTM,
                # "ProfitMarginTTM": result.netProfitMarginTTM,
                "Sector": result.sector
              } 
              for result in results]
        
        total = query.count()
        total_pages = (total + limit - 1) // limit

        return JSONResponse({
            "data": result,
            "total_pages": total_pages,
            "total_records": total,
            "current_pages": page
        })
    else:
        total = query.count()
        total_pages = (total + limit - 1) // limit
        # query = query.filter(StockInfo.price <= StockInfo.yearLow)

        results = query.offset(skip).limit(limit).all()

        result =[{ 
                    "Symbol": result.Csymbol,
                    "Name": result.Cname,
                    "Price": f"{round(result.price,2)} USD",
                    "Change": f"{result.changesPercentage}%",
                    "Volume": format_large_number(result.volume),
                    "MarketCap": format_large_number(result.marketCap),
                    "Beta":result.beta,
                    "PERatio": result.pe,
                    "FreeCashFlowTTM": result.freeCashFlowPerShareTTM,
                    "ProfitMarginsTTM":  result.netProfitMarginTTM,
                    "DividendPayoutRatioTTM": result.payoutRatioTTM,
                    "RevenueGrowthTTM": result.revenueGrowth,
                    "DebtToEquityRatioTTM": result.debtEquityRatioTTM,
                    "PriceToBookRatioTTM": result.priceToBookRatioTTM,
                    # "ProfitMarginTTM": result.netProfitMarginTTM,
                    "Sector": result.sector
                } 
                for result in results]


        return JSONResponse({
            "data": result,
            "total_pages": total_pages,
            "total_records": total,
            "current_pages": page
        })


@StockIdeaRouter.get("/stock/todaytopgain")
async def TodayTopGain(
    Search: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    limit: int = Query(10, le=100)
    ):
    skip = (page - 1) * limit
    query = db.session.query(Symbols.Csymbol,Symbols.Cname,StockInfo.price,StockInfo.onedayvolatility,StockInfo.changesPercentage,StockInfo.volume,StockInfo.marketCap,
                            StockInfo.pe,StockInfo.eps,StockInfo.yearHigh,StockInfo.yearLow,CompanyProfile.beta,CompanyProfile.sector,StockInfo.priceAvg50,StockInfo.priceAvg200,StockInfo.dayHigh,StockInfo.dayLow,
                            StockPerformance.one_day,StockPerformance.one_month,StockPerformance.one_year,FinancialMetrics.freeCashFlowPerShareTTM,FinancialMetrics.payoutRatioTTM,
                            TechnicalIndicator.rsi, FinancialMetrics.netProfitMarginTTM,FinancialGrowth.revenueGrowth).\
                            outerjoin(StockInfo,Symbols.Csymbol == StockInfo.symbol).\
                            outerjoin(StockPerformance, Symbols.Csymbol == StockPerformance.symbol).\
                            outerjoin(FinancialMetrics, Symbols.Csymbol == FinancialMetrics.symbol).\
                            outerjoin(TechnicalIndicator, Symbols.Csymbol == TechnicalIndicator.symbol).\
                            outerjoin(FinancialGrowth, Symbols.Csymbol == FinancialGrowth.symbol).\
                            outerjoin(CompanyProfile, Symbols.Csymbol == CompanyProfile.symbol).order_by(StockInfo.price.desc())

    if Search:
        query = query.filter(
            or_(
                Symbols.Csymbol.ilike(f"%{Search}%"),
                Symbols.Cname.ilike(f"%{Search}%"),
               
                CompanyProfile.sector.ilike(f"%{Search}%")  

            )
        )
        results = query.all()

        result =[{ 
            "Symbol": result.Csymbol,
            "Name": result.Cname,
            "Price": f"{round(result.price,2)} USD",
            "Change": f"{result.changesPercentage}%",
            "Volume": format_large_number(result.volume),
            "MarketCap": format_large_number(result.marketCap),
            "DayHigh": result.dayHigh,
            "DayLow": result.dayLow,
            "52WeeksHigh": result.yearHigh,
            "52WeeksLow": result.yearLow,
            "SMA50": result.priceAvg50,
            "SMA200": result.priceAvg200,
            "Beta":result.beta,
            "PERatio": result.pe,
            "RSI": result.rsi,
            "FreeCashFlowTTM": result.freeCashFlowPerShareTTM,
            "ProfitMarginsTTM": result.netProfitMarginTTM,
            "DividendPayoutRatioTTM": result.payoutRatioTTM,
            "RevenueGrowthTTM": result.revenueGrowth,
            "Sector": result.sector
            } 
            for result in results]
        
        total = query.count()
        total_pages = (total + limit - 1) // limit

        return JSONResponse({
            "data": result,
            "total_pages": total_pages,
            "total_records": total,
            "current_pages": page
        })
    else: 
        total = query.count()
        total_pages = (total + limit - 1) // limit

        # query = query.filter(StockInfo.price <= StockInfo.yearLow)

        results = query.offset(skip).limit(limit).all()

        result =[{ 
                    "Symbol": result.Csymbol,
                    "Name": result.Cname,
                    "Price": f"{round(result.price,2)} USD",
                    "Change": f"{result.changesPercentage}%",
                    "Volume": format_large_number(result.volume),
                    "MarketCap": format_large_number(result.marketCap),
                    "DayHigh": result.dayHigh,
                    "DayLow": result.dayLow,
                    "52WeeksHigh": result.yearHigh,
                    "52WeeksLow": result.yearLow,
                    "SMA50": result.priceAvg50,
                    "SMA200": result.priceAvg200,
                    "Beta":result.beta,
                    "PERatio": result.pe,
                    "RSI": result.rsi,
                    "FreeCashFlowTTM": result.freeCashFlowPerShareTTM,
                    "ProfitMarginsTTM": result.netProfitMarginTTM,
                    "DividendPayoutRatioTTM": result.payoutRatioTTM,
                    "RevenueGrowthTTM": result.revenueGrowth,
                    "Sector": result.sector
                } 
                for result in results]

        return JSONResponse({
            "data": result,
            "total_pages": total_pages,
            "total_records": total,
            "current_pages": page
        })


@StockIdeaRouter.get("/stock/todaytoploss")
async def TodayTopLoss(
    Search: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    limit: int = Query(10, le=100)
    ):
    skip = (page - 1) * limit
    query = db.session.query(Symbols.Csymbol,Symbols.Cname,StockInfo.price,StockInfo.onedayvolatility,StockInfo.changesPercentage,StockInfo.volume,StockInfo.marketCap,
                            StockInfo.pe,StockInfo.eps,StockInfo.yearHigh,StockInfo.yearLow,CompanyProfile.beta,CompanyProfile.sector,StockInfo.priceAvg50,StockInfo.priceAvg200,StockInfo.dayHigh,StockInfo.dayLow,
                            StockPerformance.one_day,StockPerformance.one_month,StockPerformance.one_year,FinancialMetrics.freeCashFlowPerShareTTM,FinancialMetrics.payoutRatioTTM,TechnicalIndicator.rsi,
                            FinancialMetrics.netProfitMarginTTM,FinancialGrowth.revenueGrowth).\
                            outerjoin(StockInfo,Symbols.Csymbol == StockInfo.symbol).\
                            outerjoin(StockPerformance, Symbols.Csymbol == StockPerformance.symbol).\
                            outerjoin(FinancialMetrics, Symbols.Csymbol == FinancialMetrics.symbol).\
                            outerjoin(TechnicalIndicator, Symbols.Csymbol == TechnicalIndicator.symbol).\
                            outerjoin(FinancialGrowth, Symbols.Csymbol == FinancialGrowth.symbol).\
                            outerjoin(CompanyProfile, Symbols.Csymbol == CompanyProfile.symbol).order_by(StockInfo.price.desc())
    
    
    
    if Search:
        query = query.filter(
            or_(
                Symbols.Csymbol.ilike(f"%{Search}%"),
                Symbols.Cname.ilike(f"%{Search}%"),
            
                CompanyProfile.sector.ilike(f"%{Search}%")  

            )
        )
        results = query.all()
        result =[{ 
            "Symbol": result.Csymbol,
            "Name": result.Cname,
            "Price": f"{round(result.price,2)} USD",
            "Change": f"{result.changesPercentage}%",
            "Volume": format_large_number(result.volume),
            "MarketCap": format_large_number(result.marketCap),
            "DayHigh": result.dayHigh,
            "DayLow": result.dayLow,
            "52WeeksHigh": result.yearHigh,
            "52WeeksLow": result.yearLow,
            "SMA50": result.priceAvg50,
            "SMA200": result.priceAvg200,
            "Beta":result.beta,
            "PERatio": result.pe,
            "RSI": result.rsi,
            "FreeCashFlowTTM": result.freeCashFlowPerShareTTM,
            "ProfitMarginsTTM": result.netProfitMarginTTM,
            "DividendPayoutRatioTTM": result.payoutRatioTTM,
            "RevenueGrowthTTM": result.revenueGrowth,
            "Sector": result.sector
            } 
            for result in results]
        
        total = query.count()
        total_pages = (total + limit - 1) // limit

        return JSONResponse({
            "data": result,
            "total_pages": total_pages,
            "total_records": total,
            "current_pages": page
            })
    else:
        total = query.count()
        total_pages = (total + limit - 1) // limit

        # query = query.filter(StockInfo.price <= StockInfo.yearLow)

        results = query.offset(skip).limit(limit).all()

        result =[{ 
                    "Symbol": result.Csymbol,
                    "Name": result.Cname,
                    "Price": f"{round(result.price,2)} USD",
                    "Change": f"{result.changesPercentage}%",
                    "Volume": format_large_number(result.volume),
                    "MarketCap": format_large_number(result.marketCap),
                    "DayHigh": result.dayHigh,
                    "DayLow": result.dayLow,
                    "52WeeksHigh": result.yearHigh,
                    "52WeeksLow": result.yearLow,
                    "SMA50": result.priceAvg50,
                    "SMA200": result.priceAvg200,
                    "Beta":result.beta,
                    "PERatio": result.pe,
                    "RSI": result.rsi,
                    "FreeCashFlowTTM": result.freeCashFlowPerShareTTM,
                    "ProfitMarginsTTM": result.netProfitMarginTTM,
                    "DividendPayoutRatioTTM": result.payoutRatioTTM,
                    "RevenueGrowthTTM": result.revenueGrowth,
                    "Sector": result.sector
                } 
                for result in results]

        return JSONResponse({
            "data": result,
            "total_pages": total_pages,
            "total_records": total,
            "current_pages": page
            })



@StockIdeaRouter.get("/stock/topperformance")
async def TopPerformance(
    Search: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    limit: int = Query(10, le=100)
    ):
    skip = (page - 1) * limit
    query = db.session.query(Symbols.Csymbol,Symbols.Cname,StockInfo.price,StockInfo.onedayvolatility,StockInfo.changesPercentage,StockInfo.volume,StockInfo.marketCap,
                            StockInfo.pe,StockInfo.eps,StockInfo.yearHigh,StockInfo.yearLow,CompanyProfile.beta,CompanyProfile.sector,StockInfo.priceAvg50,StockInfo.priceAvg200,StockInfo.dayHigh,StockInfo.dayLow,
                            StockPerformance.one_day,StockPerformance.one_month,StockPerformance.one_year,FinancialMetrics.freeCashFlowPerShareTTM,FinancialMetrics.dividendYielTTM,TechnicalIndicator.rsi,
                            FinancialMetrics.netProfitMarginTTM,FinancialGrowth.revenueGrowth).\
                            outerjoin(StockInfo,Symbols.Csymbol == StockInfo.symbol).\
                            outerjoin(StockPerformance, Symbols.Csymbol == StockPerformance.symbol).\
                            outerjoin(FinancialMetrics, Symbols.Csymbol == FinancialMetrics.symbol).\
                            outerjoin(TechnicalIndicator, Symbols.Csymbol == TechnicalIndicator.symbol).\
                            outerjoin(FinancialGrowth, Symbols.Csymbol == FinancialGrowth.symbol).\
                            outerjoin(CompanyProfile, Symbols.Csymbol == CompanyProfile.symbol).order_by(StockInfo.price.desc())

    if Search:
        query = query.filter(
            or_(
                Symbols.Csymbol.ilike(f"%{Search}%"),
                Symbols.Cname.ilike(f"%{Search}%"),
              
                CompanyProfile.sector.ilike(f"%{Search}%")  

            )
        )
        results = query.all()

        result =[{ 
                "Symbol": result.Csymbol,
                "Name": result.Cname,
                "Price": f"{round(result.price,2)} USD",
                "Change": f"{result.changesPercentage}%",
                "Volume": format_large_number(result.volume),
                "MarketCap": format_large_number(result.marketCap),
                "DayHigh": result.dayHigh,
                "DayLow": result.dayLow,
                "1D": result.one_day,
                "1M": result.one_month,
                "1Y": result.one_year,
                "52WeeksHigh": result.yearHigh,
                "52WeeksLow": result.yearLow,
                "SMA50": result.priceAvg50,
                "SMA200": result.priceAvg200,
                "Beta":result.beta,
                "PERatio": result.pe,
                "EPS": result.eps,
                "RSI": result.rsi,
                "FreeCashFlowTTM": result.freeCashFlowPerShareTTM,
                "ProfitMarginsTTM": result.netProfitMarginTTM,
                "DividendYieldTTM": RoundTheValue(result.dividendYielTTM),
                "RevenueGrowthTTM": result.revenueGrowth,
                "Sector": result.sector
              } 
              for result in results]
        
        total = query.count()
        total_pages = (total + limit - 1) // limit

        return JSONResponse({
            "data": result,
            "total_pages": total_pages,
            "total_records": total,
            "current_pages": page
            })

    else:
        total = query.count()
        total_pages = (total + limit - 1) // limit
        # query = query.filter(StockInfo.price <= StockInfo.yearLow)

        results = query.offset(skip).limit(limit).all()

        result =[{ 
                    "Symbol": result.Csymbol,
                    "Name": result.Cname,
                    "Price": f"{round(result.price,2)} USD",
                    "Change": f"{result.changesPercentage}%",
                    "Volume": format_large_number(result.volume),
                    "MarketCap": format_large_number(result.marketCap),
                    "DayHigh": result.dayHigh,
                    "DayLow": result.dayLow,
                    "1D": result.one_day,
                    "1M": result.one_month,
                    "1Y": result.one_year,
                    "52WeeksHigh": result.yearHigh,
                    "52WeeksLow": result.yearLow,
                    "SMA50": result.priceAvg50,
                    "SMA200": result.priceAvg200,
                    "Beta":result.beta,
                    "PERatio": result.pe,
                    "EPS": result.eps,
                    "RSI": result.rsi,
                    "FreeCashFlowTTM": result.freeCashFlowPerShareTTM,
                    "ProfitMarginsTTM": result.netProfitMarginTTM,
                    "DividendYieldTTM": RoundTheValue(result.dividendYielTTM),
                    "RevenueGrowthTTM": result.revenueGrowth,
                    "Sector": result.sector
                } 
                for result in results]
        
        return JSONResponse({
            "data": result,
            "total_pages": total_pages,
            "total_records": total,
            "current_pages": page
        })



@StockIdeaRouter.get("/stock/highdividendyield")
async def HighDividendYield(
    Search: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    limit: int = Query(10, le=100)
    ):
    skip = (page - 1) * limit
    query = db.session.query(Symbols.Csymbol,Symbols.Cname,StockInfo.price,StockInfo.onedayvolatility,StockInfo.changesPercentage,StockInfo.volume,StockInfo.marketCap,
                            StockInfo.pe,StockInfo.eps,StockInfo.yearHigh,StockInfo.yearLow,CompanyProfile.beta,CompanyProfile.sector,StockInfo.priceAvg50,StockInfo.priceAvg200,StockInfo.dayHigh,StockInfo.dayLow,
                            StockPerformance.one_day,StockPerformance.one_month,StockPerformance.one_year,FinancialMetrics.payoutRatioTTM,FinancialMetrics.dividendYielTTM,FinancialMetrics.dividendPerShareTTM,
                            FinancialMetrics.freeCashFlowPerShareTTM,FinancialGrowth.revenueGrowth,FinancialGrowth.netIncomeGrowth).\
                            outerjoin(StockInfo,Symbols.Csymbol == StockInfo.symbol).\
                            outerjoin(StockPerformance, Symbols.Csymbol == StockPerformance.symbol).\
                            outerjoin(FinancialMetrics, Symbols.Csymbol == FinancialMetrics.symbol).\
                            outerjoin(FinancialGrowth, Symbols.Csymbol == FinancialGrowth.symbol).\
                            outerjoin(CompanyProfile, Symbols.Csymbol == CompanyProfile.symbol).order_by(StockInfo.price.desc())

    if Search:
        query = query.filter(
            or_(
                Symbols.Csymbol.ilike(f"%{Search}%"),
                Symbols.Cname.ilike(f"%{Search}%"),
               
                CompanyProfile.sector.ilike(f"%{Search}%")  

            )
        )

        results = query.all()

        result =[{ 
                "Symbol": result.Csymbol,
                "Name": result.Cname,
                "Price": f"{round(result.price,2)} USD",
                "Change": f"{result.changesPercentage}%",
                "Volume": format_large_number(result.volume),
                "MarketCap": format_large_number(result.marketCap),
                "52WeeksHigh": result.yearHigh,
                "52WeeksLow": result.yearLow,
                "Beta":result.beta,
                "PERatio": result.pe,
                "EPS": result.eps,      
                "PayoutRatioTTM": result.payoutRatioTTM,
                "DividendYieldTTM": RoundTheValue(result.dividendYielTTM),
                "DividendPerShareTTM": result.dividendPerShareTTM,
                "RevenueGrowthTTM": result.revenueGrowth,
                "NetIncomeGrowth": result.netIncomeGrowth,
                "FreeCashFlowTTM": result.freeCashFlowPerShareTTM,
                "Sector": result.sector
              } 
              for result in results]
        
        total = query.count()
        total_pages = (total + limit - 1) // limit

        return JSONResponse({
            "data": result,
            "total_pages": total_pages,
            "total_records": total,
            "current_pages": page
        })
    
    else:
        total = query.count()
        total_pages = (total + limit - 1) // limit

        # query = query.filter(StockInfo.price <= StockInfo.yearLow)

        results = query.offset(skip).limit(limit).all()

        result =[{ 
                    "Symbol": result.Csymbol,
                    "Name": result.Cname,
                    "Price": f"{round(result.price,2)} USD",
                    "Change": f"{result.changesPercentage}%",
                    "Volume": format_large_number(result.volume),
                    "MarketCap": format_large_number(result.marketCap),
                    "52WeeksHigh": result.yearHigh,
                    "52WeeksLow": result.yearLow,
                    "Beta":result.beta,
                    "PERatio": result.pe,
                    "EPS": result.eps,      
                    "PayoutRatioTTM": result.payoutRatioTTM,
                    "DividendYieldTTM": RoundTheValue(result.dividendYielTTM),
                    "DividendPerShareTTM": result.dividendPerShareTTM,
                    "RevenueGrowthTTM": result.revenueGrowth,
                    "NetIncomeGrowth": result.netIncomeGrowth,
                    "FreeCashFlowTTM": result.freeCashFlowPerShareTTM,
                    "Sector": result.sector
                } 
                for result in results]
        
        return JSONResponse({
            "data": result,
            "total_pages": total_pages,
            "total_records": total,
            "current_pages": page
        })

@StockIdeaRouter.get("/stock/Search")
async def SearchSymbols(symbol: str):

    query = db.session.query(Symbols.Csymbol,Symbols.Cname).order_by(Symbols.Csymbol.asc())

    if symbol:
        query = query.filter(
            Symbols.Csymbol.ilike(f"%{symbol}%")            
        )

    results = query.all()
    if not results:
        return JSONResponse({"message": "Symbol Not Found!"})
    
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
    
    if range_type == "oneday":
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
                                    StockInfo.onedayvolatility,
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
                                    .filter(Symbols.Csymbol == symbol.upper()).order_by(Symbols.id.desc())

            result = [{
                        "Symbol": data.Csymbol,
                        "Name": data.Cname,
                        "Price": f"{round(data.price, 2)} USD",
                        "ChangePercentage": f"{data.changesPercentage}%",
                        "DayLow": data.dayLow,
                        "DayHigh": data.dayHigh,
                        "YearHigh": data.yearHigh,
                        "YearLow": data.yearLow,
                        "MarketCap": data.marketCap,
                        "SMA50": data.priceAvg50,
                        "SMA200": data.priceAvg200,
                        "Exchange": data.exchange,
                        "Volume": data.volume,
                        "AvgVolume": data.avgVolume,
                        "OpenPrice": data.open_price,
                        "PreviousClose": data.previousClose,
                        "EPS": data.eps,
                        "PE": data.pe,
                        "OneDayVolatility": data.onedayvolatility,
                        "Sector": data.sector,
                        "Description": data.description,
                        "Beta": data.beta,
                        "1D": data.one_day,
                        "5D": data.five_day,
                        "1M": data.one_month,
                        "3M": data.three_month,
                        "6M": data.six_month,
                        "YTD": data.ytd,
                        "1Y": data.one_year,
                        "DividendYieldTTM": data.dividendYielTTM,
                        "PayoutRatioTTM": data.payoutRatioTTM,
                        "CurrentRatioTTM": data.currentRatioTTM,
                        "QuickRatioTTM": data.quickRatioTTM,
                        "DebtRatioTTM": data.debtRatioTTM,
                        "DebtEquityRatioTTM": data.debtEquityRatioTTM,
                        "FreeCashFlowPerShareTTM": data.freeCashFlowPerShareTTM,
                        "PriceToBookRatioTTM": data.priceToBookRatioTTM,
                        "ProfitMarginsTTM":  data.netProfitMarginTTM,
                        "EarningGrowthTTM": data.priceEarningsRatioTTM, 
                        "NetIncomeGrowth": data.netIncomeGrowth,
                        "revenueGrowth": data.revenueGrowth,
                        "RSI": data.rsi
                    } for data in query]
        return JSONResponse({"graph_data": response.json(),"full_data":result})
    
    elif range_type == "oneweek":
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
                                    StockInfo.onedayvolatility,
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
                                    .filter(Symbols.Csymbol == symbol.upper()).order_by(Symbols.id.desc())

            result = [{
                        "Symbol": data.Csymbol,
                        "Name": data.Cname,
                        "Price": f"{round(data.price, 2)} USD",
                        "ChangePercentage": f"{data.changesPercentage}%",
                        "DayLow": data.dayLow,
                        "DayHigh": data.dayHigh,
                        "YearHigh": data.yearHigh,
                        "YearLow": data.yearLow,
                        "MarketCap": data.marketCap,
                        "SMA50": data.priceAvg50,
                        "SMA200": data.priceAvg200,
                        "Exchange": data.exchange,
                        "Volume": data.volume,
                        "AvgVolume": data.avgVolume,
                        "OpenPrice": data.open_price,
                        "PreviousClose": data.previousClose,
                        "EPS": data.eps,
                        "PE": data.pe,
                        "OneDayVolatility": data.onedayvolatility,
                        "Sector": data.sector,
                        "Description": data.description,
                        "Beta": data.beta,
                        "1D": data.one_day,
                        "5D": data.five_day,
                        "1M": data.one_month,
                        "3M": data.three_month,
                        "6M": data.six_month,
                        "YTD": data.ytd,
                        "1Y": data.one_year,
                        "DividendYieldTTM": data.dividendYielTTM,
                        "PayoutRatioTTM": data.payoutRatioTTM,
                        "CurrentRatioTTM": data.currentRatioTTM,
                        "QuickRatioTTM": data.quickRatioTTM,
                        "DebtRatioTTM": data.debtRatioTTM,
                        "DebtEquityRatioTTM": data.debtEquityRatioTTM,
                        "FreeCashFlowPerShareTTM": data.freeCashFlowPerShareTTM,
                        "PriceToBookRatioTTM": data.priceToBookRatioTTM,
                        "ProfitMarginsTTM":  data.netProfitMarginTTM,
                        "EarningGrowthTTM": data.priceEarningsRatioTTM, 
                        "NetIncomeGrowth": data.netIncomeGrowth,
                        "revenueGrowth": data.revenueGrowth,
                        "RSI": data.rsi
                    } for data in query]
        return JSONResponse({"graph_data": response.json(),"full_data":result})
    
    elif range_type == "onemonth":
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
                                    StockInfo.onedayvolatility,
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
                                    .filter(Symbols.Csymbol == symbol.upper()).order_by(Symbols.id.desc())

            result = [{
                        "Symbol": data.Csymbol,
                        "Name": data.Cname,
                        "Price": f"{round(data.price, 2)} USD",
                        "ChangePercentage": f"{data.changesPercentage}%",
                        "DayLow": data.dayLow,
                        "DayHigh": data.dayHigh,
                        "YearHigh": data.yearHigh,
                        "YearLow": data.yearLow,
                        "MarketCap": data.marketCap,
                        "SMA50": data.priceAvg50,
                        "SMA200": data.priceAvg200,
                        "Exchange": data.exchange,
                        "Volume": data.volume,
                        "AvgVolume": data.avgVolume,
                        "OpenPrice": data.open_price,
                        "PreviousClose": data.previousClose,
                        "EPS": data.eps,
                        "PE": data.pe,
                        "OneDayVolatility": data.onedayvolatility,
                        "Sector": data.sector,
                        "Description": data.description,
                        "Beta": data.beta,
                        "1D": data.one_day,
                        "5D": data.five_day,
                        "1M": data.one_month,
                        "3M": data.three_month,
                        "6M": data.six_month,
                        "YTD": data.ytd,
                        "1Y": data.one_year,
                        "DividendYieldTTM": data.dividendYielTTM,
                        "PayoutRatioTTM": data.payoutRatioTTM,
                        "CurrentRatioTTM": data.currentRatioTTM,
                        "QuickRatioTTM": data.quickRatioTTM,
                        "DebtRatioTTM": data.debtRatioTTM,
                        "DebtEquityRatioTTM": data.debtEquityRatioTTM,
                        "FreeCashFlowPerShareTTM": data.freeCashFlowPerShareTTM,
                        "PriceToBookRatioTTM": data.priceToBookRatioTTM,
                        "ProfitMarginsTTM":  data.netProfitMarginTTM,
                        "EarningGrowthTTM": data.priceEarningsRatioTTM, 
                        "NetIncomeGrowth": data.netIncomeGrowth,
                        "revenueGrowth": data.revenueGrowth,
                        "RSI": data.rsi
                    } for data in query]
        return JSONResponse({"graph_data": response.json(),"full_data":result})
       
    elif range_type == "oneyear":
        one_year = today - timedelta(days=365)
        params ={
            "from": one_year,
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
                                    StockInfo.onedayvolatility,
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
                                    .filter(Symbols.Csymbol == symbol.upper()).order_by(Symbols.id.desc())

            result = [{
                        "Symbol": data.Csymbol,
                        "Name": data.Cname,
                        "Price": f"{round(data.price, 2)} USD",
                        "ChangePercentage": f"{data.changesPercentage}%",
                        "DayLow": data.dayLow,
                        "DayHigh": data.dayHigh,
                        "YearHigh": data.yearHigh,
                        "YearLow": data.yearLow,
                        "MarketCap": data.marketCap,
                        "SMA50": data.priceAvg50,
                        "SMA200": data.priceAvg200,
                        "Exchange": data.exchange,
                        "Volume": data.volume,
                        "AvgVolume": data.avgVolume,
                        "OpenPrice": data.open_price,
                        "PreviousClose": data.previousClose,
                        "EPS": data.eps,
                        "PE": data.pe,
                        "OneDayVolatility": data.onedayvolatility,
                        "Sector": data.sector,
                        "Description": data.description,
                        "Beta": data.beta,
                        "1D": data.one_day,
                        "5D": data.five_day,
                        "1M": data.one_month,
                        "3M": data.three_month,
                        "6M": data.six_month,
                        "YTD": data.ytd,
                        "1Y": data.one_year,
                        "DividendYieldTTM": data.dividendYielTTM,
                        "PayoutRatioTTM": data.payoutRatioTTM,
                        "CurrentRatioTTM": data.currentRatioTTM,
                        "QuickRatioTTM": data.quickRatioTTM,
                        "DebtRatioTTM": data.debtRatioTTM,
                        "DebtEquityRatioTTM": data.debtEquityRatioTTM,
                        "FreeCashFlowPerShareTTM": data.freeCashFlowPerShareTTM,
                        "PriceToBookRatioTTM": data.priceToBookRatioTTM,
                        "ProfitMarginsTTM":  data.netProfitMarginTTM,
                        "EarningGrowthTTM": data.priceEarningsRatioTTM, 
                        "NetIncomeGrowth": data.netIncomeGrowth,
                        "revenueGrowth": data.revenueGrowth,
                        "RSI": data.rsi
                    } for data in query]
        return JSONResponse({"graph_data": response.json(),"full_data":result})
    
    elif range_type == "oneyear":
        one_year = today - timedelta(days=365)
        params ={
            "from": one_year,
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
                                    StockInfo.onedayvolatility,
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
                                    .filter(Symbols.Csymbol == symbol.upper()).order_by(Symbols.id.desc())

            result = [{
                        "Symbol": data.Csymbol,
                        "Name": data.Cname,
                        "Price": f"{round(data.price, 2)} USD",
                        "ChangePercentage": f"{data.changesPercentage}%",
                        "DayLow": data.dayLow,
                        "DayHigh": data.dayHigh,
                        "YearHigh": data.yearHigh,
                        "YearLow": data.yearLow,
                        "MarketCap": data.marketCap,
                        "SMA50": data.priceAvg50,
                        "SMA200": data.priceAvg200,
                        "Exchange": data.exchange,
                        "Volume": data.volume,
                        "AvgVolume": data.avgVolume,
                        "OpenPrice": data.open_price,
                        "PreviousClose": data.previousClose,
                        "EPS": data.eps,
                        "PE": data.pe,
                        "OneDayVolatility": data.onedayvolatility,
                        "Sector": data.sector,
                        "Description": data.description,
                        "Beta": data.beta,
                        "1D": data.one_day,
                        "5D": data.five_day,
                        "1M": data.one_month,
                        "3M": data.three_month,
                        "6M": data.six_month,
                        "YTD": data.ytd,
                        "1Y": data.one_year,
                        "DividendYieldTTM": data.dividendYielTTM,
                        "PayoutRatioTTM": data.payoutRatioTTM,
                        "CurrentRatioTTM": data.currentRatioTTM,
                        "QuickRatioTTM": data.quickRatioTTM,
                        "DebtRatioTTM": data.debtRatioTTM,
                        "DebtEquityRatioTTM": data.debtEquityRatioTTM,
                        "FreeCashFlowPerShareTTM": data.freeCashFlowPerShareTTM,
                        "PriceToBookRatioTTM": data.priceToBookRatioTTM,
                        "ProfitMarginsTTM":  data.netProfitMarginTTM,
                        "EarningGrowthTTM": data.priceEarningsRatioTTM, 
                        "NetIncomeGrowth": data.netIncomeGrowth,
                        "revenueGrowth": data.revenueGrowth,
                        "RSI": data.rsi
                    } for data in query]
        return JSONResponse({"graph_data": response.json(),"full_data":result})
