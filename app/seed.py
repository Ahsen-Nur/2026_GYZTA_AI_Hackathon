from app.database import engine
from app.database import SessionLocal

from app.models import Base
from app.models import Order
from app.models import Inventory

Base.metadata.create_all(bind=engine)

db = SessionLocal()

db.query(Order).delete()
db.query(Inventory).delete()

orders = [

    Order(
        customer="Ahsen Nur Aldaş",
        product="Logitech MX Master 3S",
        status="Shipped",
        city="İstanbul",
        tracking_number="YK458921",
        revenue=45000
    ),

    Order(
        customer="Eda Nur Teklik",
        product="MacBook Air M2",
        status="Preparing",
        city="Ankara",
        tracking_number="TR928111",
        revenue=65000
    ),

    Order(
        customer="Şevval Demir",
        product="Apple Magic Keyboard",
        status="Delayed",
        city="Bursa",
        tracking_number="DG552200",
        revenue=33500
    )
]

inventory = [

    Inventory(
        product="Apple Magic Keyboard",
        stock=2,
        status="Critical"
    ),

    Inventory(
        product="Logitech MX Master 3S",
        stock=25,
        status="Normal"
    ),

    Inventory(
        product="MacBook Air M2",
        stock=5,
        status="Low"
    )
]

db.add_all(orders)
db.add_all(inventory)

db.commit()

db.close()

print("Database seeded successfully.")