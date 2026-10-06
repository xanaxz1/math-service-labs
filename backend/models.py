from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.sql import func
from database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    otp_secret = Column(String) # Поле для секрета 2FA (заготовим на будущее)

class Calculation(Base):
    __tablename__ = "calculations"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    expression = Column(Text)   # Математическое выражение
    result = Column(Text)       # Результат вычисления
    created_at = Column(DateTime(timezone=True), server_default=func.now())