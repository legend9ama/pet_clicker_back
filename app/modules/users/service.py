from fastapi import HTTPException, status
from app.models.user import User
from app.modules.users.repository import UserRepository
from app.modules.users.schemas import (
    UserCreate,
    UserResponse,
    UserUpdate,
    LeaderboardUser
)
from app.core.telegram_validation import parse_telegram_data
from app.core.config import settings
from typing import Optional

class UserService:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    async def get_or_create_user(self, init_data: str) -> UserResponse:
        user_data = await parse_telegram_data(init_data)
        existing_user = await self.repo.get_by_id(user_data.id)
        if existing_user:
            existing_user = await self.update_user(
                telegram_id=user_data.id,
                first_name=user_data.first_name,
                last_name=user_data.last_name,
                username=user_data.username,
                photo_url=user_data.photo_url
                )
            return existing_user
        
        new_user = UserCreate(
            telegram_id=user_data.id,
            first_name=user_data.first_name,
            last_name=user_data.last_name,
            username=user_data.username,
            photo_url=user_data.photo_url,
            
        )
        return await self.repo.create(new_user)

    async def get_leaderboard(self) -> list[LeaderboardUser]:
        users = await self.repo.get_leaderboard()
        return [
            LeaderboardUser(
                username=user.username,
                photo_url=user.photo_url,
                clicks_count=user.clicks.clicks_count if user.clicks else 0,
                position=i+1
            )
            for i, user in enumerate(users)
        ]
    
    async def update_user(
        self,
        telegram_id: int,
        first_name: str,
        last_name: Optional[str],
        username: Optional[str],
        photo_url: Optional[str],
    ) -> User:
        
        user = await self.repo.get_by_id(telegram_id)
        
        updates = {}
        if first_name and user.first_name != first_name:
            updates["first_name"] = first_name
        if last_name and user.last_name != last_name:
            updates["last_name"] = last_name
        if username and user.username != username:
            updates["username"] = username
        if photo_url and user.photo_url != photo_url:
            updates["photo_url"] = photo_url
        
        if updates:
            return await self.repo.update_user(telegram_id, updates)
        
        return user

    async def delete_user(self, telegram_id: int) -> None:
        success = await self.repo.delete(telegram_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

    async def _format_response(self, user: User) -> UserResponse:
        stats = await self.repo.get_user_stats(user.telegram_id)
        return UserResponse(
            telegram_id=user.telegram_id,
            username=user.username,
            created_at=user.created_at,
            referrer_id=user.referrer_id,
            **stats
        )