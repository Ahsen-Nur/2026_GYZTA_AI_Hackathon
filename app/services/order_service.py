import json
import re


def load_orders():

    with open("app/data/orders.json", "r", encoding="utf-8") as file:
        return json.load(file)


def extract_order_id(message):

    numbers = re.findall(r'\d+', message)

    if numbers:
        return int(numbers[0])

    return None


def find_order(order_id):

    orders = load_orders()

    for order in orders:
        if order["order_id"] == order_id:
            return order

    return None