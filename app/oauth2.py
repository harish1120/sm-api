from datetime import datetime, timezone, timedelta
import time
from fastapi import Depends, HTTPException, status
import jwt
from jwt.exceptions import PyJWTError
from pytest import Session

from app import database, schemas, db_tables as models
from .config import settings

from fastapi.security import (
    OAuth2PasswordBearer,
    OAuth2PasswordRequestForm,
    SecurityScopes,
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def create_access_token(data: dict):
    to_encode = data.copy()

    if settings.EXPIRE_IN:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.EXPIRE_IN)
    else: 
        expire = datetime.now(timezone.utc) + timedelta(minutes=15) 

    to_encode.update({"exp": expire})

    return jwt.encode(to_encode, settings.SECURITY_KEY, settings.ALGORITHM)

def verify_access_token(token: str, credentials_exception):
    try: 
        payload = jwt.decode(token, settings.SECURITY_KEY, settings.ALGORITHM)
        id: str = payload.get('user_id')
        if id is None:
            raise credentials_exception
        token_data = schemas.TokenData(id=id)
    except PyJWTError:
        raise credentials_exception
    
    return token_data


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    credential_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                                         detail="Could not validate credentials", 
                                         headers={"WWW-Authenticate": "Bearer"})
    
    token = verify_access_token(token, credential_exception)
    user = db.query(models.User).filter(models.User.id == token.id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User does not exist")
    return user
