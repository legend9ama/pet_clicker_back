from fastapi import HTTPException, status
from jose import jwt
from app.core.config import settings

async def validate_admin_token(token: str):
    try:
        payload = jwt.decode(
            token,
            settings.admin_secret_key,
            algorithms=["HS256"]
        )
        if payload.get("role") != "admin":
            raise HTTPException(status_code=403, detail="Forbidden")
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )