from sqlalchemy import Column, Integer, String
from app.database import Base


class Order(Base):

    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)

    customer = Column(String)
    product = Column(String)
    status = Column(String)
    city = Column(String)
    tracking_number = Column(String)


class Inventory(Base):

    __tablename__ = "inventory"

    id = Column(Integer, primary_key=True, index=True)

    product = Column(String)
    stock = Column(Integer)
    status = Column(String)