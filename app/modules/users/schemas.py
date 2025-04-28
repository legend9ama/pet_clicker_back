from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
import json
from urllib.parse import parse_qs

class TelegramInitData(BaseModel):
    init_data: str = Field(..., description="Telegram InitData")

class UserCreateRequest(TelegramInitData):
    referrer_id: Optional[int] = Field(None, gt=0)

class UserCreate(BaseModel):
    telegram_id: int
    username: str
    referrer_id: Optional[int] = None

class UserUpdate(BaseModel):
    username: Optional[str] = Field(None, min_length=3, max_length=32)

class UserResponse(BaseModel):
    telegram_id: int
    username: str
    created_at: int
    referrer_id: Optional[int]
    clicks_count: int
    farms_count: int

    model_config = ConfigDict(from_attributes=True)

    @classmethod
    def parse_init_data(cls, init_data: str) -> dict:
        parsed = parse_qs(init_data)
        user_data = json.loads(parsed.get('user', ['{}'])[0])
        return {
            'telegram_id': user_data.get('id'),
            'username': user_data.get('username')
        }