from app.database import engine, SessionLocal
from app.models import Base, Order, Inventory

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
        tracking_number="YK458921"
    ),

    Order(
        customer="Eda Nur Teklik",
        product="Apple Magic Keyboard",
        status="Preparing",
        city="Ankara",
        tracking_number="YK458922"
    ),

    Order(
        customer="Şevval Demir",
        product="Samsung Monitor",
        status="Delayed",
        city="Bursa",
        tracking_number="YK458923"
    )

]

inventory = [

    Inventory(
        product="Apple Magic Keyboard",
        stock=2,
        status="Critical"
    ),

    Inventory(
        product="Samsung Monitor",
        stock=1,
        status="Critical"
    ),

    Inventory(
        product="Logitech MX Master 3S",
        stock=24,
        status="Good"
    )

]

db.add_all(orders)
db.add_all(inventory)

db.commit()

print("Database seeded successfully.")