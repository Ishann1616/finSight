from database import SessionLocal
from models.conversation import Conversation

def save_message(user_id: int,role:str, content: str):
    db= SessionLocal()
    try:
        message= Conversation(
            user_id=user_id,
            role=role,
            content=content
        )
        db.add(message)
        db.commit()
    finally:
        db.close()

def load_history(user_id: int,limit: int = 10):
    db=SessionLocal()
    try:
        message=db.query(Conversation).filter(
            Conversation.user_id == user_id
        ).order_by(Conversation.created_at.desc()).limit(limit).all()
        
        message.reverse()

        return[
            {"role":m.role, "content":m.content}
            for m in message
        ]
    finally:
        db.close()