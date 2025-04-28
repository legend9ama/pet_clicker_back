from fastapi import HTTPException, status
from app.modules.user_farm.repository import UserFarmRepository
from app.modules.farm_template.repository import FarmTemplateRepository
from app.modules.clicks.repository import ClickRepository
from app.modules.user_farm.schemas import *

class UserFarmService:
    def __init__(self, 
                 user_farm_repo: UserFarmRepository,
                 farm_template_repo: FarmTemplateRepository,
                 click_repo: ClickRepository):
        self.user_farm_repo = user_farm_repo
        self.farm_template_repo = farm_template_repo
        self.click_repo = click_repo

    async def get_farms(self, telegram_id: int) -> list[UserFarmResponse]:
        farms = await self.user_farm_repo.get_user_farms(telegram_id)
        return [UserFarmResponse.model_validate(farm) for farm in farms]

    async def purchase_farm(self, telegram_id: int, data: UserFarmPurchase) -> UserFarmResponse:
        template = await self.farm_template_repo.get_by_id(data.farm_id)
        if not template or not template.is_visible:
            raise HTTPException(status_code=400, detail="Farm not available")
        
        try:
            await self.click_repo.decrement_clicks(telegram_id, template.base_price)
            farm = await self.user_farm_repo.create_farm(telegram_id, data.farm_id)
            return UserFarmResponse.model_validate(farm)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))

    async def upgrade_farm(self, telegram_id: int, farm_id: int, data: UserFarmUpgrade) -> UserFarmResponse:
        farm = await self.user_farm_repo.get_farm(telegram_id, farm_id)
        total_cost = sum(
            farm.current_upgrade_cost * (farm.farm_template.price_multiplier ** i)
            for i in range(data.levels)
        )
        
        if not await self.click_repo.has_enough_clicks(telegram_id, total_cost):
            raise HTTPException(status_code=400, detail="Not enough clicks")
        
        try:
            await self.click_repo.decrement_clicks(telegram_id, total_cost)
            updated_farm = await self.user_farm_repo.upgrade_farm(telegram_id, farm_id, data.levels)
            return UserFarmResponse.model_validate(updated_farm)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))