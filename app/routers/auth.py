from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.database import get_db
from app import db_tables as models, oauth2, utils
from app import schemas

router = APIRouter(
    tags=["Authentication"],
    )

@router.post("/login", response_model=schemas.Token)
def login(user: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    found_user = db.query(models.User).filter(models.User.email == user.username).first()

    if found_user ==  None or utils.verify_password(user.password, found_user.password) != True:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail= "Invalid Credentials")
     
    else: 
        token = oauth2.create_access_token(data={'user_id':found_user.id})


    return {'token': token, 'token_type': 'bearer'}
