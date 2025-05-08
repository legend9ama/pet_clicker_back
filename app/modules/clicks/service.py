from fastapi import HTTPException, status
from app.modules.clicks.repository import ClickRepository
from app.modules.clicks.schemas import ClickIncrementRequest, ClickCreate, ClickDecrementRequest, ClickResponse
from app.core.config import settings
from app.core.base_service import BaseService

class ClickService(BaseService):
    async def process_increment(self, telegram_id: int, data: ClickIncrementRequest) -> ClickResponse:
        try:
            valid = await self.is_valid(telegram_id, data.amount)
            if valid:
                clicks = await self.repo.increment_clicks(telegram_id, data.amount)
            else:
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Error incrementing clicks: {str(e)}")
            return ClickResponse.model_validate(clicks)
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error incrementing clicks: {str(e)}")
    
    async def is_valid(self, telegram_id: int, amount: int) -> bool:
        clicks = await self.repo.get_clicks(telegram_id)
        time_passed = settings.unixtimestamp-clicks.updated_at
        if time_passed < 7 and amount <= 300:
            return True
        if time_passed < 20:
            return False
        if amount >= 5000:
            return False
        else:
            return True            
    
    async def process_decrement(self, telegram_id: int, data: ClickDecrementRequest) -> ClickResponse:
        try:
            clicks = await self.repo.decrement_clicks(
                telegram_id, 
                data.amount
            )
            return ClickResponse.model_validate(clicks)
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error decrementing clicks: {str(e)}"
            )

    async def get_or_create_current_clicks(self, telegram_id: int) -> ClickResponse:
        existing_clicks = await self.repo.get_clicks(telegram_id)
        if existing_clicks:
            return existing_clicks
        new_clicks = ClickCreate(telegram_id=telegram_id, clicks_count=0)
        return await self.repo.create(new_clicks)