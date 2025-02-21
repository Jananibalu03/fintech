from fastapi import APIRouter,HTTPException,Query, Depends
from fastapi.responses import JSONResponse
from models import Symbols, StockInfo, CompanyProfile, StockPerformance, FinancialMetrics, TechnicalIndicator, FinancialGrowth, StandardDeviation
from dotenv import load_dotenv
import os
import httpx
import time
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
import pytz
from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR
from sqlalchemy.orm import Session
from database import get_db
import  logging 
logging.basicConfig(
    level=logging.DEBUG,  # Set the logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
)
logger = logging.getLogger(__name__)

load_dotenv()
router = APIRouter()

Symbol_Base_URL = "https://financialmodelingprep.com/api/v3/stock/list"

Stock_Base_URL = "https://financialmodelingprep.com/api/v3/quote" 

Company_Base_URL = "https://financialmodelingprep.com/api/v3/profile"

Stock_Performance_URL = "https://financialmodelingprep.com/api/v3/stock-price-change"

Stock_Ratio_URL = "https://financialmodelingprep.com/api/v3/ratios-ttm"

RSI_Technical_URL = "https://financialmodelingprep.com/api/v3/technical_indicator/30min"

Intradata_URL = "https://financialmodelingprep.com/api/v3/historical-price-full"

FINANCIAL_GROWTH_URL = "https://financialmodelingprep.com/api/v3/financial-growth"

StandardDeviation_URL = "https://financialmodelingprep.com/api/v3/technical_indicator/30min"

Stock_Symbols = "https://financialmodelingprep.com/api/v3/stock-screener"

api_key = os.getenv("API_KEY")

@router.get("/UploadSymbols")
def Upload_Symbols(db: Session = Depends(get_db)):
    market_caps = [
        {"key": "marketCapMoreThan", "value": 1000000000},
        {"key": "marketCapLowerThan", "value": 1000000000},
        {"key": "betaLowerThan", "value": 0}
    ]
    try:
        exchanges = ["NYSE", 'NASDAQ']

        with httpx.Client() as r:
            for ticker in exchanges:
                for cap in market_caps:
                    params = {
                        cap['key']: cap['value'],
                        "exchange": ticker,
                        "apikey": api_key,
                        "limit": 50
                    }
                    response = r.get(Stock_Symbols, params=params)
                    data = response.json()
                    for record in data:
                        # Check if symbol already exists in the database
                        existing_symbol = db.query(Symbols).filter(Symbols.Csymbol == record['symbol']).first()

                        # If the key is 'betaLowerThan', check the beta value
                        if cap['key'] == "betaLowerThan":
                            if record.get("beta", 0) < cap['value']:  # Only process if beta is lower than the threshold
                                if existing_symbol:
                                    # If symbol exists, update the existing record
                                    existing_symbol.Cname = record['companyName']
                                    existing_symbol.exchange = record['exchangeShortName']
                                    db.commit()  # Commit the changes
                                    db.refresh(existing_symbol)  # Refresh the object to reflect updated values
                                else:
                                    # If symbol does not exist, create a new record
                                    SaveTickers = Symbols(
                                        Csymbol=record['symbol'],
                                        Cname=record['companyName'],
                                        exchange=record['exchangeShortName']
                                    )
                                    db.add(SaveTickers)
                                    db.commit()  # Commit the new record
                                    db.refresh(SaveTickers)  # Refresh the object to reflect new data
                        else:
                            # For other market cap filters, process normally
                            if existing_symbol:
                                # If symbol exists, update the existing record
                                existing_symbol.Cname = record['companyName']
                                existing_symbol.exchange = record['exchangeShortName']
                                db.commit()  # Commit the changes
                                db.refresh(existing_symbol)  # Refresh the object to reflect updated values
                            else:
                                # If symbol does not exist, create a new record
                                SaveTickers = Symbols(
                                    Csymbol=record['symbol'],
                                    Cname=record['companyName'],
                                    exchange=record['exchangeShortName']
                                )
                                db.add(SaveTickers)
                                db.commit()  # Commit the new record
                                db.refresh(SaveTickers)  # Refresh the object to reflect new data

        return JSONResponse(status_code=200, content={"message": "Data Successfully Inserted."})

    except Exception as e:
        return HTTPException(status_code=403,detail=f"An Error Occured! {e.args}")

