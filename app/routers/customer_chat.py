from fastapi import APIRouter
from pydantic import BaseModel

from app.database import SessionLocal
from app.models import Order

from app.services.openrouter_service import ask_ai

router = APIRouter()

LAST_ORDER = None


class CustomerChatRequest(BaseModel):

    message: str


def normalize(text):

    return (
        text.lower()
        .strip()
        .replace("ı","i")
        .replace("ü","u")
        .replace("ö","o")
        .replace("ş","s")
        .replace("ç","c")
        .replace("ğ","g")
    )



@router.post("/customer-chat")
def customer_chat(req: CustomerChatRequest):

    global LAST_ORDER

    db = SessionLocal()

    orders = db.query(Order).all()

    message = normalize(req.message)

    matched_order = None

    highest_score = 0

    matched_order = None

    message_words = message.split()

    for order in orders:

        customer_tokens = normalize(
            order.customer
        ).split()

        product_tokens = normalize(
            order.product
        ).split()

        tracking = normalize(
            order.tracking_number
        )

        found = False

        for token in customer_tokens:

            if token in message_words:

                found = True

        for token in product_tokens:

            if token in message_words:

                found = True

        if tracking in message:

            found = True

        if found:

            matched_order = order

            break

    
    keywords = [

        "kargo",
        "siparis",
        "urun",
        "takip",
        "teslimat",
        "gecik",
        "nerede",
        "hala",
        "gelmedi"
    ]

    if (

        highest_score < 0.35
        and LAST_ORDER
        and any(
            k in message
            for k in keywords
        )

    ):

        matched_order = LAST_ORDER

    if matched_order:

        LAST_ORDER = matched_order

        ai_prompt = f"""

Bir müşteri destek temsilcisi gibi davran.

Müşteri mesajı:
{req.message}

Sipariş Bilgileri:

Müşteri:
{matched_order.customer}

Ürün:
{matched_order.product}

Durum:
{matched_order.status}

Takip Numarası:
{matched_order.tracking_number}

Kargo Firması:
{matched_order.carrier}

Tahmini Teslimat:
{matched_order.estimated_delivery}

Kurallar:

- Türkçe konuş
- Resmi ama doğal konuş
- Aynı cevabı tekrar etme
- İnsan gibi cevap ver
- Kısa ve net ol
- Gereksiz maddeleme yapma
- Kullanıcı ne soruyorsa ona göre cevap üret
- Sipariş bilgisi yoksa ASLA sipariş uydurma
- Emin değilsen kullanıcıdan ek bilgi iste
- Siparişle ilgili değilse kibarca söyle ve yardımcı olabileceğin konuları belirt
- kim olduğunu, ne sipariş ettiğini veya takip numarasını sormadan kesinlikle sipariş bilgisi verme
- Eğer kullanıcı siparişle ilgili bilgi vermeden sipariş durumu sorarsa, kibarca sipariş bilgisi istediğini söyle ve kullanıcıdan isim, ürün adı veya takip numarasından birini istemesini rica et
- Eğer kullanıcı siparişle ilgili bilgi vermeden tahmini teslimat süresi sorarsa, kibarca sipariş bilgisi istediğini söyle ve kullanıcıdan isim, ürün adı veya takip numarasından birini istemesini rica et
- Eğer kullanıcı siparişle ilgili bilgi vermeden kargo firması sorarsa, kibarca sipariş bilgisi istediğini söyle ve kullanıcıdan isim, ürün adı veya takip numarasından birini istemesini rica et
- 
"""

        response = ask_ai(ai_prompt)

    else:

        response = """

        Merhaba.

        Sipariş durumunuzu kontrol edebilmem için aşağıdaki bilgilerden birini paylaşabilirsiniz:

        • Sipariş numarası
        • Takip numarası
        • Ürün adı
        • Ad soyad

        """

    db.close()

    return {

        "response": response
    }