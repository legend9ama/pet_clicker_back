from fastapi import APIRouter, Depends, HTTPException, status, Header
from sqlalchemy.ext.asyncio import AsyncSession
from app.modules.users.schemas import (
    UserResponse,
    UserUpdate,
    LeaderboardUser
)
from app.modules.users.service import UserService
from app.modules.users.repository import UserRepository
from app.core.database import get_db
from app.core.telegram_validation import parse_telegram_data
from app.core.auth import validate_admin_token
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

router = APIRouter(prefix="/users", tags=["users"])
security = HTTPBearer()

@router.get("", response_model=list[LeaderboardUser])
async def get_leaderboard(
    db: AsyncSession = Depends(get_db)
):
    repo = UserRepository(db)
    service = UserService(repo)
    return await service.get_leaderboard()

@router.get("/me", response_model=UserResponse)
async def get_current_user(
    telegram_init_data: str = Header(..., alias="Telegram-Init-Data"),
    db: AsyncSession = Depends(get_db)
):
    repo = UserRepository(db)
    service = UserService(repo)
    return await service.get_or_create_user(telegram_init_data)

@router.get("/{telegram_id}", response_model=UserResponse)
async def get_user(
    telegram_id: int,
    db: AsyncSession = Depends(get_db)
):
    repo = UserRepository(db)
    service = UserService(repo)
    return await service.get_or_create_user(telegram_id)

@router.patch("/{telegram_id}", response_model=UserResponse)
async def update_user(
    telegram_id: int,
    update_data: UserUpdate,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db)
):
    await validate_admin_token(credentials.credentials)
    repo = UserRepository(db)
    service = UserService(repo)
    return await service.update_user(telegram_id, update_data)

@router.delete("/{telegram_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    telegram_id: int,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db)
):
    await validate_admin_token(credentials.credentials)
    repo = UserRepository(db)
    service = UserService(repo)
    await service.delete_user(telegram_id)