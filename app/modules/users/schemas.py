from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
import json
from urllib.parse import parse_qs

class TelegramUserData(BaseModel):
    id: int
    username: Optional[str] = None

class UserCreate(BaseModel):
    telegram_id: int
    username: str
    referrer_id: Optional[int] = None

class UserUpdate(BaseModel):
    username: Optional[str] = Field(None, min_length=3, max_length=32)

class UserResponse(UserCreate):
    created_at: int

    model_config = ConfigDict(from_attributes=True)