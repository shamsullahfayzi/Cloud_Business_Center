# user.py
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.crud.login import TokenResponse, process_login
from app.models.login_model import LoginRequest
from ..models.customer import CustomerBase
from ..core.security import get_password_hash
from typing import Optional

async def process_create_user(db: Session, customer: CustomerBase) -> Optional[TokenResponse]:
    try:
        # Check if email exists
        exists = db.query(CustomerBase).filter(CustomerBase.email == customer.email).first()
        if exists:
            raise HTTPException(status_code=400, detail="Email already exists")
        
        # before assigning hash password to customer store the plain password in a var to use it in login
        plain_password = customer.password_hash 
        # Hash the password
        pwd_hash = get_password_hash(customer.password_hash)
        customer.password_hash = pwd_hash
        
        # Add and commit the new customer
        db.add(customer)
        db.commit()
        db.refresh(customer)
        # Process login and return token
        login_request = LoginRequest(
            email=customer.email,
            password=plain_password,     # Use the plain password
            role=customer.rid
        )
        
        return await process_login(db=db, login_data=login_request)
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))