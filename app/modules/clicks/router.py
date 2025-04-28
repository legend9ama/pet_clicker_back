from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.modules.clicks.service import ClickService
from app.modules.clicks.repository import ClickRepository
from app.modules.clicks.schemas import (
    ClickIncrementRequest,
    ClickDecrementRequest,
    ClickResponse
)
from app.core.database import get_db
from app.core.telegram_validation import validate_telegram_data
from app.core.config import settings
from urllib.parse import parse_qs
import json

router = APIRouter(prefix="/clicks", tags=["clicks"])

async def get_authenticated_user(init_data: str) -> int:
    # Validate Telegram WebApp data
    if not await validate_telegram_data(init_data, settings.bot_token):
        raise HTTPException(
            status_code=401, 
            detail="Invalid Telegram authentication"
        )
    
    # Parse user ID from initData
    parsed_data = parse_qs(init_data)
    user_data = json.loads(parsed_data.get('user', ['{}'])[0])
    return int(user_data['id'])

@router.post("/increment", response_model=ClickResponse)
async def increment_clicks(
    request: ClickIncrementRequest,
    init_data: str,
    db: AsyncSession = Depends(get_db)
):
    user_id = await get_authenticated_user(init_data)
    repo = ClickRepository(db)
    service = ClickService(repo)
    return await service.process_increment(user_id, request)

@router.post("/decrement", response_model=ClickResponse)
async def decrement_clicks(
    request: ClickDecrementRequest,
    init_data: str,
    db: AsyncSession = Depends(get_db)
):
    user_id = await get_authenticated_user(init_data)
    repo = ClickRepository(db)
    service = ClickService(repo)
    return await service.process_decrement(user_id, request)

@router.get("/", response_model=ClickResponse)
async def get_clicks(
    init_data: str,
    db: AsyncSession = Depends(get_db)
):
    user_id = await get_authenticated_user(init_data)
    repo = ClickRepository(db)
    service = ClickService(repo)
    return await service.get_current_clicks(user_id)