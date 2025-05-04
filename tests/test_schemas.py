import pytest
from pydantic import ValidationError
from app.modules.clicks.schemas import (
    ClickIncrementRequest,
    ClickDecrementRequest,
    ClickResponse
)

def test_valid_increment_request():
    valid_data = {"amount": 10, "source": "manual"}
    request = ClickIncrementRequest(**valid_data)
    assert request.amount == 10
    assert request.source == "manual"

def test_invalid_amount_increment():
    with pytest.raises(ValidationError):
        ClickIncrementRequest(amount=-5, source="manual")

def test_invalid_source_value():
    with pytest.raises(ValidationError):
        ClickIncrementRequest(amount=10, source="invalid")

def test_valid_decrement_request():
    valid_data = {"amount": 5}
    request = ClickDecrementRequest(**valid_data)
    assert request.amount == 5

def test_click_response_validation():
    valid_data = {
        "telegram_id": 123,
        "clicks_count": 100,
        "updated_at": 1678901234
    }
    response = ClickResponse(**valid_data)
    assert response.clicks_count == 100

def test_negative_clicks_response():
    with pytest.raises(ValidationError):
        ClickResponse(
            telegram_id=123,
            clicks_count=-50,
            updated_at=1678901234
        )