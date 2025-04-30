from fastapi import APIRouter, Depends, HTTPException, Header, Body
from sqlalchemy.ext.asyncio import AsyncSession
from app.modules.user_farm.service import UserFarmService
from app.modules.user_farm.repository import UserFarmRepository
from app.modules.farm_template.repository import FarmTemplateRepository
from app.modules.clicks.repository import ClickRepository
from app.modules.user_farm.schemas import *
from app.core.database import get_db
from typing import Annotated
from app.core.telegram_validation import validate_telegram_data, parse_telegram_data

router = APIRouter(prefix="/farms", tags=["farms"])

async def get_authenticated_user(
    telegram_init_data: Annotated[str, Header(alias="Telegram-Init-Data")]
) -> int:    
    user_data = await parse_telegram_data(telegram_init_data)
    return user_data.id

@router.get("/", response_model=list[UserFarmResponse])
async def get_farms(
    telegram_id: int = Depends(get_authenticated_user),
    db: AsyncSession = Depends(get_db)
):
    user_farm_repo = UserFarmRepository(db)
    farm_template_repo = FarmTemplateRepository(db)
    click_repo = ClickRepository(db)
    service = UserFarmService(user_farm_repo, farm_template_repo, click_repo)
    return await service.get_farms(telegram_id)

@router.post("/purchase", response_model=UserFarmPurchase)
async def purchase_farm(
    telegram_id: int = Depends(get_authenticated_user),
    data: UserFarmPurchase = Body(...),
    db: AsyncSession = Depends(get_db)
):
    user_farm_repo = UserFarmRepository(db)
    farm_template_repo = FarmTemplateRepository(db)
    click_repo = ClickRepository(db)
    service = UserFarmService(user_farm_repo, farm_template_repo, click_repo)
    return await service.purchase_farm(telegram_id, data)

@router.post("/{farmId}/collect", response_model=UserFarmCollectionResponse)
async def collect_farm(
    farm_id: int,
    telegram_id: int = Depends(get_authenticated_user),
    db: AsyncSession = Depends(get_db)
):
    user_farm_repo = UserFarmRepository(db)
    farm_template_repo = FarmTemplateRepository(db)
    click_repo = ClickRepository(db)
    service = UserFarmService(user_farm_repo, farm_template_repo, click_repo)
    return await service.collect_farm(telegram_id, farm_id)

@router.post("/{farm_id}/upgrade", response_model=UserFarmResponse)
async def upgrade_farm(
    farm_id: int,
    data: UserFarmUpgrade,
    telegram_id: int = Depends(get_authenticated_user),
    db: AsyncSession = Depends(get_db)
):
    user_farm_repo = UserFarmRepository(db)
    farm_template_repo = FarmTemplateRepository(db)
    click_repo = ClickRepository(db)
    service = UserFarmService(user_farm_repo, farm_template_repo, click_repo)
    return await service.upgrade_farm(telegram_id, farm_id, data)