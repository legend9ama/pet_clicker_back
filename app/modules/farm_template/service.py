from fastapi import HTTPException, status
from app.modules.farm_template.repository import FarmTemplateRepository
from app.modules.farm_template.schemas import FarmTemplateCreate, FarmTemplateUpdate, FarmTemplateResponse
from app.core.base_service import BaseService

class FarmTemplateService(BaseService):
    async def create_template(self, data: FarmTemplateCreate) -> FarmTemplateResponse:
        try:
            template = await self.repo.create(data.model_dump())
            return FarmTemplateResponse.model_validate(template)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error creating template: {str(e)}"
            )

    async def get_all_templates(self) -> list[FarmTemplateResponse]:
        templates = await self.repo.get_all()
        return [FarmTemplateResponse.model_validate(t) for t in templates]

    async def get_all_visible_templates(self) -> list[FarmTemplateResponse]:
        templates = await self.repo.get_all_visible()
        return [FarmTemplateResponse.model_validate(t) for t in templates]
    
    async def get_template(self, farm_id: int) -> FarmTemplateResponse:
        template = await self.repo.get_by_id(farm_id)
        if not template:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Farm template not found"
            )
        return FarmTemplateResponse.model_validate(template)

    async def update_template(self, farm_id: int, data: FarmTemplateUpdate) -> FarmTemplateResponse:
        template = await self.repo.update(farm_id, data.model_dump(exclude_unset=True))
        if not template:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Farm template not found"
            )
        return FarmTemplateResponse.model_validate(template)

    async def delete_template(self, farm_id: int) -> None:
        success = await self.repo.delete(farm_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Farm template not found"
            )

    async def toggle_visibility(self, farm_id: int) -> FarmTemplateResponse:
        template = await self.repo.toggle_visibility(farm_id)
        if not template:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Farm template not found"
            )
        return FarmTemplateResponse.model_validate(template)