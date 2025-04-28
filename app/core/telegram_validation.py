import hmac
import hashlib
from urllib.parse import parse_qsl

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