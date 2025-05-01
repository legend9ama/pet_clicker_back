from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
import json
from urllib.parse import parse_qs

class TelegramUserData(BaseModel):
    id: int
    first_name: str
    last_name: Optional[str] | None
    username: Optional[str] | None
    photo_url: Optional[str] | None
    referrer_id: Optional[int] = None

class UserCreate(BaseModel):
    telegram_id: int
    first_name: str
    last_name: Optional[str] | None
    username: Optional[str] | None
    photo_url: Optional[str] | None
    referrer_id: Optional[int] = None

class LeaderboardUser(BaseModel):
    username: str
    avatar_url: str | None
    clicks_count: int
    position: int

    model_config = ConfigDict(from_attributes=True)
    
class UserUpdate(BaseModel):
    username: Optional[str] = Field(None, min_length=3, max_length=32)

class UserResponse(UserCreate):
    created_at: int

    model_config = ConfigDict(from_attributes=True)