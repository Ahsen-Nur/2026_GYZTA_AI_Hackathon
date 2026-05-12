from collections import Counter


def generate_analytics(orders):

    total_revenue = sum([
        o.revenue for o in orders
    ])

    delayed_orders = [

        o for o in orders
        if o.status == "Delayed"
    ]

    preparing_orders = [

        o for o in orders
        if o.status == "Preparing"
    ]

    shipped_orders = [

        o for o in orders
        if o.status == "Shipped"
    ]

    product_counter = Counter([
        o.product for o in orders
    ])

    city_counter = Counter([
        o.city for o in orders
    ])

    top_product = (
        product_counter.most_common(1)[0][0]
        if product_counter
        else "No Data"
    )

    top_city = (
        city_counter.most_common(1)[0][0]
        if city_counter
        else "Unknown"
    )

    delayed_rate = 0

    if len(orders) > 0:

        delayed_rate = round(

            (
                len(delayed_orders)
                / len(orders)
            ) * 100,

            1
        )

    if delayed_rate >= 40:

        risk_level = "High operational risk"

    elif delayed_rate >= 20:

        risk_level = "Medium operational risk"

    else:

        risk_level = "Low operational risk"

    if len(preparing_orders) > len(shipped_orders):

        demand_prediction = \
            "Order preparation load increasing"

    else:

        demand_prediction = \
            "Shipment flow stable"

    return {

        "top_product":
            top_product,

        "predicted_demand":
            demand_prediction,

        "risk_analysis":
            f"{risk_level} • %{delayed_rate} delayed",

        "active_customers":
            f"{len(orders)} active customers",

        "revenue":
            total_revenue,

        "top_city":
            top_city,

        "delayed_count":
            len(delayed_orders)
    }