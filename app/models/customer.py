from sqlalchemy import Column, Integer, String
from pydantic import BaseModel, EmailStr, ConfigDict
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

Base = declarative_base()

class CustomerBase(Base):
    __tablename__ = "customer"
    
    uid = (Column(Integer, primary_key=True, index=True))
    uname = (Column(String, nullable=False))# User's first name
    lname = (Column(String, nullable=False))# User's last name
    email = (Column(String, unique=True, index=True, nullable=False))  # Unique email
    password_hash =(Column(String, nullable=False))  # Hashed password
    address =(Column(String))  # Address is optional
    phone = (Column(String, nullable=False))  # Phone number is required
    rid = Column(Integer, nullable=True)  # Reference to another table (optional)


class UserResponse(BaseModel):
    id: int
    email: str
    role:str
    model_config = ConfigDict(
        from_attributes=True,
        arbitrary_types_allowed=True
    )