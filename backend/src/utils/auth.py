from fastapi import status
from fastapi.security import HTTPBasicCredentials, HTTPBasic
from fastapi import Depends, HTTPException
import secrets
from src.constants import APP_USER_LIST

def verify_credentials(credentials: HTTPBasicCredentials = Depends(HTTPBasic())):
    for user in APP_USER_LIST:
        current_username_bytes = credentials.username.encode("utf8")
        correct_username_bytes = user["username"].encode("utf8")
        is_correct_username = secrets.compare_digest(
            current_username_bytes, correct_username_bytes
        )
        
        if is_correct_username:
            current_password_bytes = credentials.password.encode("utf8")
            correct_password_bytes = user["password"].encode("utf8")
            is_correct_password = secrets.compare_digest(
                current_password_bytes, correct_password_bytes
            )
            
            if is_correct_password:
                return user
                
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password",
        headers={"WWW-Authenticate": "Basic"},
    ) 