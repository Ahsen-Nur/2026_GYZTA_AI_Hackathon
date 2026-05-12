from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Dict, Optional

from app.database import SessionLocal
from app.models import Order

from app.services.openrouter_service import ask_ai

router = APIRouter()

# Konuşma geçmişi
conversation_history: List[Dict[str, str]] = []

# Aktif doğrulanmış sipariş
LAST_ORDER: Optional[object] = None

# Kimlik doğrulama durumu
# None       → henüz kimlik belirlenmedi
# "verified" → kullanıcı kendi siparişiyle doğrulandı
# "pending"  → farklı isim geldi, doğrulama bekleniyor
identity_state: str = None

# Doğrulama bekleyen sipariş (kullanıcı onaylayana kadar gösterilmez)
PENDING_ORDER: Optional[object] = None


class CustomerChatRequest(BaseModel):
    message: str


def normalize(text: str) -> str:
    return (
        text.lower()
        .strip()
        .replace("ı", "i")
        .replace("ü", "u")
        .replace("ö", "o")
        .replace("ş", "s")
        .replace("ç", "c")
        .replace("ğ", "g")
        .replace("â", "a")
        .replace("î", "i")
        .replace("û", "u")
    )


def score_order_match(message_norm: str, order) -> float:
    msg_words = message_norm.split()

    tracking = normalize(order.tracking_number)
    if tracking and tracking in message_norm:
        return 1.0

    full_name = normalize(order.customer)
    if full_name and full_name in message_norm:
        return 0.9

    name_tokens = [t for t in full_name.split() if len(t) >= 3]
    if len(name_tokens) >= 2:
        matched = [t for t in name_tokens if t in msg_words]
        ratio = len(matched) / len(name_tokens)
        if ratio == 1.0:
            return 0.88
        if len(matched) >= 2 and ratio >= 0.66:
            return 0.75

    product = normalize(order.product)
    if product and product in message_norm:
        return 0.8

    if name_tokens:
        first = name_tokens[0]
        if len(first) >= 4 and first in msg_words:
            return 0.4

    if len(name_tokens) >= 2:
        last = name_tokens[-1]
        if len(last) >= 4 and last in msg_words:
            return 0.35

    product_tokens = [t for t in product.split() if len(t) >= 4]
    hits = [t for t in product_tokens if t in msg_words]
    if len(hits) >= 2:
        return 0.3

    return 0.0


MATCH_THRESHOLD = 0.35

CONTEXT_KEYWORDS = [
    "kargo", "siparis", "urun", "takip",
    "teslimat", "gecik", "nerede", "hala",
    "gelmedi", "ne zaman", "durum", "kac gun",
    "aras", "yurtici", "mng", "hepsijet", "surat",
    "iade", "iptal", "paket", "gonderi", "neden",
    "nasil", "ne oldu", "sorun", "problem",
    "bilmiyorum", "unuttum", "hatirlamiyorum"
]

CONFIRM_KEYWORDS = [
    "evet", "dogru", "o benim", "benim",
    "evet ben", "aynen", "tamam", "kesinlikle",
    "o siparis benim", "benim siparisim"
]

DENY_KEYWORDS = [
    "hayir", "yanlis", "bu ben degilim",
    "o degil", "benim degil", "farkli",
    "hata yaptim", "yanlislikla"
]


