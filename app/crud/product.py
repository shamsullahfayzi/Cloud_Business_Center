from datetime import date
import time
from typing import Optional

from fastapi import HTTPException
from app.models.product import ProductBase
from sqlalchemy.orm import Session
from app.models.response_product_create import Response_Product_Create
from app.models.warehouse import WarehouseBase
from app.models.shipment import ShipmentBase
from datetime import datetime

# async def process_create_product(
#     db: Session, product: ProductBase,estimatedArrivalDate:str,actualArrivalDate:str
# ) -> Optional[Response_Product_Create]:
#     try:
#         # check if we have enough capacity left in the given WAREHOUSE
#         warehouse = db.query(WarehouseBase).filter(WarehouseBase.wid == product.wid).first();
#         if not warehouse:
#             raise HTTPException(status_code=404,detail="Warehouse not found")

#         volumeCapacity = warehouse.capacity_volume
#         weightCapacity = warehouse.capacity_weight
#         if volumeCapacity >= product.volumeperunit and weightCapacity >= product.weightperunit:
#             # we have enough capacity
#             warehouse.capacity_volume = warehouse.capacity_volume - (product.volumeperunit * product.stock_quantity)
#             warehouse.capacity_weight = warehouse.capacity_weight - (product.weightperunit * product.stock_quantity)
#             # check if product is available but EstimatedArrivalDate is later
#             if product.status != "Shipping" and datetime.strptime(estimatedArrivalDate,"%y-%m-%d").date() > date.today():
#                 raise HTTPException(status_code=400,detail="if product is not in warehouse status should be Shipping, or change estimated arrival date")

#             product.created_at = date.today()
#             product.updated_at = date.today()
#             db.add(product)
#             db.commit()
#             db.refresh(product)

#             # shipment
#             shipment = ShipmentBase(
#                 ProductID=product.pid,
#                 WarehouseID=product.wid,
#                 Quantity=product.stock_quantity,
#                 Status=product.status,
#                 EstimatedArrivalDate=datetime.strptime(
#                     estimatedArrivalDate, "%y-%m-%d"
#                 ).date(),
#                 ActualArrivalDate=datetime.strptime(
#                     actualArrivalDate, "%y-%m-%d"
#                 ).date(),
#             )
#             db.add(shipment)
#             db.commit()
#             db.refresh(shipment)

#             return Response_Product_Create(success=True,message="Product created successfully",data={product,shipment})
#         else:
#             return Response_Product_Create(success=False,message="Not enough space in warehouse",error={"Available Volume":volumeCapacity,"Available Weight":weightCapacity})

#     except Exception as e:
#         raise HTTPException(status_code=500,detail=str(e))


from datetime import datetime, date
from typing import Optional
from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

async def process_create_product(
    db: Session, 
    product: ProductBase,
) -> Response_Product_Create:
    try:
        # Validate dates
        try:
            estimated_date = datetime.strptime(product.estimatedArrivalDate, "%Y-%m-%d").date()
            actual_date = datetime.strptime(product.actualArrivalDate, "%Y-%m-%d").date() if product.actualArrivalDate else None
        except ValueError:
            return Response_Product_Create(
                success=False,
                message="Invalid date format",
                error={"date_format": "Use YYYY-MM-DD"}
            )

        # Fetch warehouse with error handling
        warehouse = db.query(WarehouseBase).filter(WarehouseBase.wid == product.wid).first()
        if not warehouse:
            return Response_Product_Create(
                success=False,
                message="Warehouse not found",
                error={"warehouse_id": product.wid}
            )

        # Validate warehouse capacity
        total_volume_needed = product.volumeperunit * product.stock_quantity
        total_weight_needed = product.weightperunit * product.stock_quantity

        if (warehouse.capacity_volume < total_volume_needed or 
            warehouse.capacity_weight < total_weight_needed):
            return Response_Product_Create(
                success=False,
                message="Insufficient warehouse capacity",
                error={
                    "available_volume": warehouse.capacity_volume,
                    "available_weight": warehouse.capacity_weight
                }
            )

        # Date and status validation
        if (product.status != "Shipping" and estimated_date > date.today()):
            return Response_Product_Create( 
                success=False,
                message="Invalid product status or estimated arrival date",
                error={
                    "status": product.status,
                    "estimated_date": estimated_date
                }
            )

        # Update warehouse capacity
        warehouse.capacity_volume -= total_volume_needed
        warehouse.capacity_weight -= total_weight_needed

        # Set timestamps
        product.created_at = date.today()
        product.updated_at = date.today()

        # Create product and shipment in a transaction
        db.add(product)
        db.commit()
        db.refresh(product)
        shipment = ShipmentBase(
            ProductID=product.pid,
            WarehouseID=product.wid,
            Quantity=product.stock_quantity,
            Status=product.status,
            EstimatedArrivalDate=estimated_date,
            ActualArrivalDate=actual_date
        )
        db.add(shipment)
        db.commit()

        db.refresh(shipment)

        return Response_Product_Create(
            success=True,
            message="Product created successfully",
            data={"product": product, "shipment": shipment}
        )

    except SQLAlchemyError as db_error:
        db.rollback()
        return Response_Product_Create(
            success=False,
            message="Database error occurred",
            error={"details": str(db_error)}
        )
    except Exception as e:
        db.rollback()
        return Response_Product_Create(
            success=False,
            message="Unexpected error",
            error={"details": str(e)}
        )
