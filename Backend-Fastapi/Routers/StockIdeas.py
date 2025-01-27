from fastapi import APIRouter,HTTPException,Query
from Models.StocksModels import Symbols, StockInfo, StockPerformance, CompanyProfile
from fastapi_sqlalchemy import db
from fastapi.responses import JSONResponse
from typing import List, Optional
from sqlalchemy import or_, and_


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

@StockIdeaRouter.get("/stock/volatility")
async def Volatility(
    Search: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    limit: int = Query(10, le=100)
    ):
    skip = (page - 1) * limit
    query = db.session.query(CompanyProfile.image,Symbols.Csymbol,Symbols.Cname,StockInfo.onedayvolatility,StockInfo.price,StockInfo.changesPercentage,StockInfo.volume,StockInfo.marketCap,
                            CompanyProfile.beta,CompanyProfile.sector,StockInfo.priceAvg50,StockInfo.priceAvg200, 
                            StockPerformance.one_day,StockPerformance.one_month,StockPerformance.one_year).\
                            join(StockInfo,Symbols.Csymbol == StockInfo.symbol).\
                            join(StockPerformance, Symbols.Csymbol == StockPerformance.symbol).\
                            join(CompanyProfile, Symbols.Csymbol == CompanyProfile.symbol).order_by(StockInfo.price.desc())

    if Search:
        query = query.filter(
            or_(
                Symbols.Csymbol.ilike(f"%{Search}%"),
                Symbols.Cname.ilike(f"%{Search}%"),
                StockInfo.onedayvolatility.ilike(f"%{Search}%"),
                StockInfo.price.ilike(f"%{Search}%"),
                StockInfo.changesPercentage.ilike(f"%{Search}%"),
                StockInfo.volume.ilike(f"%{Search}%"),
                StockInfo.marketCap.ilike(f"%{Search}%"),
                CompanyProfile.beta.ilike(f"%{Search}%"),
                CompanyProfile.sector.ilike(f"%{Search}%")  

            )
        )
    
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
                "DividendYield": "213423", #----------------------------------------pending
                "RSI": "32534", #----------------------------------------pending
                "Sector": result.sector
              } 
              for result in results]

    return JSONResponse(result)



@StockIdeaRouter.get("/stock/52weekshigh")
async def YearHigh(
    Search: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    limit: int = Query(10, le=100)
    ):
    skip = (page - 1) * limit
    query = db.session.query(CompanyProfile.image,Symbols.Csymbol,Symbols.Cname,StockInfo.price,StockInfo.changesPercentage,StockInfo.volume,StockInfo.marketCap,
                            StockInfo.yearHigh,StockInfo.yearLow,CompanyProfile.beta,CompanyProfile.sector,StockInfo.priceAvg50,StockInfo.priceAvg200, 
                            StockPerformance.one_day,StockPerformance.one_month,StockPerformance.one_year).\
                            join(StockInfo,Symbols.Csymbol == StockInfo.symbol).\
                            join(StockPerformance, Symbols.Csymbol == StockPerformance.symbol).\
                            join(CompanyProfile, Symbols.Csymbol == CompanyProfile.symbol).order_by(StockInfo.price.desc())

    if Search:
        query = query.filter(
            or_(
                Symbols.Csymbol.ilike(f"%{Search}%"),
                Symbols.Cname.ilike(f"%{Search}%"),
                StockInfo.price.ilike(f"%{Search}%"),
                StockInfo.changesPercentage.ilike(f"%{Search}%"),
                StockInfo.volume.ilike(f"%{Search}%"),
                StockInfo.marketCap.ilike(f"%{Search}%"),
                CompanyProfile.beta.ilike(f"%{Search}%"),
                CompanyProfile.sector.ilike(f"%{Search}%")  

            )
        )
    # query = query.filter(StockInfo.price >= StockInfo.yearHigh)

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
                "RSI": "23414",#----------------------------------------------------pending
                "DividendYield": "213423", #----------------------------------------pending
                "Sector": result.sector
              } 
              for result in results]

    return JSONResponse(result)

