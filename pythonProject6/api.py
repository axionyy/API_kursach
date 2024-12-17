from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session, sessionmaker
from pydantic import BaseModel
from typing import List
from database import *

# Создание таблиц в базе данных
Base.metadata.create_all(bind=engine)

#python -m uvicorn api:app --reload --host 0.0.0.0 --port 8000

app = FastAPI()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class UserLogin(BaseModel):
    login: str
    password: str

@app.post("/login")
def login(user_login: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.login == user_login.login).first()
    if not user or user.password != user_login.password:
        raise HTTPException(status_code=400, detail="Invalid login or password")
    return {"message": "Login successful", "user_id": user.id}
