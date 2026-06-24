from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.sip_plan import SIPPlan
from models.user import User
from routers.auth import get_current_user
from pydantic import BaseModel

router = APIRouter(prefix="/sip", tags=["SIP"])

class SIPCreate (BaseModel):
    fund_name: str
    amount: float
    due_date: int
    frequency: str ="monthly"
    status: str = "active"

@router.post("/")
def creat_sip(sip: SIPCreate, db: Session = Depends(get_db),current_user:User = Depends(get_current_user)):
    new_sip = SIPPlan(
        user_id= current_user.id,
        fund_name= sip.fund_name,
        amount=sip.amount,
        due_date=sip.due_date,
        frequency=sip.frequency,
        status= sip.status
    )
    db.add(new_sip)
    db.commit()
    db.refresh(new_sip)
    return new_sip

@router.get("/")
def get_sips(db: Session = Depends(get_db),current_user:User = Depends(get_current_user)):
    return db.query(SIPPlan).filter(SIPPlan.user_id == current_user.id).all()