@router.get("/UploadStocks") #--history required updated every 30 minutes per day
def Upload_Stocks(db: Session = Depends(get_db)):
    print("task1")
    params = {"apikey": os.getenv("API_KEY")}

    try:
        with httpx.Client() as r:
            # Fetch all existing stock symbols in a single query
            existing_symbols = {s.symbol: s for s in db.query(StockInfo).all()}

            # Fetch all stock data from API in a single request
            symbol_query = db.query(Symbols).all()

            for symbol in symbol_query:
                response = r.get(f"{Stock_Base_URL}/{symbol.Csymbol}", params=params, timeout=60)
                res = response.json()

                for data in res:
                    # stock_info = existing_symbols.get(data.get("symbol"))

                    # if not stock_info:  
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
                        date=datetime.now()
                    )

                    db.add(stock_data_list)
                    db.commit()
                    db.refresh(stock_data_list)
                
                    
            Technical_Indicator(db=db)
            time.sleep(30)
            Standard_deviation(db=db)
            print("task1 completed")

            return JSONResponse(status_code=200, content={"message": "Data Successfully Inserted."})
    except Exception as e:
        return HTTPException(status_code=403, detail=f"An Error Occurred! {e.args}")

@router.get("/UploadCompanyProfiles") #-- no history required update monthly once
def Upload_CompanyProfile(db: Session = Depends(get_db)):
    print("task2")
    params = {
        "apikey": os.getenv("API_KEY")
    }
    try:
        with httpx.Client() as r:
            symbol_query = db.query(Symbols).all()

            for symbol in symbol_query:
                response = r.get(f"{Company_Base_URL}/{symbol.Csymbol}", params = params,  timeout=60)
                res = response.json()
                for data in res:
                    symbol_id = db.query(CompanyProfile).filter(CompanyProfile.symbol==symbol.Csymbol).first()
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
                        db.add(company_profile_list)
                        db.commit()
                        db.refresh(company_profile_list)
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

                        db.commit()  
                        db.refresh(symbol_id)

            Upload_StocksPerformance(db=db)
            time.sleep(30)
            Upload_FinancialMetrics(db=db)
            time.sleep(30)
            upload_financial_growth(db=db)

            return JSONResponse(status_code=200,content={"message": "Data Successfully Inserted."})
    except Exception as e:
        raise HTTPException(status_code=403,detail=f"An Error Occured! {e.args}")
    
# @router.get("/UploadStocksPerformance") #-- no history required updated end of the every day
def Upload_StocksPerformance(db: Session = Depends(get_db)):
    print("task3")
    params = {
        "apikey": os.getenv("API_KEY")
    }
    try:
        with httpx.Client() as r:
            symbol_query = db.query(Symbols).all()

            for symbol in symbol_query:
                response = r.get(f"{Stock_Performance_URL}/{symbol.Csymbol}", params = params,  timeout=60)
                res = response.json()

                for data in res:
                    symbol_id = db.query(StockPerformance).filter(StockPerformance.symbol==symbol.Csymbol).first()
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
                                                                max_val=data.get("max")
                                                            )
                        db.add(Stock_performance_list)
                        db.commit()
                        db.refresh(Stock_performance_list)
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

                        db.commit()
                        db.refresh(symbol_id)

            return JSONResponse(status_code=200,content={"message": "Data Successfully Inserted."})
    except Exception as e:
        return HTTPException(status_code=403,detail=f"An Error Occured! {e.args}")
    
# @router.get("/UploadFinancialMetrics") #-- no history required update annualy/quartly 
def Upload_FinancialMetrics(db: Session = Depends(get_db)):
    print("task4")

    params = {
        "apikey": os.getenv("API_KEY")
    }
    try:
        with httpx.Client() as r:
            symbol_query = db.query(Symbols).all()


            for symbol in symbol_query:
                response = r.get(f"{Stock_Ratio_URL}/{symbol.Csymbol}", params = params,  timeout=60)
                res = response.json()

                for data in res:
                    symbol_id = db.query(FinancialMetrics).filter(FinancialMetrics.symbol==symbol.Csymbol).first()
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
                        db.add(financial_metrics_list)
                        db.commit()
                        db.refresh(financial_metrics_list)

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

                        db.commit()
                        db.refresh(symbol_id)
                            
            return JSONResponse(status_code=200,content={"message": "Data Successfully Inserted."})
    except Exception as e:
        return HTTPException(status_code=403,detail=f"An Error Occured! {e.args}")

