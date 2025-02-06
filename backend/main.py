from fastapi import FastAPI,Response
from fastapi.responses import JSONResponse
from Routers.Stocks import router as StockRouter
from Routers.StockIdeas import StockIdeaRouter 
from fastapi_sqlalchemy import DBSessionMiddleware
import os
from Routers.Stocks import Myscheduler
import asyncio
from Models.StocksModels import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from alembic import command
from alembic.config import Config
from fastapi.middleware.cors import CORSMiddleware
from Routers.chatbot import ChatRouter
from Routers.Auth import AuthRouter

app = FastAPI()

#mysql middleware
DATABASE_URL = "mysql+mysqlconnector://root:@localhost/stocks"
app.add_middleware(DBSessionMiddleware, db_url=DATABASE_URL)

# Create engine
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def Create_table():
    Base.metadata.create_all(bind = engine)
Create_table()

# def run_migrations():
#     alembic_cfg = Config("alembic.ini")
#     command.upgrade(alembic_cfg, "head")

# run_migrations()


#routers
app.include_router(StockRouter,prefix='/Api',tags=["StockData"])
app.include_router(StockIdeaRouter,prefix='/api',tags=["StockIdeas"])
app.include_router(AuthRouter,prefix='/authapi',tags=["Auth"])
app.include_router(ChatRouter,prefix='/botapi',tags=["Chatbot"])

# # CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins (change to specific domains for security)
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)
@app.on_event("startup")
def startup_event():
    Myscheduler()

@app.get('/')
async def root():
    return JSONResponse(status_code=200,content={"message":"welcome to mysite"})
