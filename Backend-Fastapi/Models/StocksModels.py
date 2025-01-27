from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Text, Float, BigInteger, Date, Boolean

Base = declarative_base()

class Symbols(Base):
    __tablename__ = "symbol"
    id = Column(Integer, primary_key=True, index=True)
    Csymbol = Column(String(150))
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
    onedayvolatility = Column(String(100))
    timestamp = Column(BigInteger)

class CompanyProfile(Base):
    __tablename__ = "companyprofile"

    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String(10), nullable=False)
    price = Column(Float)
    beta = Column(Float)
    volAvg = Column(BigInteger)
    mktCap = Column(BigInteger)
    lastDiv = Column(Float)
    price_range = Column(String(255))
    changes = Column(Float)
    companyName = Column(String(255))
    currency = Column(String(10))
    cik = Column(String(20))
    isin = Column(String(20))
    cusip = Column(String(20))
    exchange = Column(String(100))
    exchangeShortName = Column(String(50))
    industry = Column(String(100))
    website = Column(String(255))
    description = Column(Text)
    ceo = Column(String(100))
    sector = Column(String(50))
    country = Column(String(50))
    fullTimeEmployees = Column(Integer)
    phone = Column(String(50))
    address = Column(Text)
    city = Column(String(50))
    state = Column(String(50))
    zip_code = Column(String(20))
    dcfDiff = Column(Float)
    dcf = Column(Float)
    image = Column(String(255))
    ipoDate = Column(Date)
    defaultImage = Column(Boolean)
    isEtf = Column(Boolean)
    isActivelyTrading = Column(Boolean)
    isAdr = Column(Boolean)
    isFund = Column(Boolean)


class StockPerformance(Base):
    __tablename__ = 'stockperformance'
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    symbol = Column(String(10), nullable=False, unique=True)
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

