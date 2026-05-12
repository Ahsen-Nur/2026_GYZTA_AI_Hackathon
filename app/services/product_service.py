import requests


def get_products():

    url = "https://fakestoreapi.com/products"

    response = requests.get(url)

    return response.json()