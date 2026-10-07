from pydantic import BaseModel
from typing import Optional

class UserRegister(BaseModel):
    username: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str
    otp_code: str

class CalcRequest(BaseModel):
    expression: str
    operation: str 
    param_a: Optional[float] = None
    param_b: Optional[float] = None
    param_x0: Optional[float] = None