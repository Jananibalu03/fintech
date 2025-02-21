from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from database import engine
from models import Base
from Routers.Stocks import Myscheduler
from Routers.Stocks import router as StockRouter
from Routers.Stockideas import StockIdeaRouter 
from Routers.Chatbot import ChatRouter
from Routers.Auth import AuthRouter

try:
    print("Creating tables...")
    Base.metadata.create_all(bind=engine)
    print("Table created")
except Exception as e:
    print("Error creating tables:", e)

app = FastAPI()


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
def root():
    return JSONResponse(status_code=200,content={"message":"welcome to mysite"})
