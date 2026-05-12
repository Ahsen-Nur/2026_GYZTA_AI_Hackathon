from fastapi import APIRouter

from app.services.product_service import get_products

router = APIRouter()


@router.get("/products")
def products():

    return get_products()