import os
from fastapi import HTTPException,Response
from sqlalchemy.orm import Session
from ..models.login_model import LoginRequest
from ..models.customer import CustomerBase, UserResponse
from ..models.salesman import SalesmanBase, SalesmanResponse
from ..core.security import verify_password, create_access_token
from datetime import datetime, timedelta
from typing import Optional, Dict, Union
from pydantic import BaseModel
from jose import jwt
ACCESS_TOKEN_EXPIRE_MINUTES = 120
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key")
ALGORITHM = "HS256"
class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    user_data: Union[UserResponse, SalesmanResponse]

async def process_login(db: Session, login_data: LoginRequest,res:Response) -> Optional[TokenResponse]:
    """
    Process login request and return access token if successful
    """
    if login_data.role == 3:  # customer
        user = db.query(CustomerBase).filter(
            CustomerBase.email == login_data.email
        ).first()
        if not user :            
            raise HTTPException(status_code=401,detail="Invalid Email or Password")
        if not verify_password(login_data.password, user.password_hash):
            raise HTTPException(status_code=401,detail="Invalid Email or Password")
        token_data = {
            "sub":login_data.email,
            "role":login_data.role,
            "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),  # Expiration
            "id":user.uid
        }
        create_token = jwt.encode(token_data,SECRET_KEY,algorithm=ALGORITHM)
        res.set_cookie(
            
            key="access_token",
            value=create_token,
            httponly=True,secure=True,
            samesite="strict",
            max_age=ACCESS_TOKEN_EXPIRE_MINUTES*60
            )
        return TokenResponse(
            access_token="",
            token_type="",
            user_data=UserResponse(id=user.uid,email=user.email,role="customer")
        )
            
    elif login_data.role == 2:  # salesman
        salesman = db.query(SalesmanBase).filter(
            SalesmanBase.email == login_data.email
        ).first()
        
        if not salesman:
            raise HTTPException(status_code=401,detail="Invalid email or password")
        if not verify_password(login_data.password,salesman.password_hash):
            raise HTTPException(status_code=401,detail="Invalid email or password")
            
        token_data = {
            "sub":login_data.email,
            "role":login_data.role,
            "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES), # Expiration
            "id":salesman.sid,
            
        }
        create_token = jwt.encode(token_data,SECRET_KEY,algorithm=ALGORITHM)
        res.set_cookie(key="access_token",value=create_token,httponly=True,secure=False,samesite="strict",max_age=ACCESS_TOKEN_EXPIRE_MINUTES*60)

        return TokenResponse(
            access_token="",
            token_type="",
            user_data = SalesmanResponse(id = salesman.sid,email=salesman.email,role="salesman")
        )
    
    return None 
