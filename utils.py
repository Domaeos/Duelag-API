from datetime import datetime, timedelta, timezone
from typing import Any, Union
import jwt
import jwt.exceptions
from passlib.context import CryptContext
from config import ACCESS_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_MINUTES, ALGORITHM, JWT_SECRET_KEY, JWT_REFRESH_SECRET_KEY

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info(" --- ENVIRONMENT VARIABLES --- ")
logger.info(f"Algorithm: {ALGORITHM}")
logger.info(f"JWT Secret Key: {JWT_SECRET_KEY}")
logger.info(f"JWT Refresh Key: {JWT_REFRESH_SECRET_KEY}")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(subject: Union[str, Any], expires_delta: int = None) -> str:
    if expires_delta is not None:
        expires_delta = datetime.now(timezone.utc) + expires_delta

    else:
        expires_delta = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode = {"exp": expires_delta, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


def create_refresh_token(subject: Union[str, Any], expires_delta: int = None) -> str:
    logger.info("Creating refresh token")

    if expires_delta is not None:
        expires_delta = datetime.now(timezone.utc) + expires_delta
    else:
        expires_delta = datetime.now(timezone.utc) + timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)

    to_encode = {"exp": expires_delta, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, JWT_REFRESH_SECRET_KEY, ALGORITHM)

    return encoded_jwt

def decodeJWT(jwtoken: str, refresh: bool = False):
    secret_key = JWT_REFRESH_SECRET_KEY if refresh else JWT_SECRET_KEY
    try:
        payload = jwt.decode(
            jwtoken,
            secret_key,
            algorithms=[ALGORITHM],
            options={"verify_exp": True}
        )
        return payload
    except jwt.exceptions.InvalidTokenError as e:
        logger.error(f"Error decoding token: {e}")
        return None