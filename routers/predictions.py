from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models.user import User
from services.forecaster import get_forecast, get_forecast_accuracy
from routers.auth import get_current_user

router = APIRouter()

@router.get("/next-months")
def next_month_prediction(current_user: User = Depends(get_current_user)):
    return get_forecast(current_user.id)

@router.get("/can-i-afford")
def can_i_afford(amount: float, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    forecast = get_forecast(current_user.id)
    predicted = forecast["predicted_total"]
    balance = current_user.current_balance if current_user.current_balance is not None else 0.0
    return calculate_affordability(amount, balance, predicted)

def calculate_affordability(amount: float, current_balance: float, predicted: float) -> dict:
    leftover = current_balance - predicted
    safety_buffer = current_balance * 0.20
    max_affordable = leftover - safety_buffer

    if amount <= max_affordable:
        answer = "Yes"
        reasoning = f"After your forecasted spend of ₹{predicted} and a 20% safety buffer, you can afford ₹{amount}"
    else:
        answer = "No"
        reasoning = f"₹{amount} exceeds what you can safely spend after forecasted expenses of ₹{predicted} and your buffer"

    return {
        "amount": amount,
        "answer": answer,
        "reasoning": reasoning,
        "predicted_monthly": predicted,
        "current_balance": current_balance,
        "max_affordable": round(max_affordable, 2)
    }

@router.get("/accuracy")
def forecast_accuracy(current_user: User = Depends(get_current_user)):
    return get_forecast_accuracy(current_user.id)