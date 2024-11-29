


from datetime import datetime, date
from typing import Optional
from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from app.models.product import ProductBase, ProductResponse
from app.models.response_product_create import Response_Product_Create
from app.models.shipment import ShipmentBase
from app.models.warehouse import WarehouseBase

async def process_create_product(
    db: Session, 
    product: ProductBase,
) -> Optional[Response_Product_Create]:
    try:
        # Validate dates
        try:    
            estimated_date = datetime.strptime(product.estimatedArrivalDate, "%Y-%m-%d").date()
            actual_date = datetime.strptime(product.actualArrivalDate, "%Y-%m-%d").date() if product.actualArrivalDate else None
        except ValueError:
            return Response_Product_Create(
                success=False,
                message="Invalid date format. Use YYYY-MM-DD",
            )

        # Fetch warehouse with error handling
        warehouse = db.query(WarehouseBase).filter(WarehouseBase.wid == product.wid).first()
        if not warehouse:
            return Response_Product_Create(
                success=False,
                message="Warehouse not found",
            )

        # Validate warehouse capacity
        total_volume_needed = product.volumeperunit * product.stock_quantity
        total_weight_needed = product.weightperunit * product.stock_quantity

        if (warehouse.capacity_volume < total_volume_needed or 
            warehouse.capacity_weight < total_weight_needed):
            return Response_Product_Create(
                success=False,
                message="Insufficient warehouse capacity.",
               
            )

        # Date and status validation
        if (product.status != "Shipping" and estimated_date > date.today()):
            return Response_Product_Create( 
                success=False,
                message="Invalid product status or estimated arrival date",
               
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
        )

    except SQLAlchemyError as db_error:
        db.rollback()
        return Response_Product_Create(
            success=False,
            message=f"Database error occurred {str(db_error)}",
            
        )
    except Exception as e:
        db.rollback()
        return Response_Product_Create(
            success=False,
            message=f"Unexpected error {str(e)}",
        )
