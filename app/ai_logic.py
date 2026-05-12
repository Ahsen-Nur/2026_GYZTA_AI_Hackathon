def generate_ai_response(message, orders):

    msg = message.lower()

    for order in orders:

        if (
            str(order.id) in msg
            or order.customer.lower() in msg
        ):

            return f"""
Merhaba {order.customer}.

Siparişiniz:
{order.product}

Durum:
{order.status}

Takip numarası:
{order.tracking_number}
"""

    if "stok" in msg:

        return """
Kritik stok seviyesinde ürünler mevcut.
Apple Magic Keyboard ve Samsung Monitor yeniden sipariş edilmelidir.
"""

    return """
Şunları sorabilirsiniz:

- Siparişim nerede?
- Stok durumu
- Geciken kargolar
"""