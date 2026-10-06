from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Создаем локальную SQLite базу данных (файл math_service.db появится сам)
SQLALCHEMY_DATABASE_URL = "sqlite:///./math_service.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Зависимость для получения сессии БД
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()