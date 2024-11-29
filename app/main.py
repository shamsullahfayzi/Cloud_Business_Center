from fastapi import FastAPI, Depends, HTTPException,Response,Request
from pydantic import BaseModel, ConfigDict, EmailStr
from sqlalchemy.orm import Session

from app.models.response_product_create import Response_Product_Create

from .crud.customer import process_create_user
from .crud.product import process_create_product
from .crud.salesman import process_create_salesman
from .models.customer import CustomerBase
from .models.salesman import SalesmanBase
from .models.product import ProductBase
from .db import database
from .crud.login import process_login, TokenResponse
from .models.login_model import LoginRequest

from .middleware.middleware import require_roles
ROLE_CUSTOMER = 3
ROLE_SALESMAN = 2
ROLE_ADMIN = 1
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
    res:Response,
    db: Session = Depends(database.get_db)
): 
    try:
        result = await process_login(db=db, login_data=request,res=res)
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


@app.post("/products/new/",response_model=Response_Product_Create)
@require_roles([ROLE_SALESMAN])
async def new_product_endpoint(request:Request,product:Product_Create,db:Session = Depends(database.get_db)):
    try:
        # create instance of base model
        pb = ProductBase(
            sid=product.sid,
            pname=product.pname,
            pdescription=product.pdescription,
            price=product.price,
            discount=product.discount,
            status=product.status,
            wid=product.wid,
            cid=product.cid,
            volumeperunit=product.volumeperunit,
            weightperunit=product.weightperunit,
            stock_quantity=product.stock_quantity,
            estimatedArrivalDate = product.estimatedArrivalDate,
            actualArrivalDate = "",
            
        )
        result =  await process_create_product(db,pb)
        
        return result if result.success else HTTPException(status_code=500,detail={result.message,})
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))
