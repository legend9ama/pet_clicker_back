from pydantic import BaseModel, Field, ConfigDict

class UserFarmBase(BaseModel):
    farm_id: int = Field(..., gt=0)
    level: int = Field(1, gt=0)

class UserFarmPurchase(BaseModel):
    farm_id: int = Field(..., gt=0)

class UserFarmUpgrade(BaseModel):
    levels: int = Field(1, gt=0, le=10, description="Number of levels to upgrade (1-10)")

class UserFarmPurchaseResponse(BaseModel):
    farm_id: int
    level: int
    current_income: int
    current_upgrade_cost: int
    name: str
    image_url: str
    
    model_config = ConfigDict(from_attributes=True)
    
class UserFarmResponse(BaseModel):
    farm_id: int
    level: int
    current_income: int
    current_upgrade_cost: int
    last_collected: int
    name: str
    image_url: str
    clicks_needed: int
    
    model_config = ConfigDict(from_attributes=True)

class UserFarmCollectionResponse(BaseModel):
    collected: int