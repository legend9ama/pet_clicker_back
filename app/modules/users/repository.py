from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from app.models.user import User
from app.modules.users.schemas import UserCreate

class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, user: UserCreate) -> User:
        new_user = User(
            telegram_id=user.telegram_id,
            username=user.username,
            referrer_id=user.referrer_id
        )
        self.db.add(new_user)
        await self.db.commit()
        await self.db.refresh(new_user)
        return new_user

    async def get_by_id(self, telegram_id: int) -> User | None:
        result = await self.db.execute(
            select(User).where(User.telegram_id == telegram_id)
        )
        return result.scalars().first()

    async def get_or_create(self, user_data: dict) -> User:
        user = await self.get_by_id(user_data.telegram_id)
        if user:
            return user
        new_user = User(**user_data)
        self.db.add(new_user)
        await self.db.commit()
        return new_user

    async def update(self, telegram_id: int, data: dict) -> User | None:
        stmt = (
            update(User)
            .where(User.telegram_id == telegram_id)
            .values(**data)
            .returning(User)
        )
        result = await self.db.execute(stmt)
        await self.db.commit()
        return result.scalars().first()

    async def delete(self, telegram_id: int) -> bool:
        stmt = delete(User).where(User.telegram_id == telegram_id)
        result = await self.db.execute(stmt)
        await self.db.commit()
        return result.rowcount > 0

    async def get_user_stats(self, telegram_id: int) -> dict:
        user = await self.get_by_id(telegram_id)
        if not user:
            return {}
            
        return {
            "clicks_count": user.clicks.clicks_count if user.clicks else 0,
            "farms_count": len(user.farms)
        }