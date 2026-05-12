from app.models import Order


def generate_analytics(orders):

    delayed = len([
        o for o in orders
        if o.status == "Delayed"
    ])

    revenue = sum([
        o.revenue for o in orders
    ])

    return {

        "top_product":
            "Logitech MX Master 3S",

        "predicted_demand":
            "%24 Elektronik Artışı",

        "risk_analysis":
            f"{delayed} geciken gönderi",

        "active_customers":
            f"{len(orders)} aktif müşteri",

        "revenue":
            revenue
    }