from sqlalchemy import Column, Integer, String,Date
from ..db.database import Base
from pydantic import BaseModel, EmailStr, ConfigDict

class SalesmanBase(Base):
    __tablename__ = "salesman"

    sid = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    lname = Column(String)
    phone = Column(String)
    email = Column(String, unique=True, index=True)
    password_hash = Column(String)
    address = Column(String)
    created_at = Column(Date)
    updated_at = Column(Date)
    

class SalesmanResponse(BaseModel):
    id: int
    email: str
    role:str
    model_config = ConfigDict(
        from_attributes=True,
        arbitrary_types_allowed=True
    )
