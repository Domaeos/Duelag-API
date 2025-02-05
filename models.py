from sqlalchemy import TIMESTAMP, Boolean, Column, Float, Integer, String, text, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(20), unique=True, index=True)
    email = Column(String(100), unique=True, index=True)
    password = Column(String(100))
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'))
    verified = Column(Boolean, server_default='FALSE')

    game_data = relationship("GameData", back_populates="user", uselist=False, cascade="all, delete-orphan")
    duel_history = relationship("DuelHistory", primaryjoin="User.id == DuelHistory.user_id")


class TokenTable(Base):
    __tablename__ = "token"

    user_id = Column(Integer)
    access_token = Column(String(450), primary_key=True)
    refresh_token = Column(String(450),nullable=False)
    online = Column(Boolean)
    premium = Column(Boolean, default=False)
    created_date = Column(TIMESTAMP(timezone=True), server_default=text('now()'))

class GameData(Base):
    __tablename__ = "game_data"

    id = Column(Integer, primary_key=True)
    kills = Column(Integer, default=0)
    deaths = Column(Integer, default=0)
    assists = Column(Integer, default=0)

    avatar = Column(String(50), nullable=True)
    model = Column(String(50), nullable=True)

    last_arena = Column(String(50), nullable=True)
    last_coords = Column(String(50), nullable=True)

    hit_points = Column(Integer, default=100)
    mana_points = Column(Integer, default=100)

    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("User", back_populates="game_data")

class DuelHistory(Base):
    __tablename__ = "duel_history"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    enemy_id = Column(Integer, ForeignKey('users.id'))
    win = Column(Boolean)
    length = Column(Float)
    arena = Column(String(50))
    timestamp = Column(TIMESTAMP(timezone=True), server_default=text('now()'))

    user = relationship("User", foreign_keys=[user_id])
    enemy = relationship("User", foreign_keys=[enemy_id])