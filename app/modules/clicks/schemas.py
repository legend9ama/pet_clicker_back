from pydantic import BaseModel, Field, field_validator, ConfigDict
from typing import Literal

class ClickBase(BaseModel):
    amount: int = Field(..., gt=0, description="Must be positive integer")
    
class ClickCreate(BaseModel):
    telegram_id: int
    clicks_count: int
    
class ClickIncrementRequest(ClickBase):
    source: Literal['manual', 'farm'] = Field(
        'manual', 
        description="Source of clicks: manual click or farm collection"
    )

class ClickDecrementRequest(ClickBase):
    pass

class ClickResponse(BaseModel):
    telegram_id: int
    clicks_count: int
    pet_coins: int
    updated_at: int

    model_config = ConfigDict(from_attributes=True)
