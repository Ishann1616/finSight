from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from database import get_db
from models.transaction import Transaction
from services.pdf_parser import parse_statement_pdf
from services.categorizer import categorize
from services.ml_categorizer import ml_categorize
import shutil
import os

router = APIRouter()

@router.post("/upload")
def upload_statement(file: UploadFile = File(...), user_id:int =1,db: Session = Depends(get_db)):
    temp_path=f"temp_{file.filename}"
    with open(temp_path,"wb") as buffer:
        shutil.copyfileobj(file.file,buffer)
    
    transactions = parse_statement_pdf(temp_path)
    os.remove(temp_path)

    saved = 0
    for t in transactions:
        category = ml_categorize(t["merchant"])
        new_transaction = Transaction(
            user_id=user_id,
            merchant=t["merchant"],
            amount=t["amount"],
            category=category,
            date=t["date"],
            payment_method=t["payment_method"]
        )
        db.add(new_transaction)
        saved += 1

    db.commit()
    return {"message": f"Successfully saved {saved} transactions"}

@router.get("/")
def get_transactions(user_id: int = 1, db: Session = Depends(get_db)):
    transactions = db.query(Transaction).filter(Transaction.user_id == user_id).all()
    return transactions

@router.get("/summary")
def get_summary(user_id: int = 1, db: Session = Depends(get_db)):
    transactions = db.query(Transaction).filter(Transaction.user_id == user_id).all()
    summary = {}
    for t in transactions:
        if t.category not in summary:
            summary[t.category] = 0
        summary[t.category] += t.amount
    return summary
