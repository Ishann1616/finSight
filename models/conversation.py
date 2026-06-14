from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy import func
from database import Base

class Conversation(Base):
    __tablename__="conversations"

    id=Column(Integer, primary_key=True, index=True)
    user_id= Column(Integer, ForeignKey("users.id"), nullable=False)
    role = Column(String, nullable=False)
    content = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())