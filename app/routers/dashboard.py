from fastapi import APIRouter

from app.database import SessionLocal

from app.models import Order
from app.models import Inventory

from app.services.analytics_service import (
    generate_analytics
)

from app.services.insight_service import (
    generate_insights
)

router = APIRouter()


@router.get("/dashboard")
def dashboard():

    db = SessionLocal()

    orders = db.query(Order).all()

    inventory = db.query(Inventory).all()

    analytics = generate_analytics(
        orders
    )

    insights = generate_insights(
        orders,
        inventory
    )

    delayed_orders = len([

        o for o in orders
        if o.status == "Delayed"
    ])

    critical_stock = len([

        i for i in inventory
        if i.stock <= 5
    ])

    response = {

        "total_orders":
            len(orders),

        "delayed_orders":
            delayed_orders,

        "critical_stock":
            critical_stock,

        "revenue":
            analytics["revenue"],

        "insights":
            insights,

        "top_city":
            analytics["top_city"],

        "delayed_count":
            analytics["delayed_count"]
    }

    db.close()

    return response