from sqlalchemy import Column, Date, Integer, String, Float
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class ShipmentBase(Base):
    __tablename__ = "shipment"

    ShipmentID = Column(Integer, primary_key=True, index=True)
    ProductID = Column(Integer, nullable=False)
    WarehouseID = Column(Integer, nullable=False)
    Quantity = Column(Integer, nullable=False)
    Status = Column(String, nullable=False)
    EstimatedArrivalDate = Column(Date)
    ActualArrivalDate = Column(Date)