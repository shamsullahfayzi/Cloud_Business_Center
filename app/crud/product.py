from datetime import date
from typing import Optional

from fastapi import HTTPException
from app.main import Response_Product_Create
from app.models.product import ProductBase
from sqlalchemy.orm import Session


async def process_create_product(
    db: Session, product: ProductBase
) -> Optional[Response_Product_Create]:
    try:
        product.created_at = date.today()
        product.updated_at = date.today()
        db.add(product)
        db.commit()
        db.refresh(product)
        return Response_Product_Create(success=True,message="Product created successfully",data=product)
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))