@StockIdeaRouter.get("/stock/52weekslow")
async def YearLow(
    Search: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    limit: int = Query(10, le=100)
    ):
    skip = (page - 1) * limit
    query = db.session.query(CompanyProfile.image,Symbols.Csymbol,Symbols.Cname,StockInfo.price,StockInfo.changesPercentage,StockInfo.volume,StockInfo.marketCap,
                            StockInfo.yearHigh,StockInfo.yearLow,CompanyProfile.beta,CompanyProfile.sector,StockInfo.priceAvg50,StockInfo.priceAvg200, 
                            StockPerformance.one_day,StockPerformance.one_month,StockPerformance.one_year).\
                            join(StockInfo,Symbols.Csymbol == StockInfo.symbol).\
                            join(StockPerformance, Symbols.Csymbol == StockPerformance.symbol).\
                            join(CompanyProfile, Symbols.Csymbol == CompanyProfile.symbol).order_by(StockInfo.price.desc())

    if Search:
        query = query.filter(
            or_(
                Symbols.Csymbol.ilike(f"%{Search}%"),
                Symbols.Cname.ilike(f"%{Search}%"),
                StockInfo.price.ilike(f"%{Search}%"),
                StockInfo.changesPercentage.ilike(f"%{Search}%"),
                StockInfo.volume.ilike(f"%{Search}%"),
                StockInfo.marketCap.ilike(f"%{Search}%"),
                CompanyProfile.beta.ilike(f"%{Search}%"),
                CompanyProfile.sector.ilike(f"%{Search}%")  

            )
        )
    # query = query.filter(StockInfo.price <= StockInfo.yearLow)

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
                "RSI": "23414",#----------------------------------------------------pending
                "DividendYield": "213423", #----------------------------------------pending
                "Sector": result.sector
              } 
              for result in results]

    return JSONResponse(result)



@StockIdeaRouter.get("/stock/undertendollar")
async def UnderTen_Dollar(
    Search: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    limit: int = Query(10, le=100)
    ):
    skip = (page - 1) * limit
    query = db.session.query(CompanyProfile.image,Symbols.Csymbol,Symbols.Cname,StockInfo.price,StockInfo.onedayvolatility,StockInfo.changesPercentage,StockInfo.volume,StockInfo.marketCap,
                            StockInfo.pe,StockInfo.eps,StockInfo.yearHigh,StockInfo.yearLow,CompanyProfile.beta,CompanyProfile.sector,StockInfo.priceAvg50,StockInfo.priceAvg200, 
                            StockPerformance.one_day,StockPerformance.one_month,StockPerformance.one_year).\
                            join(StockInfo,Symbols.Csymbol == StockInfo.symbol).\
                            join(StockPerformance, Symbols.Csymbol == StockPerformance.symbol).\
                            join(CompanyProfile, Symbols.Csymbol == CompanyProfile.symbol).order_by(StockInfo.price.desc())
    query = query.filter(StockInfo.price <= 10)
    if Search:
        query = query.filter(
            or_(
                Symbols.Csymbol.ilike(f"%{Search}%"),
                Symbols.Cname.ilike(f"%{Search}%"),
                StockInfo.price.ilike(f"%{Search}%"),
                StockInfo.onedayvolatility.ilike(f"%{Search}%"),
                StockInfo.changesPercentage.ilike(f"%{Search}%"),
                StockInfo.volume.ilike(f"%{Search}%"),
                StockInfo.marketCap.ilike(f"%{Search}%"),
                CompanyProfile.beta.ilike(f"%{Search}%"),
                CompanyProfile.sector.ilike(f"%{Search}%")  

            )
        )
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
                "RSI": "23414",#----------------------------------------------------pending
                "PE_ratio": result.pe,
                "EPS": result.eps,
                "Sector": result.sector
              } 
              for result in results]

    return JSONResponse(result)


