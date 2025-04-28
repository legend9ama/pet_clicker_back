from fastapi import HTTPException, status
from app.modules.clicks.repository import ClickRepository
from app.modules.clicks.schemas import (
    ClickIncrementRequest,
    ClickDecrementRequest,
    ClickResponse
)

class ClickService:
    def __init__(self, repo: ClickRepository):
        self.repo = repo

    async def process_increment(self, telegram_id: int, data: ClickIncrementRequest) -> ClickResponse:
        try:
            clicks = await self.repo.increment_clicks(telegram_id, data.amount)
            return ClickResponse.model_validate(clicks)
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error incrementing clicks: {str(e)}")

    async def process_decrement(self, telegram_id: int, data: ClickDecrementRequest) -> ClickResponse:
        try:
            clicks = await self.repo.decrement_clicks(
                telegram_id, 
                data.amount
            )
            return ClickResponse.from_orm(clicks)
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

    async def get_current_clicks(self, telegram_id: int) -> ClickResponse:
        clicks = await self.repo.get_clicks(telegram_id)
        if not clicks:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Clicks record not found"
            )
        return ClickResponse.model_validate(clicks)