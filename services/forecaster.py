from prophet import Prophet
import pandas as pd
from database import SessionLocal
from models.transaction import Transaction

def get_forecast(user_id: int):
    db= SessionLocal()
    transactions= db.query(Transaction).filter(
        Transaction.user_id == user_id
    ).all()
    db.close()

    data = [
    {"ds": t.date, "y": t.amount}
    for t in transactions
    if "MONEYWISE" not in t.merchant.upper()
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