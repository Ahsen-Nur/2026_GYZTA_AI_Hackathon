from fastapi import APIRouter

from app.database import SessionLocal
from app.models import Inventory

router = APIRouter()


@router.get("/inventory")
def inventory():

    db = SessionLocal()

    items = db.query(Inventory).all()

    result = []

    for i in items:

        result.append({

            "product":
                i.product,

            "stock":
                i.stock,

            "status":
                i.status,

            "reorder_threshold":
                i.reorder_threshold,

            "warehouse":
                i.warehouse
        })

    db.close()

    return result