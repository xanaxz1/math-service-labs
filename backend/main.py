from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import database
import models
import schemas
import os
import pyotp
import bcrypt

# --- Функции для безопасного хеширования паролей (чистый bcrypt) ---
def get_password_hash(password: str) -> str:
    pwd_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(pwd_bytes, salt)
    return hashed.decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    pwd_bytes = plain_password.encode('utf-8')
    hashed_bytes = hashed_password.encode('utf-8')
    return bcrypt.checkpw(pwd_bytes, hashed_bytes)
# -------------------------------------------------------------------

# Создаем таблицы в БД при старте
database.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="Math Service API")

# Разрешаем CORS для корректной работы фронтенда
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

FRONTEND_PATH = os.path.join(os.path.dirname(__file__), "..", "frontend")

@app.get("/")
def read_root():
    return FileResponse(os.path.join(FRONTEND_PATH, "index.html"))

# --- 1. РЕГИСТРАЦИЯ ---
@app.post("/api/register")
def register(user: schemas.UserRegister, db: Session = Depends(database.get_db)):
    db_user = db.query(models.User).filter(models.User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Пользователь уже существует")
    
    # Генерируем секрет для 2FA и хешируем пароль
    otp_secret = pyotp.random_base32()
    hashed_pw = get_password_hash(user.password)
    
    new_user = models.User(username=user.username, hashed_password=hashed_pw, otp_secret=otp_secret)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    # Формируем URI для генерации QR-кода (совместим с Google Authenticator)
    otp_uri = pyotp.totp.TOTP(otp_secret).provisioning_uri(name=user.username, issuer_name="MathService")
    
    return {"message": "Регистрация успешна", "otp_secret": otp_secret, "otp_uri": otp_uri}

# --- 2. ВХОД С 2FA ---
@app.post("/api/login")
def login(user: schemas.UserLogin, db: Session = Depends(database.get_db)):
    db_user = db.query(models.User).filter(models.User.username == user.username).first()
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Неверный логин или пароль")
    
    # Проверка 2FA кода
    totp = pyotp.TOTP(db_user.otp_secret)
    if not totp.verify(user.otp_code):
        raise HTTPException(status_code=401, detail="Неверный код 2FA")
    
    return {"message": "Вход выполнен успешно", "token": "dummy-secure-jwt-token"}

# --- 3. ЗАЩИЩЕННЫЙ ЭНДПОИНТ 
@app.post("/api/calculate")
def calculate(req: schemas.CalcRequest):
    return {"expression": req.expression, "result": f"Вычислено: {req.expression} (функционал в разработке)"}