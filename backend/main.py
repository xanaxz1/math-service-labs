from fastapi import FastAPI, Depends
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
import database
import models
import os

# Автоматически создаем таблицы в БД при старте
database.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="Math Service API")

# --- СЕТЕВОЙ МОДУЛЬ (REST API) ---
# Минимальный функционал: проверяем, что БД работает и мы можем писать в неё
@app.post("/api/test_db")
def test_db(db: Session = Depends(database.get_db)):
    # Ищем тестового юзера, если нет - создаем
    user = db.query(models.User).filter(models.User.username == "testuser").first()
    if not user:
        user = models.User(username="testuser", hashed_password="dummy", otp_secret="dummy")
        db.add(user)
        db.commit()
        db.refresh(user)
        
    # Создаем тестовую запись в истории вычислений
    calc = models.Calculation(user_id=user.id, expression="x**2", result="2*x")
    db.add(calc)
    db.commit()
    
    return {"status": "success", "message": "Прототип работает. Связь Frontend-Backend-DB установлена."}

# --- ФРОНТЕНД ---
# Отдаем HTML-страничку по корневому пути
FRONTEND_PATH = os.path.join(os.path.dirname(__file__), "..", "frontend")

@app.get("/")
def read_root():
    return FileResponse(os.path.join(FRONTEND_PATH, "index.html"))