from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List
from datetime import datetime

class LoginRequest(BaseModel):
    username: str
    password: str

class LoginResponse(BaseModel):
    token: str
    expires_in: int

class KYCRequest(BaseModel):
    token: str

class KYCStatus(BaseModel):
    status: str
    verified: bool
    updated_at: Optional[datetime] = None

class Card(BaseModel):
    id: str
    last4: str
    brand: str
    holder: Optional[str] = None
    exp_month: int
    exp_year: int

class Transaction(BaseModel):
    id: str
    amount: float
    currency: str = Field(default="INR")
    description: Optional[str] = None
    status: str
    created_at: datetime

class DemoEvent(BaseModel):
    type: str
    detail: Optional[dict] = None
