def generate_insights(orders, inventory):

    insights = []

    delayed = [
        o.customer for o in orders
        if o.status == "Delayed"
    ]

    if delayed:

        insights.append(
            f"Geciken sipariş: {delayed[0]}"
        )

    critical = [
        i.product for i in inventory
        if i.stock < 5
    ]

    if critical:

        insights.append(
            f"Kritik stok: {critical[0]}"
        )

    insights.append(
        "İstanbul sipariş yoğunluğu arttı."
    )

    return insights