from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base
from routers import auth
from models.transaction import Transaction
from models.user import User
from routers import transactions
from agent import routes as agent_routes
from models.conversation import Conversation
from routers import sip 

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(transactions.router, prefix="/transactions", tags=["Transactions"])
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(agent_routes.router, prefix="/agent", tags=["Agent"])
app.include_router(sip.router)

@app.get("/")
def home():
    return {"message":"FinSight API is running"}

from routers import predictions 
app.include_router(predictions.router, prefix="/predict", tags=["Predictions"])
