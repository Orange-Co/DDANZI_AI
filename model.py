from sqlalchemy import Column, String, INT, BIGINT
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Product(Base):
   __tablename__ = "products"
   
   product_id = Column(String, primary_key=True)
   origin_name = Column(String, unique=True)
