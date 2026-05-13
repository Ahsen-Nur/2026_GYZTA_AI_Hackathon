import os
import requests
from typing import List, Dict, Optional

from dotenv import load_dotenv

load_dotenv()

OPENROUTER_API_KEY = os.getenv(
    "OPENROUTER_API_KEY"
)

# Fallback zinciri — ilki başarısız olursa sıradakini dener
MODELS = [
    "google/gemini-2.0-flash-001",
    "google/gemini-2.5-flash-lite",
    "google/gemini-2.5-flash",
    "openai/gpt-4o-mini",
]


def _call_openrouter(messages: list, model: str) -> dict:
    """Tek bir modele istek atar, ham response dict döner."""
    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type":  "application/json",
        },
        json={
            "model":    model,
            "messages": messages,
        },
        timeout=30,
    )
    return response.json()


def ask_ai(
    prompt: str,
    orders=None,
    system_override: Optional[str] = None,
    history: Optional[List[Dict[str, str]]] = None,
) -> str:
    """
    AI'ya mesaj gönderir. Model başarısız olursa fallback zinciriyle dener.

    Parametreler:
    - prompt          : Kullanıcının son mesajı
    - orders          : Sipariş listesi (admin paneli context'i için)
    - system_override : Hazır sistem prompt'u (customer_chat kullanır)
    - history         : Önceki konuşma geçmişi
    """

    # ── Sistem prompt'u ───────────────────────────────────────────────
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

    # ── Mesaj listesi ─────────────────────────────────────────────────
    messages = [{"role": "system", "content": system_prompt}]
    if history:
        messages.extend(history)
    messages.append({"role": "user", "content": prompt})

    # ── Fallback zinciri ──────────────────────────────────────────────
    last_error = ""

    for model in MODELS:
        try:
            data = _call_openrouter(messages, model)

            if "error" in data:
                last_error = data["error"].get("message", "API hatası")
                print(f"[OpenRouter] {model} başarısız: {last_error}")
                continue

            if "choices" not in data or not data["choices"]:
                last_error = f"Beklenmeyen yanıt formatı: {data}"
                print(f"[OpenRouter] {model} choices yok, sonraki deneniyor")
                continue

            content = data["choices"][0]["message"].get("content", "").strip()

            if not content:
                last_error = "Boş yanıt"
                continue

            print(f"[OpenRouter] Yanıt alındı → {model}")
            return content

        except requests.exceptions.Timeout:
            last_error = "Zaman aşımı"
            print(f"[OpenRouter] {model} timeout, sonraki deneniyor")
            continue

        except requests.exceptions.ConnectionError:
            last_error = "Bağlantı hatası"
            print(f"[OpenRouter] {model} bağlantı hatası, sonraki deneniyor")
            continue

        except Exception as e:
            last_error = str(e)
            print(f"[OpenRouter] {model} beklenmeyen hata: {e}")
            continue

    print(f"[OpenRouter] Tüm modeller başarısız. Son hata: {last_error}")
    return "Şu an yapay zeka servisine ulaşılamıyor, lütfen biraz sonra tekrar deneyin."