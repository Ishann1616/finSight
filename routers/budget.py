from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import extract
from database import get_db
from models.budget import Budget
from models.transaction import Transaction
from datetime import datetime
from pydantic import BaseModel

router = APIRouter()

class BudgetCreate(BaseModel):
    category: str
    limit: float

@router.post("/")
def set_budget(budget: BudgetCreate, user_id:int =1, db: Session= Depends(get_db)):
    existing= db.query(Budget).filter(
        Budget.user_id == user_id,
        Budget.category == budget.category
    ).first()
    if existing:
        existing.limit= budget.limit
    else:
        db.add(Budget(user_id = user_id, category = budget.category,limit= budget.limit))
    db.commit()
    return {"message": f"Budget set for {budget.category}"}

@router.get("/alerts")
def get_alerts(user_id: int =1, db: Session = Depends(get_db)):
    budgets = db.query(Budget).filter(Budget.user_id==user_id).all()
    now =datetime.now()
    alerts=[]
    for b in budgets:
        transactions = db.query(Transaction).filter(
            Transaction.user_id == user_id,
            Transaction.category == b.category,
            extract('month', Transaction.created_at)== now.month,
            extract('year', Transaction.created_at) == now.year,
        ).all()
        spent = sum(t.amount for t in transactions)
        percent = round((spent/b.limit)*100,1)
        if percent >=100:
            alerts.append({"category": b.category, "status": "EXCEEDED", "percent":percent})
        elif percent >= 80:
            alerts.append({"category": b.category, "status": "WARNING", "percent": percent})
    return alerts