@StockIdeaRouter.get("/stock/abovetendoller")
async def AboveTen_Dollar(
    Search: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    limit: int = Query(10, le=100)
    ):
    skip = (page - 1) * limit
    query = db.session.query(CompanyProfile.image,Symbols.Csymbol,Symbols.Cname,StockInfo.price,StockInfo.onedayvolatility,StockInfo.changesPercentage,StockInfo.volume,StockInfo.marketCap,
                            StockInfo.pe,StockInfo.eps,StockInfo.yearHigh,StockInfo.yearLow,CompanyProfile.beta,CompanyProfile.sector,StockInfo.priceAvg50,StockInfo.priceAvg200, 
                            StockPerformance.one_day,StockPerformance.one_month,StockPerformance.one_year).\
                            join(StockInfo,Symbols.Csymbol == StockInfo.symbol).\
                            join(StockPerformance, Symbols.Csymbol == StockPerformance.symbol).\
                            join(CompanyProfile, Symbols.Csymbol == CompanyProfile.symbol).order_by(StockInfo.price.desc())
    query = query.filter(StockInfo.price >= 10)
    if Search:
        query = query.filter(
            or_(
                Symbols.Csymbol.ilike(f"%{Search}%"),
                Symbols.Cname.ilike(f"%{Search}%"),
                StockInfo.price.ilike(f"%{Search}%"),
                StockInfo.onedayvolatility.ilike(f"%{Search}%"),
                StockInfo.changesPercentage.ilike(f"%{Search}%"),
                StockInfo.volume.ilike(f"%{Search}%"),
                StockInfo.marketCap.ilike(f"%{Search}%"),
                CompanyProfile.beta.ilike(f"%{Search}%"),
                CompanyProfile.sector.ilike(f"%{Search}%")  

            )
        )
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
                "RSI": "23414",#----------------------------------------------------pending
                "PE_ratio": result.pe,
                "EPS": result.eps,
                "Sector": result.sector
              } 
              for result in results]

    return JSONResponse(result)


@StockIdeaRouter.get("/stock/negativebeta")
async def NegativeBeta(
    Search: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    limit: int = Query(10, le=100)
    ):
    skip = (page - 1) * limit
    query = db.session.query(CompanyProfile.image,Symbols.Csymbol,Symbols.Cname,StockInfo.price,StockInfo.onedayvolatility,StockInfo.changesPercentage,StockInfo.volume,StockInfo.marketCap,
                            StockInfo.pe,StockInfo.eps,StockInfo.yearHigh,StockInfo.yearLow,CompanyProfile.beta,CompanyProfile.sector,StockInfo.priceAvg50,StockInfo.priceAvg200, 
                            StockPerformance.one_day,StockPerformance.one_month,StockPerformance.one_year).\
                            join(StockInfo,Symbols.Csymbol == StockInfo.symbol).\
                            join(StockPerformance, Symbols.Csymbol == StockPerformance.symbol).\
                            join(CompanyProfile, Symbols.Csymbol == CompanyProfile.symbol).order_by(StockInfo.price.desc())
    query = query.filter(CompanyProfile.beta < 0)
    if Search:
        query = query.filter(
            or_(
                Symbols.Csymbol.ilike(f"%{Search}%"),
                Symbols.Cname.ilike(f"%{Search}%"),
                StockInfo.price.ilike(f"%{Search}%"),
                StockInfo.onedayvolatility.ilike(f"%{Search}%"),
                StockInfo.changesPercentage.ilike(f"%{Search}%"),
                StockInfo.volume.ilike(f"%{Search}%"),
                StockInfo.marketCap.ilike(f"%{Search}%"),
                CompanyProfile.beta.ilike(f"%{Search}%"),
                CompanyProfile.sector.ilike(f"%{Search}%")  

            )
        )
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
                "RSI": "23414",#----------------------------------------------------pending
                "Sector": result.sector
              } 
              for result in results]

    return JSONResponse(result)

