from sqlalchemy import Integer, Column, String, DateTime, Float, ForeignKey
from sqlalchemy import func
from database import Base

class Fund(Base):
    __tablename__= "Funds"
    id= Column(Integer, primary_key=True,index= True,nullable=False)
    fund_name= Column(String, nullable=False)
    category= Column(String, nullable=False)
    risk_profile=Column(String, nullable=False)
    expected_return=Column(Float, nullable=False)