from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from services.forecaster import get_forecast

router = APIRouter()

@router.get("/next-months")
def next_month_prediction(user_id: int=1):
    forecast=get_forecast(user_id)
    return forecast

@router.get("/can-i-afford")
def can_i_afford(amount: float,user_id: int=1):
    forecast=get_forecast(user_id)
    predicted= forecast["predicted_total"]
    average_monthly= predicted/30*30

    if amount < (average_monthly * 0.2):
        answer = "Yes"
        reasoning = f"₹{amount} is within your budget buffer"
    else:
        answer = "No"
        reasoning = f"₹{amount} would strain your predicted monthly spend of ₹{predicted}"


    return {
            "amount": amount,
            "answer": answer,
            "reasoning": reasoning,
            "predicted_monthly": predicted
    }