from langchain.tools import tool
from sqlalchemy import func
from database import SessionLocal
from models.transaction import Transaction
from agent.vector_store import search_transactions


def get_db():
    return SessionLocal()

@tool
def get_spending_summary(user_id: int)-> str:
    """Get total spending grouped by category for a user.
    Use this when the iser asks where their money goes,
    spending habits , or category breakdown."""
    db = get_db()
    try:
        result= db.query(
            Transaction.category,
            func.sum(Transaction.amount).label("total")
        ).filter(
            Transaction.user_id== user_id
        ).group_by(Transaction.category).all()

        if not result:
            return "No Transactions found for this user."
        
        summary="\n".join([
            f"{cat}: ₹{total:.2f}" for cat,total in result
        ])
        return f"Spending by category:\n {summary}"
    finally:
        db.close()


@tool
def get_recent_transactions(user_id: int)-> str:
    """Get the 10 most recent transactions for a user.
    Use this when the user asks about recent spending,
    last purchase, or what they bought recently. """
    db=get_db()
    try:
        txns= db.query(Transaction).filter(
            Transaction.user_id == user_id
        ).order_by(Transaction.created_at.desc()).limit(10).all()

        if not txns:
            return "No transcations found"
        
        result = "\n".join([
            f"{t.date} | {t.merchant} | ₹{t.amount} |{t.category}"
            for t in txns
        ])
        return f"Recent transactions:\n{result}"
    finally:
        db.close()


@tool
def get_monthly_total(user_id: int)-> str:
    """Get the total amount spend this month by a user.
    Use this when the user asks how much they spend this 
    month or wants their monthly total."""
    db=get_db()
    try:
        from datetime import datetime
        current_month = datetime.now().strftime("%Y-%m")

        total = db.query(func.sum(Transaction.amount)).filter(
            Transaction.user_id == user_id,
            Transaction.date.like(f"{current_month}%")
        ).scalar()

        total= total or 0
        return f"Total spent this month:₹{total:.2f} "
    finally:
        db.close()

@tool
def semantic_search_transactions(query: str,user_id: int) ->str:
    """Search transactions by meaning and context.
    Use this when the user asks conceptual questions like
    'when was I careless with money', 'find my impulsive spending',
    'show me unnecessary purchases', or any question that
    can't be answered with exact category filters."""
    return search_transactions(query=query,user_id=user_id)