import os
import requests

from dotenv import load_dotenv

load_dotenv()

OPENROUTER_API_KEY = os.getenv(
    "OPENROUTER_API_KEY"
)

MODEL = "google/gemini-2.0-flash-001"


def ask_ai(prompt):

    try:

        response = requests.post(

            "https://openrouter.ai/api/v1/chat/completions",

            headers={

                "Authorization":
                    f"Bearer {OPENROUTER_API_KEY}",

                "Content-Type":
                    "application/json"
            },

            json={

                "model": MODEL,

                "messages": [

                    {
                        "role": "system",

                        "content": """

Sen profesyonel bir yapay zeka operasyon asistanısın.

Kurallar:

- Her zaman Türkçe konuş
- Doğal konuş
- İnsan gibi cevap ver
- Aynı cevabı tekrar etme
- Kısa ama açıklayıcı ol
- Gereksiz teknik detay verme
"""
                    },

                    {
                        "role": "user",

                        "content": prompt
                    }
                ]
            }

        )

        data = response.json()

        return data["choices"][0]["message"]["content"]

    except Exception as e:

        return f"AI sistem hatası oluştu: {str(e)}"