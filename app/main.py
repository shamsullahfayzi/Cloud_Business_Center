# main.py
from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel, ConfigDict, EmailStr
from sqlalchemy.orm import Session

from app.crud.user import process_create_user
from app.models.customer import CustomerBase
from .db import database
from .crud.login import process_login, TokenResponse
from .models.login_model import LoginRequest

app = FastAPI()

class CustomerCreate(BaseModel):
    uname: str
    lname: str
    email: EmailStr
    password: str
    address: str | None = None
    phone: str
    rid: int | None = None

    model_config = ConfigDict(
        from_attributes=True,
        arbitrary_types_allowed=True
    )

@app.post("/customer/new/", response_model=TokenResponse)
async def customer_new_endpoint(
    request: CustomerCreate, 
    db: Session = Depends(database.get_db)
):
    try:
        # Create a new CustomerBase instance
        db_customer = CustomerBase(
            uname=request.uname,
            lname=request.lname,
            email=request.email,
            password_hash=request.password,
            address=request.address,
            phone=request.phone,
            rid=request.rid
        )
        
        result = await process_create_user(db, db_customer)
        if result:
            return result
        raise HTTPException(status_code=401, detail="Failed to create user")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/login/", response_model=TokenResponse)
async def login_endpoint(
    request: LoginRequest,
    db: Session = Depends(database.get_db)
): 
    try:
        result = await process_login(db=db, login_data=request)
        if result:
            return result
        raise HTTPException(status_code=401, detail="Invalid credentials")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))