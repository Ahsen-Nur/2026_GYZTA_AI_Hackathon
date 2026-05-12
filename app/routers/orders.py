from fastapi import APIRouter

from app.database import SessionLocal
from app.models import Order

router = APIRouter()


@router.get("/orders")
def get_orders():

    db = SessionLocal()

    orders = db.query(Order).all()

    result = []

    for o in orders:

        result.append({

            "id": o.id,

            "customer": o.customer,

            "product": o.product,

            "status": o.status,

            "city": o.city
        })

    db.close()

    return result