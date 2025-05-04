import pytest
from app.modules.clicks.repository import ClickRepository
from app.models.click import Clicks
from app.models.user import User
from app.models.user_farm import UserFarm
from app.models.farm_template import FarmTemplate
from sqlalchemy.exc import NoResultFound

@pytest.mark.asyncio
async def test_get_clicks_not_found(repo: ClickRepository):
    result = await repo.get_clicks(999999)
    assert result is None

@pytest.mark.asyncio
async def test_increment_clicks_new_user(repo: ClickRepository):
    clicks = await repo.increment_clicks(telegram_id=1, amount=10)
    assert clicks.clicks_count == 10
    assert isinstance(clicks.updated_at, int)

@pytest.mark.asyncio
async def test_increment_clicks_existing_user(repo: ClickRepository):
    await repo.increment_clicks(telegram_id=2, amount=5)
    updated = await repo.increment_clicks(telegram_id=2, amount=3)
    assert updated.clicks_count == 8

@pytest.mark.asyncio
async def test_decrement_clicks_success(repo: ClickRepository):
    await repo.increment_clicks(telegram_id=3, amount=15)
    result = await repo.decrement_clicks(telegram_id=3, amount=7)
    assert result.clicks_count == 8

@pytest.mark.asyncio
async def test_decrement_insufficient_clicks(repo: ClickRepository):
    await repo.increment_clicks(telegram_id=4, amount=10)
    with pytest.raises(ValueError) as exc:
        await repo.decrement_clicks(telegram_id=4, amount=20)
    assert "Insufficient clicks balance" in str(exc.value)

@pytest.mark.asyncio
async def test_has_enough_clicks(repo: ClickRepository):
    await repo.increment_clicks(telegram_id=5, amount=25)
    assert await repo.has_enough_clicks(5, 20) is True
    assert await repo.has_enough_clicks(5, 30) is False

@pytest.mark.asyncio
async def test_upsert_clicks_conflict(repo: ClickRepository):
    await repo._upsert_clicks(telegram_id=6, amount=10)
    result = await repo._upsert_clicks(telegram_id=6, amount=5)
    assert result.clicks_count == 15