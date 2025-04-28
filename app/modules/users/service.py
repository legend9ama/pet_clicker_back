from fastapi import HTTPException, status
from app.models.user import User
from app.modules.users.repository import UserRepository
from app.modules.users.schemas import (
    UserCreateRequest,
    UserCreate,
    UserResponse,
    UserUpdate
)
from app.core.telegram_validation import validate_telegram_data
from app.core.config import settings

class UserService:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    async def _validate_telegram_data(self, init_data: str) -> dict:
        if not await validate_telegram_data(init_data, settings.bot_token()):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid Telegram authorization"
            )
        return UserResponse.parse_init_data(init_data)

    async def create_user(self, data: UserCreateRequest) -> UserResponse:
        telegram_data = await self._validate_telegram_data(data.init_data)
        existing_user = await self.repo.get_by_id(telegram_data['telegram_id'])
        
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User already exists"
            )

        if data.referrer_id:
            referrer = await self.repo.get_by_id(data.referrer_id)
            if not referrer:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Referrer not found"
                )

        user = await self.repo.create(UserCreate(
            **telegram_data,
            referrer_id=data.referrer_id
        ))
        return await self._format_response(user)

    async def get_user(self, telegram_id: int) -> UserResponse:
        user = await self.repo.get_by_id(telegram_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        return await self._format_response(user)

    async def update_user(self, telegram_id: int, data: UserUpdate) -> UserResponse:
        user = await self.repo.update(telegram_id, data.dict(exclude_unset=True))
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