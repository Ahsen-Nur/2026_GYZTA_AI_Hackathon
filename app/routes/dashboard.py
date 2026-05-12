from fastapi import APIRouter
import json

router = APIRouter()


@router.get("/dashboard-data")
def dashboard_data():

    with open(
        "app/data/orders.json",
        "r",
        encoding="utf-8"
    ) as file:

        orders = json.load(file)

    with open(
        "app/data/stock.json",
        "r",
        encoding="utf-8"
    ) as file:

        stock = json.load(file)

    total_orders = len(orders)

    delayed_orders = len([
        order for order in orders
        if order["status"] == "Delayed"
    ])

    critical_stock = len([
        item for item in stock
        if item["critical"] is True
    ])

    return {

        "stats": {

            "total_orders":
                total_orders,

            "delayed_orders":
                delayed_orders,

            "critical_stock":
                critical_stock,

            "revenue":
                "₺248K"
        },

        "orders":
            orders,

        "stock":
            stock,

        "insights": [

            "Apple Magic Keyboard stock dropped below critical threshold.",

            "Delayed cargo detected for Bursa shipments.",

            "AI predicts increased SSD demand within next 7 days.",

            "High customer activity detected in İstanbul region."

        ]
    }