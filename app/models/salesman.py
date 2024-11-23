from sqlalchemy import Column, Integer, String
from ..db.database import Base
from pydantic import BaseModel, EmailStr, ConfigDict

class SalesmanBase(Base):
    __tablename__ = "salesmen"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password_hash = Column(String)

class SalesmanResponse(BaseModel):
    id: int
    email: str

    model_config = ConfigDict(
        from_attributes=True,
        arbitrary_types_allowed=True
    )