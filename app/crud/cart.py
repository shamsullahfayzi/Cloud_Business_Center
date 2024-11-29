from datetime import date
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.crud.login import TokenResponse, process_login
from app.models.login_model import LoginRequest
from app.models.salesman import SalesmanBase
from ..core.security import get_password_hash
from typing import Optional

async def existingCart(db:Session,cid:int) -> bool:
    pass 