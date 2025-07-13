from fastapi import APIRouter, Depends, HTTPException, status
from app import schemas
from sqlalchemy.orm import Session
from app.database import get_db
from app import db_tables as models
from app import utils

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}}
)

@router.post("/", response_model=schemas.UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    new_user = models.User(**user.model_dump())
    # Hash the password before saving
    new_user.password = utils.hash_password(new_user.password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user