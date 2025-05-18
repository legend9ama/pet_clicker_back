from pydantic import BaseModel, Field, ConfigDict
from typing import Optional

class FarmTemplateBase(BaseModel):
    name: str = Field(..., min_length=3, max_length=100)
    image_url: str = Field(..., description="Valid URL to farm image")
    base_price: float = Field(..., gt=0)
    price_multiplier: float = Field(..., gt=1.0)
    base_income: float = Field(..., gt=0)
    income_multiplier: float = Field(..., gt=1.0)
    clicks_needed: int

class FarmTemplateCreate(FarmTemplateBase):
    is_visible: bool = Field(False, description="Visibility for users")

class FarmTemplateUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=3, max_length=100)
    image_url: Optional[str] = None
    base_price: Optional[float] = Field(None, gt=0)
    price_multiplier: Optional[float] = Field(None, gt=1.0)
    base_income: Optional[float] = Field(None, gt=0)
    income_multiplier: Optional[float] = Field(None, gt=1.0)
    is_visible: Optional[bool] = None

class FarmTemplateResponse(FarmTemplateBase):
    farm_id: int
    is_visible: bool

    model_config = ConfigDict(from_attributes=True)
    
