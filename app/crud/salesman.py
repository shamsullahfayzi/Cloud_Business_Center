from datetime import date
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.crud.login import TokenResponse, process_login
from app.models.login_model import LoginRequest
from app.models.salesman import SalesmanBase
from ..core.security import get_password_hash
from typing import Optional

async def process_create_salesman(db:Session, salesman:SalesmanBase) -> Optional[TokenResponse]:
    try:
        
        # check if user exist with the givin email then create salesman and give him token
        exists = db.query(SalesmanBase).filter(SalesmanBase.email == salesman.email).first()
        if exists:
            raise HTTPException(status_code=400,detail="Salesman already exists. Try logging in instead") 
        # store plain password we will use it in login method then hash the password for db
        plain_pwd = salesman.password_hash
        pwd_hash = get_password_hash(plain_pwd)
        salesman.password_hash = pwd_hash
        salesman.created_at = date.today()
        salesman.updated_at = date.today()
        # salesman.rid = 2
        db.add(salesman)
        db.commit()
        db.refresh(salesman)
        # create a login request 
        login =  LoginRequest(email=salesman.email,password=plain_pwd,role=2)
        return await process_login(db,login)
        
    except Exception as e:
         db.rollback()
         raise HTTPException(status_code=500,detail=str(e))