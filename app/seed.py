from random import choice
from random import randint

from app.database import engine
from app.database import SessionLocal

from app.models import Base
from app.models import Order
from app.models import Inventory

Base.metadata.drop_all(bind=engine)

Base.metadata.create_all(bind=engine)

db = SessionLocal()

customers = [

    "Ahsen Nur Aldaş",
    "Eda Nur Teklik",
    "Şevval Demir",
    "Mehmet Yılmaz",
    "Ayşe Kaya",
    "Burak Çetin",
    "Zeynep Arslan",
    "Ali Vural",
    "Merve Aksoy",
    "Can Yıldız",
    "Emre Demirtaş",
    "Elif Korkmaz",
    "Kaan Özdemir",
    "Seda Karaca",
    "Oğuz Şahin",
    "Fatma Kurt",
    "Murat Güneş",
    "Selin Yıldırım",
    "Berk Aydın",
    "Deniz Çelik"
]

products = [

    "Logitech MX Master 3S",
    "MacBook Air M2",
    "Apple Magic Keyboard",
    "Sony WH-1000XM5",
    "AirPods Pro",
    "Apple Watch Series 9",
    "RTX 4070",
    "Samsung SSD 2TB",
    "LG Ultragear Monitor",
    "iPad Air",
    "PlayStation 5 Controller",
    "SteelSeries Apex Pro",
    "Razer DeathAdder V3",
    "Huawei MatePad",
    "Dell XPS 15"
]

cities = [

    "İstanbul",
    "Ankara",
    "İzmir",
    "Bursa",
    "Antalya",
    "Gaziantep",
    "Konya",
    "Adana"
]

statuses = [

    "Shipped",
    "Preparing",
    "Delayed"
]

carriers = [

    "Yurtiçi Kargo",
    "MNG Kargo",
    "Aras Kargo",
    "Sürat Kargo",
    "Hepsijet"
]

priorities = [

    "Low",
    "Medium",
    "High",
    "Critical"
]

deliveries = [

    "Bugün",
    "Yarın",
    "2 Gün",
    "3 Gün",
    "Gecikmiş"
]

orders = []

for i in range(1, 26):

    product = choice(products)

    stock_status = choice(statuses)

    order = Order(

        customer=choice(customers),

        product=product,

        status=stock_status,

        city=choice(cities),

        tracking_number=f"TRX-{randint(100000,999999)}",

        revenue=randint(12000,95000),

        shipment_priority=choice(priorities),

        estimated_delivery=choice(deliveries),

        carrier=choice(carriers)
    )

    orders.append(order)

inventory_products = [

    "Logitech MX Master 3S",
    "MacBook Air M2",
    "Apple Magic Keyboard",
    "Sony WH-1000XM5",
    "AirPods Pro",
    "Apple Watch Series 9",
    "RTX 4070",
    "Samsung SSD 2TB",
    "LG Ultragear Monitor",
    "iPad Air",
    "PlayStation 5 Controller",
    "SteelSeries Apex Pro",
    "Razer DeathAdder V3",
    "Huawei MatePad",
    "Dell XPS 15"
]

inventory = []

for product in inventory_products:

    stock = randint(1,40)

    if stock <= 5:

        status = "Critical"

    elif stock <= 10:

        status = "Low"

    else:

        status = "Normal"

    item = Inventory(

        product=product,

        stock=stock,

        status=status,

        reorder_threshold=10,

        warehouse=choice([

            "İstanbul Depo",
            "Ankara Depo",
            "İzmir Depo",
            "Bursa Depo"

        ])
    )

    inventory.append(item)

db.add_all(orders)

db.add_all(inventory)

db.commit()

db.close()

print(
    "AI operasyon veritabanı başarıyla oluşturuldu."
)