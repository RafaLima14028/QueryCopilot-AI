from pydantic import BaseModel, EmailStr, IPvAnyAddress, field_validator
from typing import Union
import ipaddress
import re
from fastapi import HTTPException, status


class UserRegisterRequest(BaseModel):
    name: str
    email: EmailStr
    password: str
    is_admin: bool = False


class UserRegisterResponse(BaseModel):
    id: int
    name: str
    email: EmailStr


class UserRegiserDbRequest(BaseModel):
    host: str
    port: int
    db_name: str
    user: str
    password: str
    ssl_mode_enable: bool = True

    @field_validator("host")
    def validate_host(cls, v):
        try:
            ipaddress.ip_address(v)
            return v
        except ValueError:
            pass

        hostname_regex = r"^(?=.{1,253}$)([a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}$"

        if re.match(hostname_regex, v):
            return v

        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            "The host must be a valid IP address or a valid domain name"
        )


class UserRegiserDbResponse(BaseModel):
    sucess: bool = True
