/* =========================
   XSS KORUMASI
========================= */

function escapeHtml(text) {
    const map = {
        "&": "&amp;",
        "<": "&lt;",
        ">": "&gt;",
        '"': "&quot;",
        "'": "&#x27;"
    };
    return String(text).replace(/[&<>"']/g, m => map[m]);
}

/* =========================
   PANEL GEÇİŞLERİ
========================= */

function enterAdminPanel() {

    document
        .getElementById("role-screen")
        .classList.add("hidden-section");

    document
        .getElementById("admin-panel")
        .classList.remove("hidden-section");

    init();
}

function enterCustomerPanel() {

    document
        .getElementById("role-screen")
        .classList.add("hidden-section");

    document
        .getElementById("customer-panel")
        .classList.remove("hidden-section");
}

/* =========================
   MENÜ
========================= */

function showSection(section, event) {

    const sections = [
        "dashboard-section",
        "orders-section",
        "inventory-section",
        "analytics-section"
    ];

    sections.forEach(id => {
        const el = document.getElementById(id);
        if (el) {
            el.classList.add("hidden-section");
        }
    });

    document
        .getElementById(section + "-section")
        .classList.remove("hidden-section");

    document
        .querySelectorAll(".nav-item")
        .forEach(item => {
            item.classList.remove("active");
        });

    event.target.classList.add("active");
}

/* =========================
   DURUM ÇEVİRİ
========================= */

function translateStatus(status) {

    if (status === "Shipped")   return "Gönderildi";
    if (status === "Preparing") return "Hazırlanıyor";
    if (status === "Delayed")   return "Gecikmiş";

    return status;
}

/* =========================
   DASHBOARD
========================= */

async function loadDashboard() {

    const res  = await fetch("/dashboard");
    const data = await res.json();

    document.getElementById("total-orders").innerText   = data.total_orders;
    document.getElementById("delayed-orders").innerText = data.delayed_orders;
    document.getElementById("critical-stock").innerText = data.critical_stock;
    document.getElementById("revenue").innerText        = "₺" + data.revenue;

    loadInsights(data.insights);
}

/* =========================
   İÇGÖRÜ
========================= */

function loadInsights(insights) {

    const container = document.getElementById("insights-container");
    container.innerHTML = "";

    insights.forEach(insight => {
        const div = document.createElement("div");
        div.className = "insight-card";
        div.textContent = insight;          // textContent → XSS yok
        container.appendChild(div);
    });
}

/* =========================
   OPERASYON AKIŞI
========================= */

function addFeedItem(title, text, color = "blue") {

    const feed = document.getElementById("operations-feed");
    if (!feed) return;

    const item = document.createElement("div");
    item.className = "feed-item";
    item.innerHTML = `
        <div class="feed-indicator ${escapeHtml(color)}"></div>
        <div>
            <h4>${escapeHtml(title)}</h4>
            <p>${escapeHtml(text)}</p>
        </div>
    `;

    feed.insertBefore(item, feed.firstChild);

    const items = feed.querySelectorAll(".feed-item");
    if (items.length > 6) {
        items[items.length - 1].remove();
    }
}

/* =========================
   SİPARİŞLER
========================= */

async function loadOrders() {

    const res  = await fetch("/orders");
    const data = await res.json();

    const table    = document.getElementById("orders-table");
    const allTable = document.getElementById("all-orders-table");

    if (table)    table.innerHTML    = "";
    if (allTable) allTable.innerHTML = "";

    data.forEach(order => {

        const status = translateStatus(order.status);

        if (table) {
            const tr = document.createElement("tr");
            tr.innerHTML = `
                <td>#${escapeHtml(String(order.id))}</td>
                <td>${escapeHtml(order.customer)}</td>
                <td>${escapeHtml(status)}</td>
                <td>${escapeHtml(order.city)}</td>
            `;
            table.appendChild(tr);
        }

        if (allTable) {
            const tr = document.createElement("tr");
            tr.innerHTML = `
                <td>#${escapeHtml(String(order.id))}</td>
                <td>${escapeHtml(order.customer)}</td>
                <td>${escapeHtml(order.product)}</td>
                <td>${escapeHtml(status)}</td>
                <td>${escapeHtml(order.city)}</td>
            `;
            allTable.appendChild(tr);
        }
    });
}

/* =========================
   STOK
========================= */

async function loadInventory() {

    const res  = await fetch("/inventory");
    const data = await res.json();

    const cards = document.getElementById("inventory-cards");
    if (!cards) return;

    cards.innerHTML = "";

    data.forEach(item => {
        const div = document.createElement("div");
        div.className = "card";
        div.innerHTML = `
            <span class="card-label">${escapeHtml(item.product)}</span>
            <h2>${escapeHtml(String(item.stock))}</h2>
            <p>${escapeHtml(item.status)}</p>
        `;
        cards.appendChild(div);
    });
}

/* =========================
   ANALİTİK
========================= */

async function loadAnalytics() {

    const res  = await fetch("/analytics");
    const data = await res.json();

    const top  = document.getElementById("top-product");
    const risk = document.getElementById("risk-orders");

    if (top)  top.innerText  = data.top_product;
    if (risk) risk.innerText = data.risk_analysis;
}

/* =========================
   YÖNETİCİ CHAT — mesaj gönder
========================= */

async function sendMessage() {

    const input   = document.getElementById("message-input");
    const message = input.value.trim();

    if (!message) return;

    const box = document.getElementById("chat-box");

    // Kullanıcı mesajı — XSS korumalı
    const userDiv = document.createElement("div");
    userDiv.className   = "user-message";
    userDiv.textContent = message;
    box.appendChild(userDiv);

    input.value = "";
    box.scrollTop = box.scrollHeight;

    // Loading göstergesi
    const loadingDiv = document.createElement("div");
    loadingDiv.className = "bot-message loading-container";
    loadingDiv.innerHTML = `
        <div class="loading-dot"></div>
        <div class="loading-dot"></div>
        <div class="loading-dot"></div>
    `;
    box.appendChild(loadingDiv);
    box.scrollTop = box.scrollHeight;

    try {
        const res  = await fetch("/chat", {
            method:  "POST",
            headers: { "Content-Type": "application/json" },
            body:    JSON.stringify({ message })
        });
        const data = await res.json();

        loadingDiv.remove();

        const botDiv = document.createElement("div");
        botDiv.className   = "bot-message";
        botDiv.textContent = data.response;
        box.appendChild(botDiv);

    } catch (err) {
        loadingDiv.remove();

        const errDiv = document.createElement("div");
        errDiv.className   = "bot-message";
        errDiv.textContent = "Bağlantı hatası. Lütfen tekrar deneyin.";
        box.appendChild(errDiv);
    }

    box.scrollTop = box.scrollHeight;
}

/* =========================
   MÜŞTERİ CHAT — mesaj gönder
========================= */

async function sendCustomerMessage() {

    const input   = document.getElementById("customer-message");
    const message = input.value.trim();

    if (!message) return;

    const box = document.getElementById("customer-chat");

    // Kullanıcı mesajı — XSS korumalı
    const userDiv = document.createElement("div");
    userDiv.className   = "user-message";
    userDiv.textContent = message;
    box.appendChild(userDiv);

    input.value = "";
    box.scrollTop = box.scrollHeight;

    // Loading göstergesi
    const loadingDiv = document.createElement("div");
    loadingDiv.className = "bot-message loading-container";
    loadingDiv.innerHTML = `
        <div class="loading-dot"></div>
        <div class="loading-dot"></div>
        <div class="loading-dot"></div>
    `;
    box.appendChild(loadingDiv);
    box.scrollTop = box.scrollHeight;

    try {
        const res  = await fetch("/customer-chat", {
            method:  "POST",
            headers: { "Content-Type": "application/json" },
            body:    JSON.stringify({ message })
        });
        const data = await res.json();

        loadingDiv.remove();

        const botDiv = document.createElement("div");
        botDiv.className   = "bot-message";
        botDiv.textContent = data.response;
        box.appendChild(botDiv);

    } catch (err) {
        loadingDiv.remove();

        const errDiv = document.createElement("div");
        errDiv.className   = "bot-message";
        errDiv.textContent = "Bağlantı hatası. Lütfen tekrar deneyin.";
        box.appendChild(errDiv);
    }

    box.scrollTop = box.scrollHeight;
}

/* =========================
   ENTER TUŞU DESTEĞİ
========================= */

document.addEventListener("DOMContentLoaded", () => {

    // Admin chat — Enter ile gönder
    const adminInput = document.getElementById("message-input");
    if (adminInput) {
        adminInput.addEventListener("keydown", e => {
            if (e.key === "Enter" && !e.shiftKey) {
                e.preventDefault();
                sendMessage();
            }
        });
    }

    // Müşteri chat — Enter ile gönder
    const customerInput = document.getElementById("customer-message");
    if (customerInput) {
        customerInput.addEventListener("keydown", e => {
            if (e.key === "Enter" && !e.shiftKey) {
                e.preventDefault();
                sendCustomerMessage();
            }
        });
    }
});

/* =========================
   OPERASYON OLAYLARI
========================= */

function startFeedLoop() {

    const events = [
        {
            title: "Yeni Sipariş",
            text:  "İstanbul bölgesinden yeni sipariş oluşturuldu.",
            color: "blue"
        },
        {
            title: "Kritik Stok",
            text:  "Apple Magic Keyboard stok seviyesi kritik.",
            color: "yellow"
        },
        {
            title: "Teslimat Tamamlandı",
            text:  "1 sipariş başarıyla teslim edildi.",
            color: "green"
        },
        {
            title: "Gecikme Tespiti",
            text:  "Bursa gönderisinde gecikme riski algılandı.",
            color: "red"
        }
    ];

    setInterval(() => {
        const random = events[Math.floor(Math.random() * events.length)];
        addFeedItem(random.title, random.text, random.color);
    }, 7000);
}

/* =========================
   INIT
========================= */

async function init() {

    await loadDashboard();
    await loadOrders();
    await loadInventory();
    await loadAnalytics();

    startFeedLoop();
}