# @router.get("/UploadTechnicalIndicator") #-- history required update every day 
def Technical_Indicator(db: Session = Depends(get_db)):
    print("task5")

    params = {
        "type": "rsi",
        "period": 10,
        "apikey": os.getenv("API_KEY")
    }
    try:
        with httpx.Client() as r:
            symbol_query = db.query(Symbols).all()

            for symbol in symbol_query:
                response = r.get(f"{RSI_Technical_URL}/{symbol.Csymbol}", params = params,  timeout=60)
                res = response.json()
                print(res)
                if res:
                    data = res[0]
                    formatted_date = datetime.strptime(data.get("date"), "%Y-%m-%d %H:%M:%S").date()
                    # symbol_id = db.query(TechnicalIndicator).filter(
                    #         TechnicalIndicator.date ==  formatted_date,
                    #         TechnicalIndicator.symbol == symbol.Csymbol
                    #     ).first()
                    
                    # if not symbol_id:
                    technical_indicator_list = TechnicalIndicator(
                        symbol = symbol.Csymbol,
                        date = formatted_date,
                        rsi = data.get("rsi")
                    )
                    db.add(technical_indicator_list)
                    db.commit()
                    db.refresh(technical_indicator_list)
                    # else:
                    #     symbol_id.date = formatted_date
                    #     symbol_id.rsi = data.get("rsi", symbol_id.rsi)
                    #     db.commit()
                    #     db.refresh(symbol_id)
            return JSONResponse(status_code=200,content={"message": "Data Successfully Inserted."})
    except Exception as e:
        return HTTPException(status_code=403,detail=f"An Error Occured! {e.args}")

