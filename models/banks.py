from sqlalchemy import Integer, Float, String, Column
from database import Base

class Bank(Base):
    __tablename__= "BankLoanDetails"
    id=Column(Integer,primary_key=True,index=True,nullable=False)
    bank_name=Column(String,nullable=False)
    loan_type=Column(String,nullable=False)
    interest_rate=Column(Float,nullable=False)
    processing_fee= Column(Float,nullable=False)
    max_tenure_months=Column(Integer,nullable=False)