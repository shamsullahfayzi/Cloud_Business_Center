from sqlalchemy import Column, Date, Integer, String, Float
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class ProductBase(Base):
    __tablename__ = "product"

    pid = Column(Integer, primary_key=True, index=True)
    sid = Column(Integer,nullable=False)
    pname = Column(String, nullable=False)
    pdescription = Column(String,nullable=False)
    price = Column(Float, nullable=False)
    stock_quantity = Column(Integer, nullable=False)
    discount = Column(Float,nullable=True)
    status = Column(Float,nullable=False)
    wid = Column(Float,nullable=False)
    cid = Column(Float,nullable=False)
    created_at = Column(Date),
    updated_at = (Column(Date))

class ProductResponse(BaseModel):
    id: int
    name: str
    description: str | None
    price: float
    stock: int
    image: str | None

    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True)
