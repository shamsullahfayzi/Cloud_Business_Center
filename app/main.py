# main.py
from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel, ConfigDict, EmailStr
from sqlalchemy.orm import Session

from .crud.customer import process_create_user
from .crud.product import process_create_product
from .crud.salesman import process_create_salesman
from .models.customer import CustomerBase
from .models.salesman import SalesmanBase
from .models.product import ProductBase
from .db import database
from .crud.login import process_login, TokenResponse
from .models.login_model import LoginRequest
from middleware import middleware
ROLE_CUSTOMER = "customer"
ROLE_SALESMAN = "salesman"
ROLE_ADMIN = "admin"
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

class SalesmanCreate(BaseModel):
    name: str
    lname: str
    phone: str
    email: EmailStr
    password: str
    address: str | None = None
    model_config = ConfigDict(
        from_attributes=True,
        arbitrary_types_allowed=True
    )

@app.post("/salesman/new/", response_model=TokenResponse)
async def salesman_new_endpoint(request:SalesmanCreate,db:Session = Depends(database.get_db)):
    
    # try to create an instance of base salesman 
    try:
        salesman = SalesmanBase(
            name = request.name,
            lname = request.lname,
            email = request.email,
            password_hash = request.password,
            
            address = request.address,
            phone = request.phone
        
        )
        result  = await process_create_salesman(db,salesman)
        if result:
            return result
        raise HTTPException(status_code=500,detail="Failed to create salesman")
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))


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

class Product_Create(BaseModel):
    sid:int
    pname:str
    pdescription:str
    price:float
    cid:int
    discount:float
    status:str
    wid:int
    stock_quantity:int
    volumeperunit:float
    weightperunit:float
    estimatedArrivalDate:str
    actualArrivalDate:str | None = None

    model_config = ConfigDict(
        from_attributes=True,
        arbitrary_types_allowed=True
    )


class Response_Product_Create(BaseModel):
    success:bool
    message:str
    data:dict | None = None
    error:dict | None = None

@app.post("/products/new/",response_model=Response_Product_Create)
@middleware.require_roles([ROLE_SALESMAN])
async def new_product_endpoint(request:Product_Create,db:Session = Depends(database.get_db)):
    try:
        # create instance of base model
        pb = ProductBase(
            sid=request.sid,
            pname=request.pname,
            pdescription=request.pdescription,
            price=request.price,
            discount=request.discount,
            status=request.status,
            wid=request.wid,
            cid=request.cid,
            volumeperunit=request.volumeperunit,
            weightperunit=request.weightperunit,
            stock_quantity=request.stock_quantity
        )
        product =  await process_create_product(db,pb,request.estimatedArrivalDate,request.actualArrivalDate)
        
        return product if product.success else HTTPException(status_code=500,detail={product.message,product.error})
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))
