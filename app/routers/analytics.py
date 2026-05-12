from fastapi import APIRouter

from app.database import SessionLocal
from app.models import Order

from app.services.analytics_service import generate_analytics

router = APIRouter()


@router.get("/analytics")
def analytics():

    db = SessionLocal()

    orders = db.query(Order).all()

    result = generate_analytics(orders)

    db.close()

    return result