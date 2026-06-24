from sqlalchemy import Column,Integer, String, Float,DateTime, ForeignKey
from sqlalchemy import func
from database import Base

class SIPPlan(Base):
    __tablename__="SipPlans"

    id=Column(Integer, primary_key=True, index=True)
    user_id=Column(Integer, ForeignKey("users.id"), nullable=False)
    fund_name=Column(String, nullable=False)
    amount=Column(Float, nullable=False)
    due_date=Column(Integer,nullable=False)
    frequency= Column(String, nullable=False)
    status =Column(String, nullable=False)
    created_at=Column(DateTime(timezone=True), server_default=func.now())
