from fastapi import FastAPI,Response
from fastapi.responses import JSONResponse
from Routers.Stocks import router as StockRouter
from Routers.StockIdeas import StockIdeaRouter 
from fastapi_sqlalchemy import DBSessionMiddleware
import os

app = FastAPI()
DATABASE_URL = "mysql+mysqlconnector://root:@localhost/stocks"
app.add_middleware(DBSessionMiddleware, db_url=DATABASE_URL)

app.include_router(StockRouter,prefix='/Api',tags=["StockData"])
app.include_router(StockIdeaRouter,prefix='/api',tags=["StockIdeas"])

@app.get('/')
async def root():
    return JSONResponse(status_code=200,content={"message":"welcome to mysite"})