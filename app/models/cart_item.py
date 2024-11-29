from sqlalchemy import Column, Float, Integer


Base = declarative_base()


class CartItemBase(Base):
    __tablename__ = "cart_items"

    ci_id = Column(Integer, primary_key=True, index=True)
    cid = Column(Integer, nullable=False)  
    pid = Column(Integer, nullable=False)  
    quantity = Column(Integer, index=True, nullable=False)  
    price = Column(Float, nullable=False)  
    
