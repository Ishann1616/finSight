from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.sql import func
from database import Base

class Budget(Base):
    __tablename__= "budgets"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"),nullable=False)
    category = Column(String, nullable=False)
    limit = Column(Float, nullable=False)
    created_at= Column(DateTime(timezone=True), server_default=func.now())
    

