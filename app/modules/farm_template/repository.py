from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from app.models.farm_template import FarmTemplate
from app.core.base_repository import BaseRepository

class FarmTemplateRepository(BaseRepository):
    async def create(self, data: dict) -> FarmTemplate:
        new_template = FarmTemplate(**data)
        self._db.add(new_template)
        await self._db.commit()
        await self._db.refresh(new_template)
        return new_template

    async def get_all(self) -> list[FarmTemplate]:
        result = await self._db.execute(select(FarmTemplate).order_by(FarmTemplate.base_price))
        return result.scalars().all()
    
    async def get_all_visible(self) -> list[FarmTemplate]:
        result = await self._db.execute(select(FarmTemplate).where(FarmTemplate.is_visible == True).order_by(FarmTemplate.base_price))
        return result.scalars().all()

    async def get_by_id(self, farm_id: int) -> FarmTemplate | None:
        result = await self._db.execute(
            select(FarmTemplate).where(FarmTemplate.farm_id == farm_id)
        )
        return result.scalars().all()

    async def update(self, farm_id: int, data: dict) -> FarmTemplate | None:
        stmt = (
            update(FarmTemplate)
            .where(FarmTemplate.farm_id == farm_id)
            .values(**data)
            .returning(FarmTemplate)
        )
        result = await self._db.execute(stmt)
        await self._db.commit()
        return result.scalars().first()

    async def delete(self, farm_id: int) -> bool:
        stmt = delete(FarmTemplate).where(FarmTemplate.farm_id == farm_id)
        result = await self._db.execute(stmt)
        await self._db.commit()
        return result.rowcount > 0

    async def toggle_visibility(self, farm_id: int) -> FarmTemplate | None:
        stmt = (
            update(FarmTemplate)
            .where(FarmTemplate.farm_id == farm_id)
            .values(is_visible=~FarmTemplate.is_visible)
            .returning(FarmTemplate)
        )
        result = await self._db.execute(stmt)
        await self._db.commit()
        return result.scalars().first()