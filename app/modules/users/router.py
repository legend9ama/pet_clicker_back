from fastapi import APIRouter, Depends, HTTPException, status, Header
from sqlalchemy.ext.asyncio import AsyncSession
from app.modules.users.schemas import (
    UserResponse,
    UserUpdate
)
from app.modules.users.service import UserService
from app.modules.users.repository import UserRepository
from app.core.database import get_db

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/me", response_model=UserResponse)
async def get_current_user(
    init_data: str = Header(..., alias="Telegram-Init-Data"),
    db: AsyncSession = Depends(get_db)
):
    repo = UserRepository(db)
    service = UserService(repo)
    telegram_data = await service._validate_telegram_data(init_data)
    return await service.get_user(telegram_data['telegram_id'])

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
    db: AsyncSession = Depends(get_db)
):
    repo = UserRepository(db)
    service = UserService(repo)
    return await service.update_user(telegram_id, update_data)

@router.delete("/{telegram_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    telegram_id: int,
    db: AsyncSession = Depends(get_db)
):
    repo = UserRepository(db)
    service = UserService(repo)
    await service.delete_user(telegram_id)