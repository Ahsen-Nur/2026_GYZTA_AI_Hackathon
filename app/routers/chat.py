from fastapi import APIRouter
from pydantic import BaseModel

from app.database import SessionLocal
from app.models import Order

from app.services.openrouter_service import ask_ai

router = APIRouter()


class ChatRequest(BaseModel):

    message: str


@router.post("/chat")
def chat(req: ChatRequest):

    db = SessionLocal()

    orders = db.query(Order).all()

    response = ask_ai(
        req.message,
        orders
    )

    db.close()

    return {

        "response":
            response
    }