@StockIdeaRouter.get("/stock/lowbeta")
async def LowBeta(
    Search: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    limit: int = Query(10, le=100)
    ):
    skip = (page - 1) * limit
    query = db.session.query(CompanyProfile.image,Symbols.Csymbol,Symbols.Cname,StockInfo.price,StockInfo.onedayvolatility,StockInfo.changesPercentage,StockInfo.volume,StockInfo.marketCap,
                            StockInfo.pe,StockInfo.eps,StockInfo.yearHigh,StockInfo.yearLow,CompanyProfile.beta,CompanyProfile.sector,StockInfo.priceAvg50,StockInfo.priceAvg200, 
                            StockPerformance.one_day,StockPerformance.one_month,StockPerformance.one_year).\
                            join(StockInfo,Symbols.Csymbol == StockInfo.symbol).\
                            join(StockPerformance, Symbols.Csymbol == StockPerformance.symbol).\
                            join(CompanyProfile, Symbols.Csymbol == CompanyProfile.symbol).order_by(StockInfo.price.desc())
    query = query.filter(CompanyProfile.beta < 1)
    if Search:
        query = query.filter(
            or_(
                Symbols.Csymbol.ilike(f"%{Search}%"),
                Symbols.Cname.ilike(f"%{Search}%"),
                StockInfo.price.ilike(f"%{Search}%"),
                StockInfo.onedayvolatility.ilike(f"%{Search}%"),
                StockInfo.changesPercentage.ilike(f"%{Search}%"),
                StockInfo.volume.ilike(f"%{Search}%"),
                StockInfo.marketCap.ilike(f"%{Search}%"),
                CompanyProfile.beta.ilike(f"%{Search}%"),
                CompanyProfile.sector.ilike(f"%{Search}%")  

            )
        )
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
                "RSI": "23414",#----------------------------------------------------pending
                "Sector": result.sector
              } 
              for result in results]

    return JSONResponse(result)


@StockIdeaRouter.get("/stock/highriskandreward")
async def HighRisk_Reward(
    Search: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    limit: int = Query(10, le=100)
    ):
    skip = (page - 1) * limit
    query = db.session.query(Symbols.Csymbol,Symbols.Cname,StockInfo.price,StockInfo.onedayvolatility,StockInfo.changesPercentage,StockInfo.volume,StockInfo.marketCap,
                            StockInfo.pe,StockInfo.eps,StockInfo.yearHigh,StockInfo.yearLow,CompanyProfile.beta,CompanyProfile.sector,StockInfo.priceAvg50,StockInfo.priceAvg200, 
                            StockPerformance.one_day,StockPerformance.one_month,StockPerformance.one_year).\
                            join(StockInfo,Symbols.Csymbol == StockInfo.symbol).\
                            join(StockPerformance, Symbols.Csymbol == StockPerformance.symbol).\
                            join(CompanyProfile, Symbols.Csymbol == CompanyProfile.symbol).order_by(StockInfo.price.desc())
    
     # Query for high-risk, high-reward stocks
    query = query.filter(
        or_(

            StockInfo.onedayvolatility > 5,  # Filter for high volatility, e.g., daily volatility > 5%
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
                StockInfo.price.ilike(f"%{Search}%"),
                StockInfo.onedayvolatility.ilike(f"%{Search}%"),
                StockInfo.changesPercentage.ilike(f"%{Search}%"),
                StockInfo.volume.ilike(f"%{Search}%"),
                StockInfo.marketCap.ilike(f"%{Search}%"),
                CompanyProfile.beta.ilike(f"%{Search}%"),
                CompanyProfile.sector.ilike(f"%{Search}%")  

            )
        )
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
                "RSI": "23414",#----------------------------------------------------pending
                "PE_ratio": result.pe,
                "PB_ratio": "pending", #----------------pending
                "EarningGrowth": "pending", #-----------------------pending
                "DebttoEquity": "pending", #--------------------------pending
                "RisktoReward_ratio": "pending", #-------------------------pending
                "DividendYield": "pending", #--------------------------pending
                "Sector": result.sector
              } 
              for result in results]

    return JSONResponse(result)


