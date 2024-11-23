from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional

class LoginRequest(BaseModel):
    email: EmailStr
    password: str
    role: int  # 2 for salesman, 3 for customer

    model_config = ConfigDict(
        from_attributes=True,
        arbitrary_types_allowed=True
    )