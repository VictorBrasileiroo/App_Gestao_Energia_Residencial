# app/schemas.py
from pydantic import BaseModel
from typing import Optional, List

class UserCreate(BaseModel):
    name: Optional[str]
    email: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class DashboardSummary(BaseModel):
    date: str
    energy_kwh: float
    cost_brl: float
    comparison_vs_yesterday_pct: float
