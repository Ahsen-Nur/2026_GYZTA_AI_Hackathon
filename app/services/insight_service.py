from collections import Counter


def generate_insights(
    orders,
    inventory
):

    insights = []

    delayed_orders = [

        o for o in orders
        if o.status == "Delayed"
    ]

    if delayed_orders:

        delayed_customers = ", ".join([

            o.customer
            for o in delayed_orders
        ])

        insights.append(

            f"""
AI shipment monitor gecikme tespit etti.
Etkilenen müşteriler:
{delayed_customers}
"""
        )

    critical_stock = [

        i for i in inventory
        if i.stock <= 5
    ]

    if critical_stock:

        for item in critical_stock:

            insights.append(

                f"""
{item.product} kritik stok seviyesinde.
AI sistem otomatik restock öneriyor.
"""
            )

    city_counter = Counter([
        o.city for o in orders
    ])

    if city_counter:

        top_city = city_counter.most_common(1)[0]

        insights.append(

            f"""
En yoğun sipariş bölgesi:
{top_city[0]}

Toplam sipariş:
{top_city[1]}
"""
        )

    revenue = sum([
        o.revenue for o in orders
    ])

    insights.append(

        f"""
Toplam operasyon hacmi:
₺{revenue}

AI engine satış performansını analiz ediyor.
"""
    )

    preparing = len([

        o for o in orders
        if o.status == "Preparing"
    ])

    shipped = len([

        o for o in orders
        if o.status == "Shipped"
    ])

    if preparing > shipped:

        insights.append(

            """
Sipariş hazırlama yoğunluğu arttı.
Ek operasyon desteği öneriliyor.
"""
        )

    else:

        insights.append(

            """
Shipment akışı stabil görünüyor.
Teslimat performansı normal seviyede.
"""
        )

    return insights