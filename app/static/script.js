/* =========================
   PANEL GEÇİŞLERİ
========================= */

function enterAdminPanel(){

    document
        .getElementById("role-screen")
        .classList.add("hidden-section");

    document
        .getElementById("admin-panel")
        .classList.remove("hidden-section");

    init();
}

function enterCustomerPanel(){

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

function showSection(section,event){

    const sections = [

        "dashboard-section",
        "orders-section",
        "inventory-section",
        "analytics-section"
    ];

    sections.forEach(id => {

        const el =
            document.getElementById(id);

        if(el){

            el.classList.add(
                "hidden-section"
            );
        }
    });

    document
        .getElementById(
            section + "-section"
        )
        .classList.remove(
            "hidden-section"
        );

    document
        .querySelectorAll(".nav-item")
        .forEach(item => {

            item.classList.remove(
                "active"
            );
        });

    event.target.classList.add(
        "active"
    );
}

/* =========================
   DURUM ÇEVİRİ
========================= */

function translateStatus(status){

    if(status === "Shipped")
        return "Gönderildi";

    if(status === "Preparing")
        return "Hazırlanıyor";

    if(status === "Delayed")
        return "Gecikmiş";

    return status;
}

/* =========================
   DASHBOARD
========================= */

async function loadDashboard(){

    const res =
        await fetch("/dashboard");

    const data =
        await res.json();

    document.getElementById(
        "total-orders"
    ).innerText =
        data.total_orders;

    document.getElementById(
        "delayed-orders"
    ).innerText =
        data.delayed_orders;

    document.getElementById(
        "critical-stock"
    ).innerText =
        data.critical_stock;

    document.getElementById(
        "revenue"
    ).innerText =
        "₺" + data.revenue;

    loadInsights(data.insights);
}

/* =========================
   İÇGÖRÜ
========================= */

function loadInsights(insights){

    const container =
        document.getElementById(
            "insights-container"
        );

    container.innerHTML = "";

    insights.forEach(insight => {

        container.innerHTML += `

            <div class="insight-card">

                ${insight}

            </div>
        `;
    });
}

/* =========================
   OPERASYON AKIŞI
========================= */

function addFeedItem(
    title,
    text,
    color = "blue"
){

    const feed =
        document.getElementById(
            "operations-feed"
        );

    if(!feed) return;

    const item = `

        <div class="feed-item">

            <div class="feed-indicator ${color}">
            </div>

            <div>

                <h4>${title}</h4>

                <p>${text}</p>

            </div>

        </div>
    `;

    feed.innerHTML =
        item + feed.innerHTML;

    const items =
        feed.querySelectorAll(
            ".feed-item"
        );

    if(items.length > 6){

        items[
            items.length - 1
        ].remove();
    }
}

/* =========================
   SİPARİŞLER
========================= */

async function loadOrders(){

    const res =
        await fetch("/orders");

    const data =
        await res.json();

    const table =
        document.getElementById(
            "orders-table"
        );

    const allTable =
        document.getElementById(
            "all-orders-table"
        );

    if(table){

        table.innerHTML = "";
    }

    if(allTable){

        allTable.innerHTML = "";
    }

    data.forEach(order => {

        const status =
            translateStatus(
                order.status
            );

        const row = `

            <tr>

                <td>#${order.id}</td>

                <td>${order.customer}</td>

                <td>${status}</td>

                <td>${order.city}</td>

            </tr>
        `;

        if(table){

            table.innerHTML += row;
        }

        if(allTable){

            allTable.innerHTML += `

                <tr>

                    <td>#${order.id}</td>

                    <td>${order.customer}</td>

                    <td>${order.product}</td>

                    <td>${status}</td>

                    <td>${order.city}</td>

                </tr>
            `;
        }
    });
}

/* =========================
   STOK
========================= */

async function loadInventory(){

    const res =
        await fetch("/inventory");

    const data =
        await res.json();

    const cards =
        document.getElementById(
            "inventory-cards"
        );

    if(!cards) return;

    cards.innerHTML = "";

    data.forEach(item => {

        cards.innerHTML += `

            <div class="card">

                <span class="card-label">

                    ${item.product}

                </span>

                <h2>

                    ${item.stock}

                </h2>

                <p>

                    ${item.status}

                </p>

            </div>
        `;
    });
}

/* =========================
   ANALİTİK
========================= */

async function loadAnalytics(){

    const res =
        await fetch("/analytics");

    const data =
        await res.json();

    const top =
        document.getElementById(
            "top-product"
        );

    const risk =
        document.getElementById(
            "risk-orders"
        );

    if(top){

        top.innerText =
            data.top_product;
    }

    if(risk){

        risk.innerText =
            data.risk_analysis;
    }
}

/* =========================
   YÖNETİCİ CHAT
========================= */

async function sendMessage(){

    const input =
        document.getElementById(
            "message-input"
        );

    const message =
        input.value.trim();

    if(!message) return;

    const box =
        document.getElementById(
            "chat-box"
        );

    box.innerHTML += `

        <div class="user-message">

            ${message}

        </div>
    `;

    input.value = "";

    const res =
        await fetch("/chat", {

            method:"POST",

            headers:{
                "Content-Type":"application/json"
            },

            body:JSON.stringify({
                message:message
            })
        });

    const data =
        await res.json();

    box.innerHTML += `

        <div class="bot-message">

            ${data.response}

        </div>
    `;

    box.scrollTop =
        box.scrollHeight;
}

/* =========================
   MÜŞTERİ CHAT
========================= */

async function sendCustomerMessage(){

    const input =
        document.getElementById(
            "customer-message"
        );

    const message =
        input.value.trim();

    if(!message) return;

    const box =
        document.getElementById(
            "customer-chat"
        );

    box.innerHTML += `

        <div class="user-message">

            ${message}

        </div>
    `;

    input.value = "";

    const res =
        await fetch("/customer-chat", {

            method:"POST",

            headers:{
                "Content-Type":"application/json"
            },

            body:JSON.stringify({
                message:message
            })
        });

    const data =
        await res.json();

    box.innerHTML += `

        <div class="bot-message">

            ${data.response}

        </div>
    `;

    box.scrollTop =
        box.scrollHeight;
}

/* =========================
   OPERASYON OLAYLARI
========================= */

function startFeedLoop(){

    const events = [

        {
            title:"Yeni Sipariş",
            text:"İstanbul bölgesinden yeni sipariş oluşturuldu.",
            color:"blue"
        },

        {
            title:"Kritik Stok",
            text:"Apple Magic Keyboard stok seviyesi kritik.",
            color:"yellow"
        },

        {
            title:"Teslimat Tamamlandı",
            text:"1 sipariş başarıyla teslim edildi.",
            color:"green"
        },

        {
            title:"Gecikme Tespiti",
            text:"Bursa gönderisinde gecikme riski algılandı.",
            color:"red"
        }
    ];

    setInterval(() => {

        const random =
            events[
                Math.floor(
                    Math.random() *
                    events.length
                )
            ];

        addFeedItem(
            random.title,
            random.text,
            random.color
        );

    }, 7000);
}

/* =========================
   INIT
========================= */

async function init(){

    await loadDashboard();

    await loadOrders();

    await loadInventory();

    await loadAnalytics();

    startFeedLoop();
}