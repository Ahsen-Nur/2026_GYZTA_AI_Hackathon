from fastapi import APIRouter
from pydantic import BaseModel

from app.services.order_service import (
    extract_order_id,
    find_order
)

from app.services.gemini_service import ask_ai

router = APIRouter()


class ChatRequest(BaseModel):
    message: str


@router.post("/chat")
def chat(request: ChatRequest):

    message = request.message

    order_id = extract_order_id(message)

    if order_id:

        order = find_order(order_id)

        if order:

            prompt = f"""
Customer asks about order status.

Customer:
{order['customer']}

City:
{order['city']}

Order:
{order['product']}

Status:
{order['status']}

Cargo Company:
{order['cargo_company']}

Tracking Number:
{order['tracking_number']}

Estimated Delivery:
{order['estimated_delivery']}

Give a professional Turkish response.
"""

            ai_response = ask_ai(prompt)

            return {
                "response": ai_response
            }

    ai_response = ask_ai(message)

    return {
        "response": ai_response
    }