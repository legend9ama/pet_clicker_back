from pydantic import BaseModel, Field, ConfigDict
from typing import Optional

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
    photo_url: str | None
    pet_coins: int
    position: int

    model_config = ConfigDict(from_attributes=True)

class UserUpdate(BaseModel):
    username: Optional[str] = Field(None, min_length=3, max_length=32)

class UserResponse(UserCreate):
    created_at: int

    model_config = ConfigDict(from_attributes=True)