def build_system_prompt(orders, matched_order=None, pending_order=None, identity_state=None) -> str:

    all_orders_text = ""
    for o in orders:
        status_tr = {
            "Shipped":   "Kargoya verildi",
            "Preparing": "Hazırlanıyor",
            "Delayed":   "Gecikmiş"
        }.get(o.status, o.status)

        all_orders_text += (
            f"  • ID:{o.id} | Ad:{o.customer} | Ürün:{o.product} | "
            f"Durum:{status_tr} | Takip:{o.tracking_number} | "
            f"Kargo:{o.carrier} | Teslim:{o.estimated_delivery}\n"
        )

    matched_section = ""
    if matched_order:
        status_tr = {
            "Shipped":   "Kargoya verildi",
            "Preparing": "Hazırlanıyor",
            "Delayed":   "Gecikmiş"
        }.get(matched_order.status, matched_order.status)

        matched_section = f"""
## AKTİF DOĞRULANMIŞ SİPARİŞ:
- Müşteri : {matched_order.customer}
- Ürün    : {matched_order.product}
- Durum   : {status_tr}
- Takip No: {matched_order.tracking_number}
- Kargo   : {matched_order.carrier}
- Teslim  : {matched_order.estimated_delivery}

Müşteriye SADECE "{matched_order.customer}" adıyla hitap et.
"""

    pending_section = ""
    if pending_order:
        status_tr = {
            "Shipped":   "Kargoya verildi",
            "Preparing": "Hazırlanıyor",
            "Delayed":   "Gecikmiş"
        }.get(pending_order.status, pending_order.status)

        pending_section = f"""
## DOĞRULAMA BEKLEYEN SİPARİŞ:
- Müşteri : {pending_order.customer}
- Ürün    : {pending_order.product}
- Durum   : {status_tr}
- Takip No: {pending_order.tracking_number}
- Kargo   : {pending_order.carrier}
- Teslim  : {pending_order.estimated_delivery}

ÖNEMLİ: Bu siparişin bilgilerini HENÜZ gösterme.
Önce müşteriye kibarca sor: "{pending_order.customer} adına kayıtlı bir sipariş bulduk.
Bu sipariş size mi ait, yoksa o kişinin siparişini mi soruyorsunuz?"
Müşteri "evet benim" derse siparişi göster.
Müşteri "hayır" veya "o kişinin siparişini soruyorum" derse,
o kişinin siparişini başkasına veremeyeceğini kibarca açıkla.
"""

    identity_section = ""
    if identity_state == "pending":
        identity_section = """
## KİMLİK DURUMU: DOĞRULAMA BEKLENİYOR
Kullanıcı önce farklı bir isim verdi, sonra başka birinin adını sordu.
Yukarıdaki "DOĞRULAMA BEKLEYEN SİPARİŞ" bölümündeki talimatları uygula.
"""
    elif identity_state == "verified":
        identity_section = """
## KİMLİK DURUMU: DOĞRULANDI
Kullanıcı kimliği doğrulandı, siparişini özgürce gösterebilirsin.
"""

    return f"""
Sen "AI Destek" adlı bir e-ticaret müşteri destek asistanısın.
Gerçek bir insan temsilci gibi, doğal ve akıcı Türkçe konuşursun.

{matched_section}
{pending_section}
{identity_section}

## TÜM SİPARİŞ VERİTABANI (sadece referans için):
{all_orders_text}

## KİŞİLİĞİN VE KONUŞMA TARZI:
- Sıcak, sabırlı ve anlayışlı bir insansın
- Asla robotik veya kalıp cümleler kullanmazsın
- Müşteri ne derse anlık tepki üretirsin
- Konuşmanın akışını ve bağlamını takip edersin
- Emojileri doğal yerlerde kullanabilirsin 😊

## AKILLI SENARYO YÖNETİMİ:

### Sipariş numarası / takip no bilmiyorsa:
→ "Sorun değil! Adınızı söylemeniz yeterli, onunla bulabilirim.
   Ya da sipariş ettiğiniz ürünün adını da söyleyebilirsiniz."

### Kullanıcı "bilmiyorum / unuttum" derse:
→ "Hiç sorun değil 😊 Hangi ürünü sipariş ettiğinizi hatırlıyor musunuz?"

### Gecikme nedeni sorulursa:
→ "Gecikmenin tam nedenini sistemimizde göremiyorum,
   kargo firmasını arayarak detaylı bilgi alabilirsiniz."

### Genel sorular (iade, değişim vb.):
→ İade: "Teslimattan itibaren 14 gün içinde iade talebinde bulunabilirsiniz."
→ Değişim: "Ürün hasarlı veya yanlış geldiyse ücretsiz değişim yapıyoruz."

### Sipariş durumu:
- "Kargoya verildi" → Takip numarasını ver, kargo firmasını belirt
- "Hazırlanıyor"    → "Siparişiniz depomuzda hazırlanıyor, yakında kargoya verilecek"
- "Gecikmiş"       → Özür dile, kargo firmasına yönlendir

## GÜVENLİK KURALLARI (EN ÖNEMLİ):
- Bir kişinin sipariş bilgilerini BAŞKASINA verme
- "X kişisinin siparişine bakın" gibi isteklerde önce sahiplik doğrulaması yap
- Kullanıcı o siparişin sahibi olduğunu onaylayana kadar sipariş detaylarını GÖSTERME
- Gizlilik konusunda şeffaf ve nazik ol: "Kişisel sipariş bilgilerini korumak için doğrulama yapıyoruz"

## MUTLAK KURALLAR:
- Veritabanında olmayan siparişi ASLA uydurma
- Bilmediğin bilgiyi ASLA tahmin etme
- Müşteri sıkıştığında her zaman yeni bir alternatif sun
- Gereksiz uzun paragraf yazma
"""