@StockIdeaRouter.get("/stock/debtfreestocks")
async def DebtFree_Stocks(
    Search: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    limit: int = Query(10, le=100)
    ):
    skip = (page - 1) * limit
    query = db.session.query(Symbols.Csymbol,Symbols.Cname,StockInfo.price,StockInfo.onedayvolatility,StockInfo.changesPercentage,StockInfo.volume,StockInfo.marketCap,
                            StockInfo.pe,StockInfo.eps,StockInfo.yearHigh,StockInfo.yearLow,CompanyProfile.beta,CompanyProfile.sector,StockInfo.priceAvg50,StockInfo.priceAvg200, 
                            StockPerformance.one_day,StockPerformance.one_month,StockPerformance.one_year).\
                            join(StockInfo,Symbols.Csymbol == StockInfo.symbol).\
                            join(StockPerformance, Symbols.Csymbol == StockPerformance.symbol).\
                            join(CompanyProfile, Symbols.Csymbol == CompanyProfile.symbol).order_by(StockInfo.price.desc())
    
    
    
    if Search:
        query = query.filter(
            or_(
                Symbols.Csymbol.ilike(f"%{Search}%"),
                Symbols.Cname.ilike(f"%{Search}%"),
                StockInfo.price.ilike(f"%{Search}%"),
                StockInfo.onedayvolatility.ilike(f"%{Search}%"),
                StockInfo.changesPercentage.ilike(f"%{Search}%"),
                StockInfo.volume.ilike(f"%{Search}%"),
                StockInfo.marketCap.ilike(f"%{Search}%"),
                CompanyProfile.beta.ilike(f"%{Search}%"),
                CompanyProfile.sector.ilike(f"%{Search}%")  

            )
        )
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
                # "52WeeksHigh": result.yearHigh,
                # "52WeeksLow": result.yearLow,
                # "SMA50": result.priceAvg50,
                # "SMA200": result.priceAvg200,
                "Beta":result.beta,
                "PE_ratio": result.pe,
                "CurrentRatio": "pending", #------------------pending
                "QuickRatio": "pending",
                "FreeCashFlow": "Pending",
                "ProfitMargins": "pending",
                "DividendPayoutRatio": "pending",
                "RevenueGrowth": "pending",
                "Sector": result.sector
              } 
              for result in results]

    return JSONResponse(result)


@StockIdeaRouter.get("/stock/dividend")
async def Dividend(
    Search: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    limit: int = Query(10, le=100)
    ):
    skip = (page - 1) * limit
    query = db.session.query(Symbols.Csymbol,Symbols.Cname,StockInfo.price,StockInfo.onedayvolatility,StockInfo.changesPercentage,StockInfo.volume,StockInfo.marketCap,
                            StockInfo.pe,StockInfo.eps,StockInfo.yearHigh,StockInfo.yearLow,CompanyProfile.beta,CompanyProfile.sector,StockInfo.priceAvg50,StockInfo.priceAvg200, 
                            StockPerformance.one_day,StockPerformance.one_month,StockPerformance.one_year).\
                            join(StockInfo,Symbols.Csymbol == StockInfo.symbol).\
                            join(StockPerformance, Symbols.Csymbol == StockPerformance.symbol).\
                            join(CompanyProfile, Symbols.Csymbol == CompanyProfile.symbol).order_by(StockInfo.price.desc())
    
    
    
    if Search:
        query = query.filter(
            or_(
                Symbols.Csymbol.ilike(f"%{Search}%"),
                Symbols.Cname.ilike(f"%{Search}%"),
                StockInfo.price.ilike(f"%{Search}%"),
                StockInfo.onedayvolatility.ilike(f"%{Search}%"),
                StockInfo.changesPercentage.ilike(f"%{Search}%"),
                StockInfo.volume.ilike(f"%{Search}%"),
                StockInfo.marketCap.ilike(f"%{Search}%"),
                CompanyProfile.beta.ilike(f"%{Search}%"),
                CompanyProfile.sector.ilike(f"%{Search}%")  

            )
        )
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
                # "52WeeksHigh": result.yearHigh,
                # "52WeeksLow": result.yearLow,
                # "SMA50": result.priceAvg50,
                # "SMA200": result.priceAvg200,
                "DividendYield": "Pending",
                "EPS": result.eps,
                "Beta":result.beta,
                "PE_ratio": result.pe,
                "FreeCashFlow": "Pending",
                "ProfitMargins": "pending",
                "DividendPayoutRatio": "pending",
                "RevenueGrowth": "pending",
                "Sector": result.sector
              } 
              for result in results]

    return JSONResponse(result)


