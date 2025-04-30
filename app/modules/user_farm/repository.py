from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, update, delete, func
from app.models.user_farm import UserFarm
from app.models.farm_template import FarmTemplate
from sqlalchemy.orm import selectinload

class UserFarmRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_user_farms(self, telegram_id: int) -> list[UserFarm]:
        result = await self.db.execute(
            select(UserFarm).options(selectinload(UserFarm.farm_template)).where(UserFarm.telegram_id == telegram_id)
        )
        return result.unique().scalars().all()

    async def get_farm(self, telegram_id: int, farm_id: int) -> list[UserFarm]:
        result = await self.db.execute(select(UserFarm).where(and_(
            UserFarm.telegram_id == telegram_id,
            UserFarm.farm_id == farm_id
            ))
        )
        return result.unique().scalars().all()
    
    async def create_farm(self, telegram_id: int, farm_id: int) -> UserFarm:
        existing = await self.db.get(UserFarm, (telegram_id, farm_id))
        template = await self.db.get(FarmTemplate, farm_id)
        if existing:
            raise ValueError("Farm already owned")
        new_farm = UserFarm(telegram_id=telegram_id, farm_id=farm_id, level = 1, last_collected=func.extract('epoch', func.now()), current_income=template.base_income, current_upgrade_cost=template.base_price*template.price_multiplier)
        self.db.add(new_farm)
        await self.db.commit()
        return new_farm

    async def upgrade_farm(self, telegram_id: int, farm_id: int, levels: int) -> UserFarm:
        farm = await self.db.get(UserFarm, (telegram_id, farm_id))
        if not farm:
            raise ValueError("Farm not found")
        
        farm.level += levels
        await self.db.commit()
        await self.db.refresh(farm)
        return farm

    async def update_last_collected(self, telegram_id: int, farm_id: int) -> UserFarm:
        farm = await self.db.get(UserFarm, (telegram_id, farm_id))
        if not farm:
            raise ValueError("Farm not found")
        
        farm.last_collected = func.extract('epoch', func.now())
        await self.db.commit()
        await self.db.refresh(farm)
        return farm
    
    async def delete_farm(self, telegram_id: int, farm_id: int) -> bool:
        result = await self.db.execute(
            delete(UserFarm).where(and_(
                UserFarm.telegram_id == telegram_id,
                UserFarm.farm_id == farm_id
            ))
        )
        return result.rowcount > 0