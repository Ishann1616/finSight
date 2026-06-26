from sqlalchemy import Integer, Float, String, Column, DateTime, ForeignKey
from sqlalchemy import func
from database import Base

class Loan(Base):
    __tablename__="Loan"
    
    id=Column(Integer, primary_key=True, index=True)
    user_id= Column(Integer, ForeignKey("users.id"),nullable=False, index=True)
    loan_type=Column(String,nullable=False)
    principal=Column(Float,nullable=False)
    annual_rate=Column(Float,nullable=False)
    tenure_months=Column(Integer,nullable=False)
    start_date= Column(DateTime(timezone=True), server_default=func.now())
    status= Column(String,nullable=False)
    created_at= Column(DateTime(timezone=True), server_default=func.now())