@StockIdeaRouter.get("/stock/lowperatio")
async def LowPERatio(
    Search: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    limit: int = Query(10, le=100)
    ):
    skip = (page - 1) * limit
    query = db.session.query(Symbols.Csymbol,Symbols.Cname,StockInfo.price,StockInfo.onedayvolatility,StockInfo.changesPercentage,StockInfo.volume,StockInfo.marketCap,
                            StockInfo.pe,StockInfo.eps,StockInfo.yearHigh,StockInfo.yearLow,CompanyProfile.beta,CompanyProfile.sector,StockInfo.priceAvg50,StockInfo.priceAvg200, 
                            StockPerformance.one_day,StockPerformance.one_month,StockPerformance.one_year).\
                            join(StockInfo,Symbols.Csymbol == StockInfo.symbol).\
                            join(StockPerformance, Symbols.Csymbol == StockPerformance.symbol).\
                            join(CompanyProfile, Symbols.Csymbol == CompanyProfile.symbol).order_by(StockInfo.price.desc())
    
    
    
    if Search:
        query = query.filter(
            or_(
                Symbols.Csymbol.ilike(f"%{Search}%"),
                Symbols.Cname.ilike(f"%{Search}%"),
                StockInfo.price.ilike(f"%{Search}%"),
                StockInfo.onedayvolatility.ilike(f"%{Search}%"),
                StockInfo.changesPercentage.ilike(f"%{Search}%"),
                StockInfo.volume.ilike(f"%{Search}%"),
                StockInfo.marketCap.ilike(f"%{Search}%"),
                CompanyProfile.beta.ilike(f"%{Search}%"),
                CompanyProfile.sector.ilike(f"%{Search}%")  

            )
        )
    # query = query.filter(StockInfo.price <= StockInfo.yearLow)

    results = query.offset(skip).limit(limit).all()

    result =[{ 
                "Symbol": result.Csymbol,
                "Name": result.Cname,
                "Price": f"{round(result.price,2)} USD",
                "Change": f"{result.changesPercentage}%",
                # "1DVolatility": result.onedayvolatility,
                "Volume": format_large_number(result.volume),
                "MarketCap": format_large_number(result.marketCap),
                # "52WeeksHigh": result.yearHigh,
                # "52WeeksLow": result.yearLow,
                # "SMA50": result.priceAvg50,
                # "SMA200": result.priceAvg200,
                "Beta":result.beta,
                "PE_ratio": result.pe,
               
                "FreeCashFlow": "Pending",
                "ProfitMargins": "pending",
                "DividendPayoutRatio": "pending",
                "RevenueGrowth": "pending",
                "DebtToEquityRatio": "pending",
                "PriceToBookRatio": "pending",
                "ProfitMargin": "pending",

                "Sector": result.sector
              } 
              for result in results]

    return JSONResponse(result)


@StockIdeaRouter.get("/stock/todaytopgain")
async def TodayTopGain(
    Search: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    limit: int = Query(10, le=100)
    ):
    skip = (page - 1) * limit
    query = db.session.query(Symbols.Csymbol,Symbols.Cname,StockInfo.price,StockInfo.onedayvolatility,StockInfo.changesPercentage,StockInfo.volume,StockInfo.marketCap,
                            StockInfo.pe,StockInfo.eps,StockInfo.yearHigh,StockInfo.yearLow,CompanyProfile.beta,CompanyProfile.sector,StockInfo.priceAvg50,StockInfo.priceAvg200,StockInfo.dayHigh,StockInfo.dayLow,
                            StockPerformance.one_day,StockPerformance.one_month,StockPerformance.one_year).\
                            join(StockInfo,Symbols.Csymbol == StockInfo.symbol).\
                            join(StockPerformance, Symbols.Csymbol == StockPerformance.symbol).\
                            join(CompanyProfile, Symbols.Csymbol == CompanyProfile.symbol).order_by(StockInfo.price.desc())
    
    
    
    if Search:
        query = query.filter(
            or_(
                Symbols.Csymbol.ilike(f"%{Search}%"),
                Symbols.Cname.ilike(f"%{Search}%"),
                StockInfo.price.ilike(f"%{Search}%"),
                StockInfo.onedayvolatility.ilike(f"%{Search}%"),
                StockInfo.changesPercentage.ilike(f"%{Search}%"),
                StockInfo.volume.ilike(f"%{Search}%"),
                StockInfo.marketCap.ilike(f"%{Search}%"),
                CompanyProfile.beta.ilike(f"%{Search}%"),
                CompanyProfile.sector.ilike(f"%{Search}%")  

            )
        )
    # query = query.filter(StockInfo.price <= StockInfo.yearLow)

    results = query.offset(skip).limit(limit).all()

    result =[{ 
                "Symbol": result.Csymbol,
                "Name": result.Cname,
                "Price": f"{round(result.price,2)} USD",
                "Change": f"{result.changesPercentage}%",
                # "1DVolatility": result.onedayvolatility,
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
                "RSI": "pending",
                "FreeCashFlow": "Pending",
                "ProfitMargins": "pending",
                "DividendPayoutRatio": "pending",
                "RevenueGrowth": "pending",
                "Sector": result.sector
              } 
              for result in results]

    return JSONResponse(result)


