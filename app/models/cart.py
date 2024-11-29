from sqlalchemy import Column, Date, Integer, String
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

class CartBase(Base):
    __tablename__ = "cart"

    cid = Column(Integer, primary_key=True, index=True)
    custid = Column(Integer, nullable=False)  
    created_at = Column(Date, nullable=False)  # User's last name
    status = Column(String, unique=True, index=True, nullable=False)  # Unique email
