import pytest
from fastapi.testclient import TestClient
from main import app
import math_engine
import pyotp
import bcrypt

client = TestClient(app)

# --- Тесты функционального модуля (математика) ---
def test_derivative():
    """Тест вычисления производной"""
    result = math_engine.calculate_derivative("x**2 + 3*x")
    assert result == "2*x + 3"

def test_integral():
    """Тест вычисления определенного интеграла"""
    result = math_engine.calculate_integral("x**2", 0, 3)
    assert result == 9.0

def test_root():
    """Тест поиска корня уравнения"""
    result = math_engine.find_root("x**2 - 4", 1.0)
    assert result == 2.0

# --- Тесты безопасности ---
def test_password_hashing():
    """Тест хеширования паролей"""
    password = "test_password_123"
    from main import get_password_hash, verify_password
    hashed = get_password_hash(password)
    assert verify_password(password, hashed) == True
    assert verify_password("wrong_password", hashed) == False

def test_2fa_generation():
    """Тест генерации и проверки 2FA кодов"""
    secret = pyotp.random_base32()
    totp = pyotp.TOTP(secret)
    code = totp.now()
    assert totp.verify(code) == True
    assert totp.verify("000000") == False

# --- Тесты API ---
def test_register_and_login():
    """Тест регистрации и входа с 2FA"""
    # Регистрация
    response = client.post("/api/register", json={
        "username": "testuser_api",
        "password": "testpass123"
    })
    assert response.status_code == 200
    data = response.json()
    assert "otp_secret" in data
    assert "otp_uri" in data
    
    otp_secret = data["otp_secret"]
    
    # Генерируем код 2FA
    totp = pyotp.TOTP(otp_secret)
    otp_code = totp.now()
    
    # Вход с 2FA
    response = client.post("/api/login", json={
        "username": "testuser_api",
        "password": "testpass123",
        "otp_code": otp_code
    })
    assert response.status_code == 200
    assert response.json()["message"] == "Вход выполнен успешно"

def test_calculate_derivative_api():
    """Тест API вычисления производной"""
    response = client.post("/api/calculate", json={
        "expression": "x**3",
        "operation": "derivative"
    })
    assert response.status_code == 200
    assert response.json()["result"] == "3*x**2"