@StockIdeaRouter.get("/stock/todaytoploss")
async def TodayTopLoss(
    Search: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    limit: int = Query(10, le=100)
    ):
    skip = (page - 1) * limit
    query = db.session.query(Symbols.Csymbol,Symbols.Cname,StockInfo.price,StockInfo.onedayvolatility,StockInfo.changesPercentage,StockInfo.volume,StockInfo.marketCap,
                            StockInfo.pe,StockInfo.eps,StockInfo.yearHigh,StockInfo.yearLow,CompanyProfile.beta,CompanyProfile.sector,StockInfo.priceAvg50,StockInfo.priceAvg200,StockInfo.dayHigh,StockInfo.dayLow,
                            StockPerformance.one_day,StockPerformance.one_month,StockPerformance.one_year).\
                            join(StockInfo,Symbols.Csymbol == StockInfo.symbol).\
                            join(StockPerformance, Symbols.Csymbol == StockPerformance.symbol).\
                            join(CompanyProfile, Symbols.Csymbol == CompanyProfile.symbol).order_by(StockInfo.price.desc())
    
    
    
    if Search:
        query = query.filter(
            or_(
                Symbols.Csymbol.ilike(f"%{Search}%"),
                Symbols.Cname.ilike(f"%{Search}%"),
                StockInfo.price.ilike(f"%{Search}%"),
                StockInfo.onedayvolatility.ilike(f"%{Search}%"),
                StockInfo.changesPercentage.ilike(f"%{Search}%"),
                StockInfo.volume.ilike(f"%{Search}%"),
                StockInfo.marketCap.ilike(f"%{Search}%"),
                CompanyProfile.beta.ilike(f"%{Search}%"),
                CompanyProfile.sector.ilike(f"%{Search}%")  

            )
        )
    # query = query.filter(StockInfo.price <= StockInfo.yearLow)

    results = query.offset(skip).limit(limit).all()

    result =[{ 
                "Symbol": result.Csymbol,
                "Name": result.Cname,
                "Price": f"{round(result.price,2)} USD",
                "Change": f"{result.changesPercentage}%",
                # "1DVolatility": result.onedayvolatility,
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
                "RSI": "pending",
                "FreeCashFlow": "Pending",
                "ProfitMargins": "pending",
                "DividendPayoutRatio": "pending",
                "RevenueGrowth": "pending",
                "Sector": result.sector
              } 
              for result in results]

    return JSONResponse(result)


@StockIdeaRouter.get("/stock/topperformance")
async def TopPerformance(
    Search: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    limit: int = Query(10, le=100)
    ):
    skip = (page - 1) * limit
    query = db.session.query(Symbols.Csymbol,Symbols.Cname,StockInfo.price,StockInfo.onedayvolatility,StockInfo.changesPercentage,StockInfo.volume,StockInfo.marketCap,
                            StockInfo.pe,StockInfo.eps,StockInfo.yearHigh,StockInfo.yearLow,CompanyProfile.beta,CompanyProfile.sector,StockInfo.priceAvg50,StockInfo.priceAvg200,StockInfo.dayHigh,StockInfo.dayLow,
                            StockPerformance.one_day,StockPerformance.one_month,StockPerformance.one_year).\
                            join(StockInfo,Symbols.Csymbol == StockInfo.symbol).\
                            join(StockPerformance, Symbols.Csymbol == StockPerformance.symbol).\
                            join(CompanyProfile, Symbols.Csymbol == CompanyProfile.symbol).order_by(StockInfo.price.desc())
    
    
    
    if Search:
        query = query.filter(
            or_(
                Symbols.Csymbol.ilike(f"%{Search}%"),
                Symbols.Cname.ilike(f"%{Search}%"),
                StockInfo.price.ilike(f"%{Search}%"),
                StockInfo.onedayvolatility.ilike(f"%{Search}%"),
                StockInfo.changesPercentage.ilike(f"%{Search}%"),
                StockInfo.volume.ilike(f"%{Search}%"),
                StockInfo.marketCap.ilike(f"%{Search}%"),
                CompanyProfile.beta.ilike(f"%{Search}%"),
                CompanyProfile.sector.ilike(f"%{Search}%")  

            )
        )
    # query = query.filter(StockInfo.price <= StockInfo.yearLow)

    results = query.offset(skip).limit(limit).all()

    result =[{ 
                "Symbol": result.Csymbol,
                "Name": result.Cname,
                "Price": f"{round(result.price,2)} USD",
                "Change": f"{result.changesPercentage}%",
                # "1DVolatility": result.onedayvolatility,
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

                "RSI": "pending",
                "FreeCashFlow": "Pending",
                "ProfitMargins": "pending",
                "DividendYield": "pending",
                "RevenueGrowth": "pending",
                "Sector": result.sector
              } 
              for result in results]

    return JSONResponse(result)



