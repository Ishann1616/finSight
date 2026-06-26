from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.loan import Loan
from models.user import User
from routers.auth import get_current_user
from pydantic import BaseModel
from services.emi_calculator import calculate_emi

router= APIRouter(prefix="/loans", tags=["Loans"])

class LoanCreate(BaseModel):
    loan_type: str
    principal: float
    annual_rate: float
    tenure_months: int
    status: str = "active"

@router.post("/")
def create_loan(loan: LoanCreate, db: Session = Depends(get_db), current_user: User= Depends(get_current_user)):
    emi= calculate_emi(loan.principal, loan.annual_rate, loan.tenure_months)
    new_loan =Loan(
        user_id=current_user.id,
        loan_type=loan.loan_type,
        principal=loan.principal,
        annual_rate=loan.annual_rate,
        tenure_months=loan.tenure_months,
        status=loan.status 
    )
    db.add(new_loan)
    db.commit()
    db.refresh(new_loan)
    return{**new_loan.__dict__, "emi_details": emi}

@router.get("/")
def get_loan(db: Session = Depends(get_db), current_user: User= Depends(get_current_user)):
    return db.query(Loan).filter(Loan.user_id==current_user.id).all()

@router.delete("/{loan_id}")
def delete_loan(loan_id: int, db: Session = Depends(get_db), current_user: User= Depends(get_current_user)):
    loan= db.query(Loan).filter(Loan.id == loan_id, Loan.user_id == current_user,id).first()
    if not loan:
        raise HTTPException(status_code=404, detail="Loan not found")
    db.delete(loan)
    db.commit()
    return{"message":"Loan deleted"}

             
    

