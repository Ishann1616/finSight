from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from passlib.context import CryptContext
from database import get_db
from models.user import User
from jose import jwt
from datetime import datetime, timedelta
from config import SECRET_KEY,ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserCreate(BaseModel):
    name:str
    email:str
    password:str
    bank_name: str = None
    current_balance: float


class UserResponse(BaseModel):
    id:int
    name:str
    email:str

    class Config:
        from_attributes =True


@router.post("/register", response_model=UserResponse)
def register(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400 ,detail="Email already registered")
    hashed_password = pwd_context.hash(user.password)
    new_user= User(name=user.name, email=user.email, password=hashed_password, bank_name= user.bank_name ,current_balance=user.current_balance)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# LOGIN

class UserLogin(BaseModel):
    email:str
    password:str

def create_token(data:dict):
    to_encode = data.copy()
    expire = datetime.utcnow()+ timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})
    return jwt.encode(to_encode,SECRET_KEY,algorithm= ALGORITHM)

@router.post("/login")
def login(user: UserLogin,db: Session = Depends(get_db)):
    db_user= db.query(User).filter(User.email== user.email).first()
    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    if not pwd_context.verify(user.password, db_user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_token({"user_id": db_user.id})
    return {"access_token": token, "token_type": "bearer"}

def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id= payload.get("user_id")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=401, detail="User not found")
        return user
    except:
        raise HTTPException(status_code=401, detail="Invalid token")