@StockIdeaRouter.get("/stock/highdividendyield")
async def HighDividendYield(
    Search: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    limit: int = Query(10, le=100)
    ):
    skip = (page - 1) * limit
    query = db.session.query(Symbols.Csymbol,Symbols.Cname,StockInfo.price,StockInfo.onedayvolatility,StockInfo.changesPercentage,StockInfo.volume,StockInfo.marketCap,
                            StockInfo.pe,StockInfo.eps,StockInfo.yearHigh,StockInfo.yearLow,CompanyProfile.beta,CompanyProfile.sector,StockInfo.priceAvg50,StockInfo.priceAvg200,StockInfo.dayHigh,StockInfo.dayLow,
                            StockPerformance.one_day,StockPerformance.one_month,StockPerformance.one_year).\
                            join(StockInfo,Symbols.Csymbol == StockInfo.symbol).\
                            join(StockPerformance, Symbols.Csymbol == StockPerformance.symbol).\
                            join(CompanyProfile, Symbols.Csymbol == CompanyProfile.symbol).order_by(StockInfo.price.desc())
    
    
    
    if Search:
        query = query.filter(
            or_(
                Symbols.Csymbol.ilike(f"%{Search}%"),
                Symbols.Cname.ilike(f"%{Search}%"),
                StockInfo.price.ilike(f"%{Search}%"),
                StockInfo.onedayvolatility.ilike(f"%{Search}%"),
                StockInfo.changesPercentage.ilike(f"%{Search}%"),
                StockInfo.volume.ilike(f"%{Search}%"),
                StockInfo.marketCap.ilike(f"%{Search}%"),
                CompanyProfile.beta.ilike(f"%{Search}%"),
                CompanyProfile.sector.ilike(f"%{Search}%")  

            )
        )
    # query = query.filter(StockInfo.price <= StockInfo.yearLow)

    results = query.offset(skip).limit(limit).all()

    result =[{ 
                "Symbol": result.Csymbol,
                "Name": result.Cname,
                "Price": f"{round(result.price,2)} USD",
                "Change": f"{result.changesPercentage}%",
                # "1DVolatility": result.onedayvolatility,
                "Volume": format_large_number(result.volume),
                "MarketCap": format_large_number(result.marketCap),
                # "DayHigh": result.dayHigh,
                # "DayLow": result.dayLow,
                # "1D": result.one_day,
                # "1M": result.one_month,
                # "1Y": result.one_year,
                "52WeeksHigh": result.yearHigh,
                "52WeeksLow": result.yearLow,
                # "SMA50": result.priceAvg50,
                # "SMA200": result.priceAvg200,
                "Beta":result.beta,
                "PERatio": result.pe,
                "EPS": result.eps,      
                "PayoutRatio": "pending",
                "DividendYield": "pending",
                "DividendPerShare": "pending",
                "RevenueGrowth": "pending",
                "NetIncomeGrowth": "pending",
                "FreeCashFlow": "pending",
                "Sector": result.sector
              } 
              for result in results]

    return JSONResponse(result)
