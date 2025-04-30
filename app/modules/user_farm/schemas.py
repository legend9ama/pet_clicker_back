from pydantic import BaseModel, Field, ConfigDict
from typing import Optional

class UserFarmBase(BaseModel):
    farm_id: int = Field(..., gt=0)
    level: int = Field(1, gt=0)

class UserFarmPurchase(BaseModel):
    farm_id: int = Field(..., gt=0)

class UserFarmUpgrade(BaseModel):
    levels: int = Field(1, gt=0, le=10, description="Number of levels to upgrade (1-10)")

class UserFarmResponse(BaseModel):
    farm_id: int
    level: int
    current_income: int
    current_upgrade_cost: int
    last_collected: Optional[float]
    name: str
    image_url: str
    
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

class UserFarmCollectionResponse(BaseModel):
    collected: int