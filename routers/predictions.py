from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models.user import User
from services.forecaster import get_forecast

router = APIRouter()

@router.get("/next-months")
def next_month_prediction(user_id: int=1):
    forecast=get_forecast(user_id)
    return forecast

@router.get("/can-i-afford")
def can_i_afford(amount: float,user_id: int=1,db: Session = Depends(get_db)):
    user= db.query(User).filter(User.id == user_id).first()
    forecast=get_forecast(user_id)
    predicted= forecast["predicted_total"]
    balance = user.current_balance if user.current_balance is not None else 0.0

    return calculate_affordability(amount, balance, predicted)

def calculate_affordability(amount: float, current_balance: float, predicted: float)-> dict:
    leftover= current_balance-predicted
    safety_buffer= current_balance * 0.20
    max_affordable= leftover-safety_buffer

    if amount<= max_affordable:
        answer = "Yes"
        reasoning =f"After your forecasted spend of ₹{predicted} and a 20% safety buffer, you can afford ₹{amount} "
    else:
        answer = "No"
        reasoning =f" ₹{amount} exceeds what you can safety spend after forecasted expenses of ₹{predicted}and your buffer "

    return{
        "amount": amount,
        "answer": answer,
        "reasoning": reasoning,
        "predicted_monthly": predicted,
        "current_balance": current_balance,
        "max_affordable": round(max_affordable, 2) 
    }


