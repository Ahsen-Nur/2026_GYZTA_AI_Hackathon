from fastapi import APIRouter
from pydantic import BaseModel

from app.database import SessionLocal
from app.models import Order
from app.models import Inventory

from app.services.openrouter_service import ask_ai

router = APIRouter()


class ChatRequest(BaseModel):

    message: str


@router.post("/chat")
def chat(req: ChatRequest):

    db = SessionLocal()

    orders = db.query(Order).all()
    inventory = db.query(Inventory).all()

    # Admin asistanı için sipariş + stok verisini birlikte gönder
    # ask_ai artık orders parametresini context olarak sisteme ekliyor
    full_prompt = f"""
Yönetici sorusu: {req.message}

Stok Durumu:
"""
    for item in inventory:
        full_prompt += (
            f"- {item.product}: {item.stock} adet "
            f"({item.status}) | Depo: {item.warehouse}\n"
        )

    ai_response = ask_ai(full_prompt, orders)

    db.close()

    return {
        "response": ai_response
    }