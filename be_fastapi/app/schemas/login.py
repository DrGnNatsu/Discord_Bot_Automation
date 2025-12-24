from pydantic import BaseModel, Field
from pydantic import EmailStr

from app.enums.role import Role

"""
DTOs for user login functionality.
"""


class LoginResponseDTO(BaseModel):
    jwt_token: str
    token_type: str = "bearer"
    role: Role


class LoginRequestDTO(BaseModel):
    email: EmailStr = Field(..., alias="username")
    password: str = Field(..., min_length=1)

    class Config:
        populate_by_name = True