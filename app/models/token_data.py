# model/token_data.py
from datetime import datetime
from pydantic import BaseModel
from typing import Optional


class TokenData(BaseModel):
    username: Optional[str] = None
    scopes: list[str] = []
    expires_at: Optional[datetime] = None
