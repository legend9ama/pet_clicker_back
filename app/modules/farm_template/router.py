from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from app.modules.farm_template.service import FarmTemplateService
from app.modules.farm_template.repository import FarmTemplateRepository
from app.modules.farm_template.schemas import (
    FarmTemplateCreate,
    FarmTemplateUpdate,
    FarmTemplateResponse
)
from app.core.database import get_db
from app.core.security.auth import validate_admin_token

router = APIRouter(prefix="/admin/farms", tags=["Admin Farms"])
security = HTTPBearer()

@router.post("", response_model=FarmTemplateResponse, status_code=201)
async def create_farm_template(
    data: FarmTemplateCreate,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db)
):
    await validate_admin_token(credentials.credentials)
    repo = FarmTemplateRepository(db)
    service = FarmTemplateService(repo)
    return await service.create_template(data)

@router.get("", response_model=list[FarmTemplateResponse])
async def get_all_farm_templates(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db)
):
    await validate_admin_token(credentials.credentials)
    repo = FarmTemplateRepository(db)
    service = FarmTemplateService(repo)
    return await service.get_all_templates()

@router.get("/visible", response_model=list[FarmTemplateResponse])
async def get_all_visible_farm_templates(
    db: AsyncSession = Depends(get_db)
):
    repo = FarmTemplateRepository(db)
    service = FarmTemplateService(repo)
    return await service.get_all_visible_templates()

@router.get("/{farm_id}", response_model=FarmTemplateResponse)
async def get_farm_template(
    farm_id: int,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db)
):
    await validate_admin_token(credentials.credentials)
    repo = FarmTemplateRepository(db)
    service = FarmTemplateService(repo)
    return await service.get_template(farm_id)

@router.put("/{farm_id}", response_model=FarmTemplateResponse)
async def update_farm_template(
    farm_id: int,
    data: FarmTemplateUpdate,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db)
):
    await validate_admin_token(credentials.credentials)
    repo = FarmTemplateRepository(db)
    service = FarmTemplateService(repo)
    return await service.update_template(farm_id, data)

@router.delete("/{farm_id}", status_code=204)
async def delete_farm_template(
    farm_id: int,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db)
):
    await validate_admin_token(credentials.credentials)
    repo = FarmTemplateRepository(db)
    service = FarmTemplateService(repo)
    await service.delete_template(farm_id)

@router.patch("/{farm_id}/visibility", response_model=FarmTemplateResponse)
async def toggle_farm_visibility(
    farm_id: int,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db)
):
    await validate_admin_token(credentials.credentials)
    repo = FarmTemplateRepository(db)
    service = FarmTemplateService(repo)
    return await service.toggle_visibility(farm_id)