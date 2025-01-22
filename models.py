from sqlalchemy import TIMESTAMP, Boolean, Column, Integer, String, text
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(20), unique=True, index=True)
    email = Column(String(100), unique=True, index=True)
    password = Column(String(100))
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'))
    verified = Column(Boolean, server_default='FALSE')