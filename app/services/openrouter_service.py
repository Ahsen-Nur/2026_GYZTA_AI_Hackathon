import os
import requests
from typing import List, Dict, Optional

from dotenv import load_dotenv

load_dotenv()

OPENROUTER_API_KEY = os.getenv(
    "OPENROUTER_API_KEY"
)

MODEL = "google/gemini-2.0-flash-001"


def ask_ai(
    prompt: str,
    orders=None,
    system_override: Optional[str] = None,
    history: Optional[List[Dict[str, str]]] = None
) -> str:
    """
    AI'ya mesaj gönderir.

    Parametreler:
    - prompt          : Kullanıcının son mesajı
    - orders          : Sipariş listesi (admin paneli context'i için)
    - system_override : Hazır sistem prompt'u (customer_chat kullanır)
    - history         : Önceki konuşma geçmişi [{"role": "user/assistant", "content": "..."}]
    """

    # ── Sistem prompt'unu belirle ─────────────────────────────────────
    if system_override:
        system_prompt = system_override
    else:
        system_prompt = """
Sen profesyonel bir yapay zeka operasyon asistanısın.

Kurallar:
- Her zaman Türkçe konuş
- Doğal ve samimi konuş
- İnsan gibi cevap ver
- Kısa ama açıklayıcı ol
- Gereksiz teknik detay verme
- Sipariş verisi varsa onları kullanarak somut cevaplar ver
"""
        if orders:
            system_prompt += "\n\nMevcut Sipariş Veritabanı:\n"
            for o in orders:
                system_prompt += (
                    f"- ID: {o.id} | Müşteri: {o.customer} | "
                    f"Ürün: {o.product} | Durum: {o.status} | "
                    f"Şehir: {o.city} | Takip No: {o.tracking_number} | "
                    f"Kargo: {o.carrier} | Tahmini Teslimat: {o.estimated_delivery} | "
                    f"Gelir: ₺{o.revenue}\n"
                )

    # ── Mesaj listesini oluştur ───────────────────────────────────────
    messages = [{"role": "system", "content": system_prompt}]

    # Konuşma geçmişini ekle
    if history:
        messages.extend(history)

    # Son kullanıcı mesajını ekle
    messages.append({"role": "user", "content": prompt})

    # ── API isteği ────────────────────────────────────────────────────
    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type":  "application/json"
            },
            json={
                "model":    MODEL,
                "messages": messages
            },
            timeout=30
        )

        data = response.json()
        return data["choices"][0]["message"]["content"]

    except Exception as e:
        return (
            "Şu an teknik bir sorun yaşıyoruz, "
            f"lütfen biraz sonra tekrar deneyin. ({str(e)})"
        )