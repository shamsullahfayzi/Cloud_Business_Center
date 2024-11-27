from pydantic import BaseModel, ConfigDict, EmailStr
class Response_Product_Create(BaseModel):
    success: bool
    message: str
    data: dict | None = None
    error: dict | None = None
