from fastapi import HTTPException
from app.modules.user_farm.repository import UserFarmRepository
from app.modules.farm_template.repository import FarmTemplateRepository
from app.modules.clicks.repository import ClickRepository
from app.modules.user_farm.schemas import *
from datetime import datetime
import time
from app.core.config import settings

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
        return [UserFarmResponse.model_validate(
                {
                    **farm.__dict__,
                    "last_collected": settings.unixtimestamp,
                    "name": farm.farm_template.name,
                    "image_url": farm.farm_template.image_url
                }
            )
        for farm in farms]

    async def purchase_farm(self, telegram_id: int, data: UserFarmPurchase) -> UserFarmPurchaseResponse:
        template = await self.farm_template_repo.get_by_id(data.farm_id)
        if not template or not template.is_visible:
            raise HTTPException(status_code=400, detail="Farm not available")
        if not await self.click_repo.has_enough_clicks(telegram_id, template.base_price):
            raise HTTPException(status_code=400, detail="Not enough clicks")
        try:
            farm = await self.user_farm_repo.create_farm(telegram_id, data.farm_id)
            await self.click_repo.decrement_clicks(telegram_id, template.base_price)
            return UserFarmPurchaseResponse.model_validate({
                    **farm.__dict__,
                    "name": farm.farm_template.name,
                    "image_url": farm.farm_template.image_url
                })
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))

    async def upgrade_farm(self, telegram_id: int, farm_id: int, data: UserFarmUpgrade) -> UserFarmResponse:
        farm = await self.user_farm_repo.get_farm(telegram_id, farm_id)
        
        if not await self.click_repo.has_enough_clicks(telegram_id, farm.current_upgrade_cost):
            raise HTTPException(status_code=400, detail="Not enough clicks")
        try:
            await self.click_repo.decrement_clicks(telegram_id, farm.current_upgrade_cost)
            updated_farm = await self.user_farm_repo.upgrade_farm(telegram_id, farm_id, data.levels)
            return UserFarmResponse.model_validate({
                **updated_farm.__dict__,
                "name": farm.farm_template.name,
                "image_url": farm.farm_template.image_url
            })
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
        
    async def collect_farm(self, telegram_id: int, farm_id: int) -> UserFarmCollectionResponse:
        farm = await self.user_farm_repo.get_farm(telegram_id, farm_id)
        collected = int(farm.current_income / 3600 * (time.mktime(datetime.timetuple(datetime.now())) - farm.last_collected))
        try:
            await self.click_repo.increment_clicks(telegram_id, collected)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
        try:
            await self.user_farm_repo.update_last_collected(telegram_id, farm_id)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
        
        return UserFarmCollectionResponse.model_validate({"collected" : collected})
        