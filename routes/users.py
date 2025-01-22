
from fastapi import APIRouter, Depends, HTTPException
from starlette import status
from sqlalchemy.orm import Session
from database import get_db
import models
import schemas
from utils import get_password_hash


router = APIRouter(
  prefix="/users",
  tags=["Users"]
)

@router.post("/register", status_code=status.HTTP_201_CREATED)
def register_user(user: schemas.CreateUser, session: Session = Depends(get_db)):
  existing_user = session.query(models.User).filter(models.User.username == user.username).first()
  if existing_user:
    raise HTTPException(status_code=400, detail="Username already exists")

  encrypted_password = get_password_hash(user.password)

  new_user = models.User(username=user.username, email=user.email, password=encrypted_password)
  session.add(new_user)
  session.commit()
  session.refresh(new_user)

  return {"message": "User created successfully", "data": new_user}