def is_confirmation(message_norm: str) -> bool:
    return any(k in message_norm for k in CONFIRM_KEYWORDS)


def is_denial(message_norm: str) -> bool:
    return any(k in message_norm for k in DENY_KEYWORDS)


@router.post("/customer-chat")
def customer_chat(req: CustomerChatRequest):

    global LAST_ORDER, PENDING_ORDER, conversation_history, identity_state

    db = SessionLocal()
    orders = db.query(Order).all()

    original_message = req.message.strip()
    message_norm = normalize(original_message)

    # ── Eşleştirme ───────────────────────────────────────────────────
    best_order = None
    best_score = 0.0

    for order in orders:
        score = score_order_match(message_norm, order)
        if score > best_score:
            best_score = score
            best_order = order

    # ── Durum makinesi ───────────────────────────────────────────────

    if identity_state == "pending" and PENDING_ORDER:
        # Kullanıcı doğrulama cevabı veriyor
        if is_confirmation(message_norm):
            # "Evet bu benim" → onayla
            LAST_ORDER = PENDING_ORDER
            PENDING_ORDER = None
            identity_state = "verified"

        elif is_denial(message_norm):
            # "Hayır o benim değil" → başkasının siparişini verme
            PENDING_ORDER = None
            identity_state = None
            LAST_ORDER = None

        # else → cevap belirsiz, AI yeniden soracak (pending kalır)

    elif best_score >= MATCH_THRESHOLD:
        new_order = best_order

        if LAST_ORDER is None:
            # İlk kez bir sipariş bulundu → direkt kabul
            LAST_ORDER = new_order
            identity_state = "verified"

        elif normalize(new_order.customer) != normalize(LAST_ORDER.customer):
            # Daha önce başka biri doğrulandı, şimdi farklı isim geldi
            # → Doğrulama iste
            PENDING_ORDER = new_order
            identity_state = "pending"

        else:
            # Aynı müşteri, devam et
            LAST_ORDER = new_order
            identity_state = "verified"

    elif (
        LAST_ORDER is not None
        and any(k in message_norm for k in CONTEXT_KEYWORDS)
        and identity_state == "verified"
    ):
        # Bağlamdan devam — mevcut doğrulanmış sipariş
        pass

    elif best_score == 0.0 and identity_state not in ("pending", "verified"):
        # Hiç eşleşme yok, yeni konuşma
        LAST_ORDER = None
        PENDING_ORDER = None
        identity_state = None

    # ── Sistem prompt'unu oluştur ─────────────────────────────────────
    system_prompt = build_system_prompt(
        orders=orders,
        matched_order=LAST_ORDER if identity_state == "verified" else None,
        pending_order=PENDING_ORDER if identity_state == "pending" else None,
        identity_state=identity_state
    )

    # ── Konuşma geçmişi ───────────────────────────────────────────────
    conversation_history.append({
        "role":    "user",
        "content": original_message
    })

    if len(conversation_history) > 20:
        conversation_history = conversation_history[-20:]

    # ── AI ────────────────────────────────────────────────────────────
    response = ask_ai(
        prompt=original_message,
        orders=None,
        system_override=system_prompt,
        history=conversation_history[:-1]
    )

    conversation_history.append({
        "role":    "assistant",
        "content": response
    })

    db.close()

    return {"response": response}