from typing import List

from pydantic import BaseModel, ConfigDict


class Add_To_Cart_Create(BaseModel):
    cid:int | None = None
    productIds: List[int]
    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True)
