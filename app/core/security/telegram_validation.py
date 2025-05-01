import hmac
import hashlib
from urllib.parse import parse_qsl
from app.modules.users.schemas import TelegramUserData
from app.core.config import settings
from fastapi import HTTPException
from urllib.parse import parse_qs
import json

async def validate_telegram_data(data: str, bot_token: str) -> bool:
    """
    https://core.telegram.org/bots/webapps#validating-data-received-via-the-mini-app
    """
    try:
        parsed_data = dict(parse_qsl(data))
        hash_value = parsed_data.pop('hash', '')
        
        data_check_string = "\n".join(
            f"{key}={value}"
            for key, value in sorted(parsed_data.items())
        )
        
        secret_key = hmac.new(
            key=b"WebAppData",
            msg=bot_token.encode(),
            digestmod=hashlib.sha256
        ).digest()
        
        calculated_hash = hmac.new(
            key=secret_key,
            msg=data_check_string.encode(),
            digestmod=hashlib.sha256
        ).hexdigest()
        
        return hmac.compare_digest(calculated_hash, hash_value)
    
    except Exception as e:
        return False
    
async def parse_telegram_data(init_data: str) -> TelegramUserData:
    if not await validate_telegram_data(init_data, settings.bot_token):
        raise HTTPException(status_code=401, detail="Invalid Telegram auth")
    parsed = parse_qs(init_data)
    user_data = json.loads(parsed['user'][0])
    
    return TelegramUserData(
        id=int(user_data.get('id')),
        first_name=user_data.get('first_name'),
        last_name=user_data.get('last_name'),
        username=user_data.get('username'),
        photo_url=user_data.get('photo_url')
    )