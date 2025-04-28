from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.modules.user_farm.service import UserFarmService
from app.modules.user_farm.repository import UserFarmRepository
from app.modules.farm_template.repository import FarmTemplateRepository
from app.modules.clicks.repository import ClickRepository
from app.modules.user_farm.schemas import *
from app.core.database import get_db
from app.core.telegram_validation import validate_telegram_data

router = APIRouter(prefix="/farms", tags=["farms"])

@router.get("/", response_model=list[UserFarmResponse])
async def get_farms(
    telegram_id: int = Depends(validate_telegram_data),
    db: AsyncSession = Depends(get_db)
):
    user_farm_repo = UserFarmRepository(db)
    farm_template_repo = FarmTemplateRepository(db)
    click_repo = ClickRepository(db)
    service = UserFarmService(user_farm_repo, farm_template_repo, click_repo)
    return await service.get_farms(telegram_id)

@router.post("/purchase", response_model=UserFarmResponse)
async def purchase_farm(
    data: UserFarmPurchase,
    telegram_id: int = Depends(validate_telegram_data),
    db: AsyncSession = Depends(get_db)
):
    user_farm_repo = UserFarmRepository(db)
    farm_template_repo = FarmTemplateRepository(db)
    click_repo = ClickRepository(db)
    service = UserFarmService(user_farm_repo, farm_template_repo, click_repo)
    return await service.purchase_farm(telegram_id, data)

@router.post("/{farm_id}/upgrade", response_model=UserFarmResponse)
async def upgrade_farm(
    farm_id: int,
    data: UserFarmUpgrade,
    telegram_id: int = Depends(validate_telegram_data),
    db: AsyncSession = Depends(get_db)
):
    user_farm_repo = UserFarmRepository(db)
    farm_template_repo = FarmTemplateRepository(db)
    click_repo = ClickRepository(db)
    service = UserFarmService(user_farm_repo, farm_template_repo, click_repo)
    return await service.upgrade_farm(telegram_id, farm_id, data)