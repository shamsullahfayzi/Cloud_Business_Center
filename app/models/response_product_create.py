from pydantic import BaseModel, ConfigDict, EmailStr
from app.models.product import ProductBase
from pycharm_venv.Lib.re._constants import error
class Response_Product_Create(BaseModel):
    success: bool
    message: str
    # product: ProductBase | None = None
    # error:dict | None = None

    model_config = ConfigDict(
        from_attributes=True,
        arbitrary_types_allowed=True
    )
