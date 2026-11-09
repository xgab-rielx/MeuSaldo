from pydantic import BaseModel, Field
from decimal import Decimal
from datetime import datetime


class SpendingCreate(BaseModel):
    description: str
    category: str
    value: Decimal = Field(ge=0, max_digits=10, decimal_places=2)
    date: datetime = Field(default_factory=datetime.now)

class SpendingUpdate(BaseModel):
    description: str
    category: str
    value: Decimal = Field(ge=0, max_digits=10, decimal_places=2)

class SpendingGet(BaseModel):
    spending_id: int
    description: str
    category: str
    value: Decimal = Field(ge=0, max_digits=10, decimal_places=2)
    date: datetime

class LoginRequest(BaseModel):
    username: str
    password: str