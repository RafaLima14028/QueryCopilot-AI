from fastapi import (
    Depends,
    HTTPException,
    status
)

from app.core.security import verify_token


def required_role(allowed_roles: list[str]):
    def role_checker(
        user: dict = Depends(verify_token)
    ) -> dict:
        user_roles = user.get("roles", [])

        if not any(
            role in user_roles for role in allowed_roles
        ):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permission"
            )

        return user

    return role_checker
