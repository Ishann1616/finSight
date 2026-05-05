from fastapi import FastAPI
from database import engine, Base
from routers import auth
from models.transaction import Transaction
from models.user import User

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
 
@app.get("/")
def home():
    return {"message":"FinSight API is running"}