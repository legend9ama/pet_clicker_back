from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete, func
from sqlalchemy.orm import joinedload
from app.models.user import User
from app.modules.users.schemas import UserCreate
from app.models.click import Clicks
from app.core.base_repository import BaseRepository

class UserRepository(BaseRepository):
    async def create(self, user: UserCreate) -> User:
        new_user = User(
            telegram_id=user.telegram_id,
            first_name=user.first_name,
            last_name=user.last_name,
            username=user.username,
            photo_url=user.photo_url,
        )
        self._db.add(new_user)
        await self._db.commit()
        await self._db.refresh(new_user)
        return new_user

    async def get_leaderboard(self, limit: int = 5) -> list[User]:
        result = await self._db.execute(
            select(User).options(joinedload(User.clicks))
            .outerjoin(Clicks)
            .order_by(func.coalesce(Clicks.pet_coins, 0).desc())
            .limit(limit)
        )
        return result.scalars().all()
    
    async def get_by_id(self, telegram_id: int) -> User | None:
        result = await self._db.execute(
            select(User).where(User.telegram_id == telegram_id)
        )
        return result.scalars().first()

    async def get_or_create(self, user_data: dict) -> User:
        user = await self.get_by_id(user_data.telegram_id)
        if user:
            return user
        new_user = User(**user_data)
        self._db.add(new_user)
        await self._db.commit()
        return new_user

    async def update(self, telegram_id: int, data: dict) -> User | None:
        stmt = (
            update(User)
            .where(User.telegram_id == telegram_id)
            .values(**data)
            .returning(User)
        )
        result = await self._db.execute(stmt)
        await self._db.commit()
        return result.scalars().first()

    async def delete(self, telegram_id: int) -> bool:
        stmt = delete(User).where(User.telegram_id == telegram_id)
        result = await self._db.execute(stmt)
        await self._db.commit()
        return result.rowcount > 0

    async def get_user_stats(self, telegram_id: int) -> dict:
        user = await self.get_by_id(telegram_id)
        if not user:
            return {}
            
        return {
            "clicks_count": user.clicks.clicks_count if user.clicks else 0,
            "farms_count": len(user.farms)
        }