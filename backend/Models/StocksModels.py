from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Text, Float, BigInteger, Date, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship

Base = declarative_base()

class Symbols(Base):
    __tablename__ = "symbol"
    id = Column(Integer, primary_key=True, index=True)
    Csymbol = Column(String(150), unique=True, nullable=False)
    Cname = Column(String(255))
    exchange = Column(String(150))


class StockInfo(Base):
    __tablename__ = "stockinfo"

    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String(20), nullable=False)
    name = Column(String(255), nullable=False)
    price = Column(Float)
    changesPercentage = Column(Float)
    change = Column(Float)
    dayLow = Column(Float)
    dayHigh = Column(Float)
    yearHigh = Column(Float)
    yearLow = Column(Float)
    marketCap = Column(BigInteger)
    priceAvg50 = Column(Float)
    priceAvg200 = Column(Float)
    exchange = Column(String(50))
    volume = Column(BigInteger)
    avgVolume = Column(BigInteger)
    open_price = Column(Float)
    previousClose = Column(Float)
    eps = Column(Float)
    pe = Column(Float)
    # onedayvolatility = Column(String(100))
    timestamp = Column(Date)

class CompanyProfile(Base):
    __tablename__ = "companyprofile"

    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String(20), nullable=False)
    beta = Column(Float)
    lastDiv = Column(Float)
    companyName = Column(String(255))
    industry = Column(String(100))
    website = Column(String(255))
    description = Column(Text)
    sector = Column(String(50))
    country = Column(String(50))
    phone = Column(String(50))
    address = Column(Text)
    city = Column(String(50))
    state = Column(String(50))
    zip_code = Column(String(20))
    ipoDate = Column(String(50))


class StockPerformance(Base):
    __tablename__ = 'stockperformance'
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    symbol = Column(String(20), nullable=False, unique=True)
    one_day = Column(Float)
    five_day = Column(Float)
    one_month = Column(Float)
    three_month = Column( Float)
    six_month = Column(Float)
    ytd = Column(Float)  
    one_year = Column( Float)
    three_year = Column(Float)
    five_year = Column(Float)
    ten_year = Column(Float)
    max_val = Column(Float)

class FinancialMetrics(Base):
    __tablename__ = 'financialmetrics'

    id = Column(Integer, primary_key=True, autoincrement=True)
    symbol = Column(String(20), nullable=False, unique=True)
    dividendYielTTM = Column(Float)
    dividendYielPercentageTTM = Column(Float)
    payoutRatioTTM = Column(Float)
    currentRatioTTM = Column(Float)
    quickRatioTTM = Column(Float)
    grossProfitMarginTTM = Column(Float)
    netProfitMarginTTM = Column(Float)
    debtRatioTTM = Column(Float)
    debtEquityRatioTTM = Column(Float)
    cashFlowToDebtRatioTTM = Column(Float)
    freeCashFlowPerShareTTM = Column(Float)
    cashPerShareTTM = Column(Float)
    priceBookValueRatioTTM = Column(Float)
    priceToBookRatioTTM = Column(Float)
    priceEarningsRatioTTM = Column(Float)
    dividendPerShareTTM = Column(Float)

class TechnicalIndicator(Base):
    __tablename__ = "rsitechnicalindicator"

    id = Column(Integer, primary_key=True, autoincrement=True)
    symbol = Column(String(20))
    date = Column(Date)
    rsi = Column(Float)

class FinancialGrowth(Base):
    __tablename__ = "financialgrowth"

    id = Column(Integer, primary_key=True, autoincrement=True)
    symbol = Column(String(20))
    date = Column(Date)
    calendarYear = Column(String(10))
    period = Column(String(10))
    revenueGrowth = Column(Float)
    grossProfitGrowth = Column(Float)
    ebitgrowth = Column(Float)
    operatingIncomeGrowth = Column(Float)
    netIncomeGrowth = Column(Float)
    epsgrowth = Column(Float)
   
class StandardDeviation(Base):
    __tablename__ = "standarddevation"

    id = Column(Integer, primary_key=True, autoincrement=True)
    symbol = Column(String(20))
    date = Column(Date)
    std = Column(Float)
