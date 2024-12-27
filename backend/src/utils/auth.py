from fastapi import status, Depends, HTTPException
from fastapi.security import HTTPBasicCredentials, HTTPBasic
import secrets
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.constants import DB_URI
from src.models import User

engine = create_engine(DB_URI)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def verify_credentials(
    credentials: HTTPBasicCredentials = Depends(HTTPBasic()),
    db: SessionLocal = Depends(get_db)
):
    user = db.query(User).filter(User.username == credentials.username).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    
    if not User.verify_password(credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    
    return user.username 