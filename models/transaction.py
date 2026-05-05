from sqlalchemy import Column, Integer, String, Float,DateTime, ForeignKey
from sqlalchemy.sql import func
from database import Base

class Transaction(Base):
    __tablename__= "transactions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    merchant = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    category = Column(String, default="Uncategorized")
    payment_method = Column(String, default="UPI")
    date = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
