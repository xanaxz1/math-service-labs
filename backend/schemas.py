from pydantic import BaseModel

class UserRegister(BaseModel):
    username: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str
    otp_code: str  # 6-значный код из Google Authenticator

class CalcRequest(BaseModel):
    expression: str