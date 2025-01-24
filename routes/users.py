
from fastapi import APIRouter, Depends, HTTPException
from starlette import status
from sqlalchemy.orm import Session
from auth_bearer import JWTBearer
from config import JWT_REFRESH_SECRET_KEY
from database import get_session
import models
import schemas
from utils import create_access_token, create_refresh_token, decodeJWT, get_password_hash, verify_password, logger


router = APIRouter(
  prefix="/users",
  tags=["Users"]
)

@router.post("/register", status_code=status.HTTP_201_CREATED)
def register_user(user: schemas.CreateUser, session: Session = Depends(get_session)):
  existing_username = session.query(models.User).filter(models.User.username == user.username).first()
  if existing_username:
    raise HTTPException(status_code=400, detail="Username is taken")

  existing_email = session.query(models.User).filter(models.User.email == user.email).first()
  if existing_email:
    raise HTTPException(status_code=400, detail="Email already has an account")

  encrypted_password = get_password_hash(user.password)

  new_user = models.User(username=user.username, email=user.email, password=encrypted_password)
  session.add(new_user)
  session.commit()
  session.refresh(new_user)

  return {"message": "User created successfully"}

@router.post("/login", status_code=status.HTTP_200_OK)
def login_user(request: schemas.LoginUser, session: Session = Depends(get_session)):

  user = session.query(models.User).filter(models.User.email == request.email).first()
  if not user:
    raise HTTPException(400, detail="Email or password is incorrect")

  password_correct = verify_password(request.password, user.password)
  if not password_correct:
    raise HTTPException(400, detail="Email or password is incorrect")

  new_access_token = create_access_token(user.id)
  new_refresh_token = create_refresh_token(user.id)

  token_db = models.TokenTable(user_id=user.id,  access_token=new_access_token,  refresh_token=new_refresh_token, status=True)
  session.add(token_db)
  session.commit()
  session.refresh(token_db)

  return {
      "access_token": new_access_token,
      "refresh_token": new_refresh_token,
  }

@router.get('/all')
def getusers(dependencies=Depends(JWTBearer()),session: Session = Depends(get_session)):
    user = session.query(models.User).all()
    return user

@router.post("/refresh")
def refresh_token(request: schemas.RefreshRequest, session: Session = Depends(get_session)):
    try:

        payload = decodeJWT(request.refresh_token, True)
        if not payload:
           raise HTTPException(status_code=400, detail="Invalid refresh token")

        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(status_code=400, detail="Invalid refresh token")

        token_record = session.query(models.TokenTable).filter_by(
            user_id=user_id,
            refresh_token=request.refresh_token,
            status=True
        ).first()

        if not token_record:
            logger.error("Error finding token record")
            raise HTTPException(status_code=401, detail="Invalid or expired refresh token")

        new_access_token = create_access_token(user_id)
        token_record.access_token = new_access_token

        session.commit()
        session.refresh(token_record)

        return {
            "detail": "Token refreshed successfully",
            "access_token": new_access_token,
        }


    except Exception as e:
        logger.error(f"Caught in refresh: {e}")
        raise HTTPException(status_code=401, detail="Invalid or expired refresh token")