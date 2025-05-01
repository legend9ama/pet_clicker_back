from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, delete, func
from app.models.user_farm import UserFarm
from app.models.farm_template import FarmTemplate
from sqlalchemy.orm import selectinload
from app.core.base_repository import BaseRepository

class UserFarmRepository(BaseRepository):
    async def get_user_farms(self, telegram_id: int) -> list[UserFarm]:
        result = await self._db.execute(
            select(UserFarm).options(selectinload(UserFarm.farm_template)).where(UserFarm.telegram_id == telegram_id).order_by(UserFarm.current_income)
        )
        return result.scalars().all()

    async def get_farm(self, telegram_id: int, farm_id: int) -> UserFarm:
        result = await self._db.execute(select(UserFarm).where(and_(
            UserFarm.telegram_id == telegram_id,
            UserFarm.farm_id == farm_id
            ))
        )
        return result.scalar_one_or_none()
    
    async def create_farm(self, telegram_id: int, farm_id: int) -> UserFarm:
        existing = await self._db.get(UserFarm, (telegram_id, farm_id))
        template = await self._db.get(FarmTemplate, farm_id)
        if existing:
            raise ValueError("Farm already owned")
        new_farm = UserFarm(telegram_id=telegram_id, farm_id=farm_id, level = 1, last_collected=func.extract('epoch', func.now()), current_income=template.base_income, current_upgrade_cost=template.base_price*template.price_multiplier)
        self._db.add(new_farm)
        await self._db.commit()
        return new_farm

    async def upgrade_farm(self, telegram_id: int, farm_id: int, levels: int) -> UserFarm:
        farm = await self._db.get(UserFarm, (telegram_id, farm_id))
        template = await self._db.get(FarmTemplate, farm_id)
        if not farm or not template:
            raise ValueError("Farm not found")
        
        farm.level += levels
        farm.current_income = template.base_income*(template.income_multiplier**farm.level)
        farm.current_upgrade_cost = template.base_price*(template.price_multiplier**farm.level)
        await self._db.commit()
        await self._db.refresh(farm)
        return farm

    async def update_last_collected(self, telegram_id: int, farm_id: int) -> UserFarm:
        farm = await self._db.get(UserFarm, (telegram_id, farm_id))
        if not farm:
            raise ValueError("Farm not found")
        
        farm.last_collected = func.extract('epoch', func.now())
        await self._db.commit()
        await self._db.refresh(farm)
        return farm
    
    async def delete_farm(self, telegram_id: int, farm_id: int) -> bool:
        result = await self._db.execute(
            delete(UserFarm).where(and_(
                UserFarm.telegram_id == telegram_id,
                UserFarm.farm_id == farm_id
            ))
        )
        return result.rowcount > 0