from fastapi import HTTPException, status
import bcrypt
import jwt
from datetime import (
    datetime,
    timedelta,
    timezone
)

from app.core.settings import get_settings


def create_acess_token(data: dict) -> str:
    to_encode = data.copy()

    settings = get_settings()

    now = datetime.now(timezone.utc)
    expire = now + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )

    to_encode.update({
        "exp": expire,
        "iat": now,
        "type": "access"
    })

    return jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=[settings.ALGORITHM]
    )


def verify_token(token: str) -> dict:
    try:
        pass
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Expired Token"
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Token"
        )
    except:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unknown Error in Token"
        )


def hash_password(password: str) -> bytes:
    salt = bcrypt.gensalt()

    return bcrypt.hashpw(
        password.encode(),
        salt
    )


def verify_password(
    password: str,
    hashed_password: bytes
) -> bool:
    return bcrypt.checkpw(
        password.encode(),
        hashed_password
    )
