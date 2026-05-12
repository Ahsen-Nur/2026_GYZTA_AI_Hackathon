import os
import requests

from dotenv import load_dotenv

load_dotenv()

OPENROUTER_API_KEY = os.getenv(
    "OPENROUTER_API_KEY"
)

URL = "https://openrouter.ai/api/v1/chat/completions"

HEADERS = {

    "Authorization":
        f"Bearer {OPENROUTER_API_KEY}",

    "Content-Type":
        "application/json"
}


def ask_ai(message, orders):

    context = "\n".join([

        f"""
Müşteri: {o.customer}
Ürün: {o.product}
Durum: {o.status}
Takip Numarası: {o.tracking_number}
Şehir: {o.city}
"""
        for o in orders
    ])

    prompt = f"""

Sen Türkçe konuşan profesyonel bir AI operasyon asistanısın.

ASLA İngilizce konuşma.

Görevlerin:
- sipariş takibi
- müşteri destek
- stok yönetimi
- kargo operasyonu
- shipment automation

Gerçek sipariş verileri:

{context}

Kullanıcı mesajı:
{message}

Kısa, profesyonel ve doğal cevap ver.
"""

    body = {

        "model":
            "openai/gpt-4o-mini",

        "messages": [

            {
                "role": "system",
                "content":
                    "Her zaman Türkçe cevap ver."
            },

            {
                "role": "user",
                "content": prompt
            }
        ]
    }

    response = requests.post(
        URL,
        headers=HEADERS,
        json=body
    )

    data = response.json()

    return data["choices"][0]["message"]["content"]