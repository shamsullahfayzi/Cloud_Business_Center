from datetime import date
import time
from typing import Optional

from fastapi import HTTPException
from app.main import Response_Product_Create
from app.models.product import ProductBase
from sqlalchemy.orm import Session
from app.models.warehouse import WarehouseBase
from app.models.shipment import ShipmentBase
from datetime import datetime

async def process_create_product(
    db: Session, product: ProductBase,estimatedArrivalDate:str,actualArrivalDate:str
) -> Optional[Response_Product_Create]:
    try:
        # check if we have enough capacity left in the given WAREHOUSE
        warehouse = db.query(WarehouseBase).filter(WarehouseBase.wid == product.wid).first();
        if not warehouse:
            raise HTTPException(status_code=404,detail="Warehouse not found")

        volumeCapacity = warehouse.capacity_volume
        weightCapacity = warehouse.capacity_weight
        if volumeCapacity >= product.volumeperunit and weightCapacity >= product.weightperunit:
            # we have enough capacity
            warehouse.capacity_volume = warehouse.capacity_volume - (product.volumeperunit * product.stock_quantity)
            warehouse.capacity_weight = warehouse.capacity_weight - (product.weightperunit * product.stock_quantity)
            # check if product is available but EstimatedArrivalDate is later
            if product.status != "Shipping" and datetime.strptime(estimatedArrivalDate,"%y-%m-%d").date() > date.today():
                raise HTTPException(status_code=400,detail="if product is not in warehouse status should be Shipping, or change estimated arrival date")

            product.created_at = date.today()
            product.updated_at = date.today()
            db.add(product)
            db.commit()
            db.refresh(product)

            # shipment
            shipment = ShipmentBase(
                ProductID=product.pid,
                WarehouseID=product.wid,
                Quantity=product.stock_quantity,
                Status=product.status,
                EstimatedArrivalDate=datetime.strptime(
                    estimatedArrivalDate, "%y-%m-%d"
                ).date(),
                ActualArrivalDate=datetime.strptime(
                    actualArrivalDate, "%y-%m-%d"
                ).date(),
            )
            db.add(shipment)
            db.commit()
            db.refresh(shipment)

            return Response_Product_Create(success=True,message="Product created successfully",data={product,shipment})
        else:
            return Response_Product_Create(success=False,message="Not enough space in warehouse",error={"Available Volume":volumeCapacity,"Available Weight":weightCapacity})

    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))
