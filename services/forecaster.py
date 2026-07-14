from prophet import Prophet
import pandas as pd
from database import SessionLocal
from models.transaction import Transaction
from datetime import datetime
from sqlalchemy import extract

def get_forecast(user_id: int):
    db= SessionLocal()
    transactions= db.query(Transaction).filter(
        Transaction.user_id == user_id
    ).all()
    db.close()

    data = [
    {"ds": t.date, "y": t.amount}
    for t in transactions
    if t.category!= "Pass-Through"
    ]       
    df =pd.DataFrame(data)
    df['ds']= pd.to_datetime(df['ds'], format='%d%b,%Y')    
    df= df.groupby('ds')['y'].sum().reset_index()

    print(df)
    print(df.describe())

    model= Prophet()
    model.fit(df)

    future= model.make_future_dataframe(periods=30)
    forecast= model.predict(future)

    next_month = forecast[['ds','yhat']].tail(30)
    total = round(next_month['yhat'].sum(),2)

    return{
        "predicted_total": total,
        "currency": "INR"
    }

def get_forecast_accuracy(user_id: int):
    db = SessionLocal()
    now = datetime.now()
    last_month = now.month - 1 if now.month > 1 else 12
    last_month_year = now.year if now.month > 1 else now.year - 1

    transactions = db.query(Transaction).filter(
        Transaction.user_id == user_id,
        Transaction.category != "Pass-Through",
        extract('month', Transaction.created_at) == last_month,
        extract('year', Transaction.created_at) == last_month_year
    ).all()
    db.close()

    actual = round(sum(t.amount for t in transactions), 2)
    predicted = get_forecast(user_id)["predicted_total"]
    accuracy = round((1- abs(actual- predicted)/actual)*100, 2)

    return{
        "actual": actual,
        "predicted": predicted,
        "accuracy_percent": accuracy,
        "currency": "INR"
    }