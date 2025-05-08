from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, update, func
from sqlalchemy.dialects.postgresql import insert as pg_insert
from app.models.click import Clicks
from app.modules.clicks.schemas import ClickCreate
from app.core.base_repository import BaseRepository
import time
from datetime import datetime
class ClickRepository(BaseRepository):
    async def get_clicks(self, telegram_id: int) -> Clicks:
        result = await self._db.execute(
            select(Clicks).where(Clicks.telegram_id == telegram_id)
        )
        if result:
            return result.scalar_one_or_none()
        new_click = ClickCreate(
            telegram_id=telegram_id,
            clicks_count=0,
            updated_at=int(time.mktime(datetime.timetuple(datetime.now()))))
        self._db.add(new_click)
        await self._db.commit()
        await self._db.refresh(new_click)
        return new_click
    
    async def _upsert_clicks(self, telegram_id: int, amount: int) -> Clicks:
        stmt = pg_insert(Clicks).values(
            telegram_id=telegram_id,
            clicks_count=amount
        ).on_conflict_do_update(
            index_elements=[Clicks.telegram_id],
            set_={
                'clicks_count': Clicks.clicks_count + amount if Clicks.clicks_count + amount else amount,
                'updated_at': func.extract('epoch', func.now())
            }
        ).returning(Clicks)
        
        result = await self._db.execute(stmt)
        await self._db.commit()
        return result.scalar_one()

    async def increment_clicks(self, telegram_id: int, amount: int) -> Clicks:
        return await self._upsert_clicks(telegram_id, amount)

    async def decrement_clicks(self, telegram_id: int, amount: int) -> Clicks:
        result = await self._db.execute(
            select(Clicks).where(Clicks.telegram_id == telegram_id)
        )
        clicks = result.scalar_one_or_none()
        
        if not clicks:
            raise ValueError("User clicks record not found")
        if clicks.clicks_count < amount:
            raise ValueError("Insufficient clicks balance")
            
        clicks.clicks_count -= amount
        clicks.updated_at = func.extract('epoch', func.now())
        await self._db.commit()
        await self._db.refresh(clicks)
        return clicks

    async def has_enough_clicks(self, telegram_id: int, amount: int) -> bool:
        clicks = await self.get_clicks(telegram_id)
        return clicks.clicks_count >= amount