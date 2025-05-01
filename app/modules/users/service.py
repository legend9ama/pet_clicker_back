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

class UserService:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    async def get_or_create_user(self, init_data: str) -> UserResponse:
        user_data = await parse_telegram_data(init_data)
        existing_user = await self.repo.get_by_id(user_data.id)
        if existing_user:
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
        return [LeaderboardUser.model_validate(t) for t in users]
    
    async def update_user(self, telegram_id: int, data: UserUpdate) -> UserResponse:
        user = await self.repo.update(telegram_id, data.model_dump(exclude_unset=True))
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        return await self._format_response(user)

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