from pydantic import BaseModel, EmailStr


class UserRegisterRequest(BaseModel):
    name: str
    email: EmailStr
    password: str


class UserRegisterResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
