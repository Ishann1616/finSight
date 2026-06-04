from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base
from routers import auth
from models.transaction import Transaction
from models.user import User
from routers import transactions


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
 
@app.get("/")
def home():
    return {"message":"FinSight API is running"}

from routers import predictions 
app.include_router(predictions.router, prefix="/predict", tags=["Predictions"])
