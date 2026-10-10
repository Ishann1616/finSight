from collections import defaultdict
from datetime import datetime
from database import SessionLocal
from models.transaction import Transaction

NOT_ENOUGH = {
    "predicted_total": 0,
    "currency": "INR",
    "message": "Not enough history to forecast. Upload statements covering at least 2 full months.",
}

def _monthly_totals(user_id: int) -> dict:
    db = SessionLocal()
    try:
        rows = db.query(Transaction).filter(
            Transaction.user_id == user_id,
            Transaction.category != "Pass-Through",
        ).all()
    finally:
        db.close()

    totals = defaultdict(float)
    for t in rows:
        d = datetime.strptime(t.date, "%d%b,%Y")
        totals[(d.year, d.month)] += t.amount

    now = datetime.now()
    totals.pop((now.year, now.month), None)  # skip the in-progress month
    return dict(sorted(totals.items()))

def _weighted_avg(values: list) -> float:
    recent = values[-3:]
    weights = range(1, len(recent) + 1)  # latest month weighs most
    return sum(v * w for v, w in zip(recent, weights)) / sum(weights)

def get_forecast(user_id: int):
    values = list(_monthly_totals(user_id).values())
    if len(values) < 2:
        return NOT_ENOUGH
    return {"predicted_total": round(_weighted_avg(values), 2), "currency": "INR"}

def get_forecast_accuracy(user_id: int):
    values = list(_monthly_totals(user_id).values())
    if len(values) < 3:
        return {"actual": 0, "predicted": 0, "accuracy_percent": None, "currency": "INR"}
    actual = round(values[-1], 2)
    predicted = round(_weighted_avg(values[:-1]), 2)
    accuracy = round((1 - abs(actual - predicted) / actual) * 100, 2) if actual else None
    return {"actual": actual, "predicted": predicted, "accuracy_percent": accuracy, "currency": "INR"}