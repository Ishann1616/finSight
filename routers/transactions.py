from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from database import get_db
from models.transaction import Transaction
from models.user import User
from services.pdf_parser import parse_statement_pdf
from services.ml_categorizer import ml_categorize
from routers.auth import get_current_user
import shutil
import os
from datetime import datetime

router = APIRouter()

@router.post("/upload")
def upload_statement(file: UploadFile = File(...), db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    temp_path=f"temp_{file.filename}"
    with open(temp_path,"wb") as buffer:
        shutil.copyfileobj(file.file,buffer)
    
    transactions = parse_statement_pdf(temp_path)
    os.remove(temp_path)

    saved = 0
    for t in transactions:
        if t["direction"] == "credit":
            continue
        category = ml_categorize(t["merchant"])
        new_transaction = Transaction(
            user_id=current_user.id,
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
def get_transactions(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    transactions = db.query(Transaction).filter(Transaction.user_id == current_user.id).all()
    return transactions

def _parse(d: str):
    return datetime.strptime(d, "%d%b,%Y")

@router.get("/summary")
def get_summary(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    transactions = db.query(Transaction).filter(Transaction.user_id == current_user.id).all()
    if not transactions:
        return {}
    dated = [(_parse(t.date), t) for t in transactions]
    latest = max(d for d, _ in dated)
    summary = {}
    for d, t in dated:
        if (d.year, d.month) == (latest.year, latest.month):
            summary[t.category] = summary.get(t.category, 0) + t.amount
    return summary

@router.get("/latest-month")
def latest_month(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    rows = db.query(Transaction.date).filter(Transaction.user_id == current_user.id).all()
    if not rows:
        return {"label": None}
    latest = max(_parse(r[0]) for r in rows)
    return {"label": latest.strftime("%b %Y")}

@router.post("/backfill")
def backfill(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    from services.ml_categorizer import backfill_categories
    backfill_categories(current_user.id)
    return {"message": "Backfill complete"}