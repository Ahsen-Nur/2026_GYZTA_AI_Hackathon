# AI Order Assistant

Bu proje; sipariş yönetimi, stok takibi, operasyon analizi ve yapay zeka destekli müşteri iletişimini tek merkezde birleştiren modern bir operasyon panelidir.

Hackathon sürecinde geliştirilen bu sistem; gerçek operasyon senaryolarına yakın bir mimari ile tasarlanmıştır ve aktif olarak geliştirilmeye devam etmektedir.

---

# İçindekiler

- [Proje Özeti](#proje-özeti)
- [Teknolojiler](#teknolojiler)
- [Sistem Özellikleri](#sistem-özellikleri)
- [UI / UX Tasarımı](#ui--ux-tasarımı)
- [Proje Yapısı](#proje-yapısı)
- [Kurulum](#kurulum)
- [OpenRouter API Ayarı](#openrouter-api-ayarı)
- [Veritabanını Oluşturma](#veritabanını-oluşturma)
- [Projeyi Çalıştırma](#projeyi-çalıştırma)
- [API Endpointleri](#api-endpointleri)
- [AI Sistemleri](#ai-sistemleri)
- [Ekranlar](#ekranlar)
- [Gelecek Geliştirmeler](#gelecek-geliştirmeler)
- [Notlar](#notlar)

---

# Proje Özeti

AI Order Assistant;

- sipariş yönetimi,
- kargo takibi,
- stok kontrolü,
- operasyon analizi,
- AI destekli müşteri desteği

özelliklerini tek panel altında birleştirir.

Sistem iki farklı kullanıcı deneyimi sunar:

## Yönetici Paneli

- Operasyon dashboardu
- Gerçek zamanlı KPI sistemi
- AI operasyon analizi
- Stok yönetimi
- Sipariş yönetimi
- AI operasyon asistanı

## Müşteri Paneli

- Doğal dil ile sipariş sorgulama
- Takip numarası olmadan sipariş bulma
- AI destekli müşteri desteği
- Akıllı kimlik doğrulama sistemi

---

# Teknolojiler

## Backend

- Python
- FastAPI
- SQLAlchemy
- SQLite
- Pydantic

## Frontend

- HTML5
- CSS3
- Vanilla JavaScript

## AI

- OpenRouter API
- Gemini Flash
- GPT-4o Mini fallback sistemi

---

# Sistem Özellikleri

## AI Operasyon Dashboardu

- Gerçek zamanlı operasyon görünümü
- KPI kart sistemi
- Operasyon akışı
- Shipment takibi
- Kritik stok uyarıları

---

## AI Analitik Sistemi

Sistem otomatik olarak:

- geciken siparişleri,
- operasyon risklerini,
- yoğun sipariş bölgelerini,
- stok problemlerini,
- operasyon yükünü

analiz eder.

---

## AI Customer Support

Müşteri;

- isim,
- takip numarası,
- ürün adı

ile siparişini sorgulayabilir.

Sistem doğal dil analizi kullanır.

---

## Güvenlik Katmanı

Sistem:

- farklı kullanıcı siparişlerini korur,
- kimlik doğrulama uygular,
- veri sızıntısını engeller.

---

## Responsive Modern UI

- Glassmorphism tasarım
- Mobil uyum
- Modern dashboard deneyimi
- Loading animasyonları
- Canlı operasyon hissi

---

# UI / UX Tasarımı

Proje modern operasyon merkezlerinden ilham alınarak tasarlanmıştır.

Arayüz tarafında:

- glassmorphism tasarım dili,
- gradient geçişler,
- transparan paneller,
- blur efektleri,
- canlı operasyon hissi,
- responsive yapı

kullanılmıştır.

---

## Glassmorphism Tasarım

Projede modern “glassmorphism” yaklaşımı uygulanmıştır.

Bu yaklaşım:

- yarı saydam paneller,
- cam hissi veren blur efektleri,
- yumuşak ışık geçişleri,
- transparan katmanlar

oluşturur.

Kullanılan bazı temel CSS teknikleri:

```css
backdrop-filter: blur(18px);

background: rgba(10,15,35,.82);

border: 1px solid rgba(255,255,255,.06);
```

Bu yapı sayesinde dashboard daha modern, premium ve canlı bir operasyon merkezi hissi vermektedir.

---



## Kullanıcı Deneyimi

Sistemde kullanıcı deneyimini güçlendirmek için:

- loading animasyonları,
- canlı durum göstergeleri,
- AI aktif göstergesi,
- operasyon feed sistemi,
- modern toast bildirimleri

kullanılmıştır.

---

## Tasarım Yaklaşımı

Arayüz geliştirilirken:

- operasyon merkezleri,
- AI dashboard sistemleri,
- modern SaaS panelleri,
- command center yapıları

referans alınmıştır.

Amaç yalnızca veri göstermek değil; kullanıcıya aktif çalışan bir operasyon merkezi hissi vermektir.

---

# Proje Yapısı

```bash
2026_GYZTA_AI_Hackathon/
│
├── app/
│   │
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── seed.py
│   │
│   ├── routers/
│   │   ├── dashboard.py
│   │   ├── orders.py
│   │   ├── inventory.py
│   │   ├── analytics.py
│   │   ├── chat.py
│   │   └── customer_chat.py
│   │
│   ├── services/
│   │   ├── analytics_service.py
│   │   ├── insight_service.py
│   │   ├── inventory_service.py
│   │   ├── order_service.py
│   │   └── openrouter_service.py
│   │
│   ├── templates/
│   │   └── index.html
│   │
│   └── static/
│       ├── style.css
│       ├── loading.css
│       └── script.js
│
└── README.md
```

---

# Kurulum

## 1) Repository Klonla

```bash
git clone https://github.com/Ahsen-Nur/2026_GYZTA_AI_Hackathon.git
```

---

## 2) Proje Klasörüne Gir

```bash
cd 2026_GYZTA_AI_Hackathon
```

---

## 3) Virtual Environment Oluştur

### Mac / Linux

```bash
python3 -m venv venv
```

```bash
source venv/bin/activate
```

### Windows

```bash
python -m venv venv
```

```bash
venv\Scripts\activate
```

---

## 4) Gerekli Paketleri Kur

```bash
pip install fastapi uvicorn sqlalchemy jinja2 python-dotenv requests
```

---

# OpenRouter API Ayarı

AI sistemlerinin çalışabilmesi için OpenRouter API gereklidir.

## 1) `.env` Dosyası Oluştur

Proje ana dizininde:

```env
OPENROUTER_API_KEY=YOUR_API_KEY
```

---

## 2) OpenRouter API Key Al

https://openrouter.ai

---

# Veritabanını Oluşturma

Proje demo verileriyle birlikte çalışır.

`seed.py` dosyası:

- sipariş verileri,
- stok verileri,
- örnek müşteri kayıtları

oluşturur.

---

## Seed Scriptini Çalıştır

```bash
python app/seed.py
```

Başarılı olursa:

```text
AI operasyon veritabanı başarıyla oluşturuldu.
```

mesajı görünür.

---

# Projeyi Çalıştırma

```bash
uvicorn app.main:app --reload
```

---

## Tarayıcıda Aç

```text
http://127.0.0.1:8000
```

---

# API Endpointleri

## Dashboard

```http
GET /dashboard
```

---

## Siparişler

```http
GET /orders
```

---

## Inventory

```http
GET /inventory
```

---

## Analytics

```http
GET /analytics
```

---

## Admin AI Chat

```http
POST /chat
```

---

## Customer AI Chat

```http
POST /customer-chat
```

---

# AI Sistemleri

## OpenRouter Fallback Sistemi

Bir AI modeli başarısız olursa sistem otomatik olarak diğer modele geçer.

Fallback sırası:

- Gemini 2.0 Flash
- Gemini 2.5 Flash Lite
- Gemini 2.5 Flash
- GPT-4o Mini

Bu yapı:

- demo stabilitesini artırır,
- servis kesintisini azaltır,
- hackathon ortamında güvenilirlik sağlar.

---

## AI Insight Engine

Sistem otomatik olarak:

- geciken siparişleri,
- kritik stokları,
- operasyon yoğunluğunu,
- shipment akışını

analiz eder.

---

## Akıllı Sipariş Eşleştirme

Sistem:

- ürün adı,
- takip numarası,
- token eşleşmesi

ile sipariş bulabilir.

---

# Ekranlar

## Yönetici Paneli

- Dashboard
- KPI kartları
- Sipariş yönetimi
- Stok yönetimi
- Operasyon analizi
- AI operasyon asistanı

---

## Müşteri Paneli

- AI destekli destek sistemi
- Sipariş sorgulama
- Doğal dil desteği
- Akıllı doğrulama sistemi

---

# Gelecek Geliştirmeler

Proje aktif olarak geliştirilmeye devam etmektedir.

Planlanan geliştirmeler:

- JWT Authentication
- Gerçek kullanıcı sistemi
- Redis cache
- WebSocket canlı veri akışı
- Gerçek kargo API entegrasyonu
- Docker deployment
- Kubernetes desteği
- AI demand forecasting
- Fine-tuned support model
- Çoklu dil desteği
- Gerçek zamanlı notification sistemi

---

# Notlar

Bu proje hackathon odaklı geliştirildiği için bazı veriler simüle edilmiştir.

Buna rağmen sistem mimarisi:

- service-based structure,
- AI orchestration,
- API architecture,
- fallback management,
- operational analytics,
- customer workflow management

gibi gerçek production sistemlerine yakın şekilde tasarlanmıştır.

---

