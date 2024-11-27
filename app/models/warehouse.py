from sqlalchemy import Column, Date, Integer, String, Float
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
class WarehouseBase(Base):  
    __tablename__ = "warehouse"
    wid = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    location = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    capacity_volume = Column(Integer, nullable=False)
    capacity_weight = Column(Integer, nullable=False)