# @router.get("/UploadFinancialGrowth") #-- history required updated annual/quartly 
def upload_financial_growth(db: Session = Depends(get_db)):
    print("task6")
    params = {
        "period": "annual",
        "apikey": os.getenv("API_KEY")
        }
    
    try:
        with httpx.Client() as client:
            symbols = db.query(Symbols).all()

            for symbol in symbols:
                response = client.get(f"{FINANCIAL_GROWTH_URL}/{symbol.Csymbol}", params=params, timeout=60)
                res = response.json()
                if res:
                    data = res[0]
                    formatted_date = datetime.strptime(data.get("date"), "%Y-%m-%d").date()
                    
                    existing_record = db.query(FinancialGrowth).filter(
                            FinancialGrowth.date == formatted_date,
                            FinancialGrowth.symbol == symbol.Csymbol
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
                        db.add(financial_growth_list)
                        db.commit()
                        db.refresh(financial_growth_list)
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

                        db.commit()
                        db.refresh(existing_record)
        
        return JSONResponse({"message": "Financial Growth Data Successfully Inserted."})
    except Exception as e:
        return HTTPException(status_code=403, detail=f"An Error Occurred! {e.args}")

# @router.get("/UploadStandardDeviation") #-- history required update every day
def Standard_deviation(db: Session = Depends(get_db)):
    print("task7")

    params = {
        "type": "standardDeviation",
        "period": 10,
        "apikey": os.getenv("API_KEY")
    }

    try:
        with httpx.Client() as r:
            symbol_query = db.query(Symbols).all()

            for symbol in symbol_query:
                response = r.get(f"{StandardDeviation_URL}/{symbol.Csymbol}", params = params,  timeout=60)

                res = response.json()
                if res:
                    data = res[0]
                    formatted_date = datetime.strptime(data.get("date"), "%Y-%m-%d %H:%M:%S").date()
                    # symbol_id = db.query(StandardDeviation).filter(
                    #         StandardDeviation.date ==  formatted_date,
                    #         StandardDeviation.symbol == symbol.Csymbol
                    #     ).first()
                    
                    # if not symbol_id:
                    standarddevation_list = StandardDeviation(
                        symbol = symbol.Csymbol,
                        date = formatted_date,
                        std = data.get("standardDeviation")
                    )
                    db.add(standarddevation_list)
                    db.commit()
                    db.refresh(standarddevation_list)
                    # else:
                    #     symbol_id.date = formatted_date
                    #     symbol_id.rsi = data.get("standardDeviation", symbol_id.std)
                    #     db.commit()
                    #     db.refresh(symbol_id)

            return JSONResponse(status_code=200,content={"message": "Data Successfully Inserted."})
    except Exception as e:
        return HTTPException(status_code=403,detail=f"An Error Occured! {e.args}")
    
# def Myscheduler():
#     scheduler = BackgroundScheduler(timezone=pytz.timezone('US/Eastern'))

#     # Define separate job chains for each sequence
#     job_chains = [
#         # Chain 1: Runs every 30 minutes between 9:30 AM and 4:30 PM
#         [
#             {"id": "my_task1", "func": Upload_Stocks, "trigger": CronTrigger(hour="20-23", minute="48", day_of_week="mon-fri", timezone='US/Eastern')},
#             {"id": "my_task5", "func": Technical_Indicator},
#             {"id": "my_task7", "func": Standard_devation}
#         ],
#         # Chain 2: Runs daily at 6 PM on weekdays
#         [
#             {"id": "my_task2", "func": Upload_CompanyProfile, "trigger": CronTrigger(hour="18", day_of_week="mon-fri", timezone='US/Eastern')},
#             {"id": "my_task3", "func": Upload_StocksPerformance},
#             {"id": "my_task4", "func": Upload_FinancialMetrics},
#             {"id": "my_task6", "func": upload_financial_growth}
#         ]
#     ]

#     def run_next_job(event):
#         """Triggers the next job in the chain after successful completion"""
#         if event.exception:
#             print(f"Job {event.job_id} failed! Skipping chain.")
#             return

#         # Find which chain and position the current job occupies
#         current_chain = None
#         current_index = None
#         for chain in job_chains:
#             current_index = next((i for i, job in enumerate(chain) if job["id"] == event.job_id), None)
#             if current_index is not None:
#                 current_chain = chain
#                 break

#         if current_chain is None or current_index is None:
#             return  # Job not part of any chain

#         # Schedule next job in the chain if exists
#         if current_index + 1 < len(current_chain):
#             next_job = current_chain[current_index + 1]
#             try:
#                 scheduler.add_job(
#                     next_job["func"],
#                     trigger='date',  # Run immediately
#                     id=next_job["id"],
#                     replace_existing=True,
#                     max_instances=1,
#                     coalesce=True,
#                     misfire_grace_time=60
#                 )
#                 print(f"Chain progression: Started {next_job['id']} after {event.job_id}")
#             except Exception as e:
#                 print(f"Error scheduling next job: {e}")

#     # Register event listener for job completion
#     scheduler.add_listener(run_next_job, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)

#     # Schedule the first job of each chain
#     for chain in job_chains:
#         first_job = chain[0]
#         scheduler.add_job(
#             first_job["func"],
#             trigger=first_job["trigger"],
#             id=first_job["id"],
#             replace_existing=True,
#             max_instances=1,
#             coalesce=True,
#             misfire_grace_time=60
#         )

#     scheduler.start()
#     print("Scheduler started with chained job execution.")

def Myscheduler():
    scheduler = BackgroundScheduler(timezone=pytz.timezone('US/Eastern'))

    # Register event listener for job completion and error
    def job_listener(event):
        """Log job completion and error events"""
        if event.exception:
            logger.error(f"Job {event.job_id} failed with exception: {event.exception}")
        else:
            logger.info(f"Job {event.job_id} completed successfully.")

    # Add listener to capture job execution results
    scheduler.add_listener(job_listener, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)

    # Schedule the first job of each chain (e.g., Upload_Stocks)
    scheduler.add_job(
        func=Upload_Stocks,  # Use func to specify the job function
        trigger=CronTrigger(hour="9-16", minute="*/40", day_of_week="mon-fri", timezone='US/Eastern'),
        id="task1",
        replace_existing=True,
        max_instances=1,
        coalesce=True,
        misfire_grace_time=60,
        args=[next(get_db())]  # Pass the database session as an argument
    )

    # Schedule the first job of each chain (e.g., Upload_Stocks)
    scheduler.add_job(
        func=Upload_CompanyProfile,  # Use func to specify the job function
        trigger=CronTrigger(hour="18", day_of_week="mon-fri", timezone='US/Eastern'),
        id="task2",
        replace_existing=True,
        max_instances=1,
        coalesce=True,
        misfire_grace_time=60,
        args=[next(get_db())]  # Pass the database session as an argument
    )

    # Start the scheduler
    scheduler.start()

    logger.info("Scheduler started with chained job execution.")