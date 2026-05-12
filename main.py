from fastapi import FastAPI
from database import engine, Base
from routers import auth
from models.transaction import Transaction
from models.user import User
from routers import transactions


Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(transactions.router, prefix="/transactions", tags=["Transactions"])
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
 
@app.get("/")
def home():
    return {"message":"FinSight API is running"}

from routers import predictions 
app.include_router(predictions.router, prefix="/predict", tags=["Predictions"])
