async function loadDashboard() {

    const res = await fetch("/dashboard");
    const data = await res.json();

    document.getElementById("total-orders").innerText = data.total_orders;
    document.getElementById("delayed-orders").innerText = data.delayed_orders;
    document.getElementById("critical-stock").innerText = data.critical_stock;
    document.getElementById("revenue").innerText = "₺" + data.revenue;
}

async function loadOrders() {

    const res = await fetch("/orders");
    const data = await res.json();

    const table = document.getElementById("orders-table");
    const management = document.getElementById("orders-management-table");

    table.innerHTML = "";
    management.innerHTML = "";

    data.forEach(order => {

        table.innerHTML += `
        <tr>
            <td>#${order.id}</td>
            <td>${order.customer}</td>
            <td>${order.status}</td>
            <td>${order.city}</td>
        </tr>
        `;

        management.innerHTML += `
        <tr>
            <td>#${order.id}</td>
            <td>${order.customer}</td>
            <td>${order.product}</td>
            <td>${order.status}</td>
        </tr>
        `;
    });
}

async function loadInventory() {

    const res = await fetch("/inventory");
    const data = await res.json();

    const table = document.getElementById("inventory-table");

    table.innerHTML = "";

    data.forEach(item => {

        table.innerHTML += `
        <tr>
            <td>${item.product}</td>
            <td>${item.stock}</td>
            <td>${item.status}</td>
        </tr>
        `;
    });
}

async function loadAnalytics() {

    const res = await fetch("/analytics");
    const data = await res.json();

    document.getElementById("top-product").innerText = data.top_product;
    document.getElementById("predicted-demand").innerText = data.predicted_demand;
    document.getElementById("risk-analysis").innerText = data.risk_analysis;
    document.getElementById("active-customers").innerText = data.active_customers;
}

async function sendMessage() {

    const input = document.getElementById("message-input");

    const message = input.value;

    const box = document.getElementById("chat-box");

    box.innerHTML += `
    <div class="user-message">${message}</div>
    `;

    const res = await fetch("/chat", {

        method: "POST",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify({
            message: message
        })
    });

    const data = await res.json();

    box.innerHTML += `
    <div class="bot-message">${data.response}</div>
    `;

    input.value = "";

    box.scrollTop = box.scrollHeight;
}

function showSection(sectionName) {

    const sections = [

        "dashboard-section",
        "orders-section",
        "inventory-section",
        "analytics-section"

    ];

    sections.forEach(id => {

        document
            .getElementById(id)
            .classList.add("hidden-section");
    });

    document
        .getElementById(sectionName + "-section")
        .classList.remove("hidden-section");

    document
        .querySelectorAll(".nav-item")
        .forEach(item => item.classList.remove("active"));

    event.target.classList.add("active");
}

loadDashboard();
loadOrders();
loadInventory();
loadAnalytics();

async function loadChart() {

    const res =
        await fetch("/orders");

    const data =
        await res.json();

    const cityCounts = {};

    data.forEach(order => {

        if (!cityCounts[order.city]) {
            cityCounts[order.city] = 0;
        }

        cityCounts[order.city]++;
    });

    const ctx =
        document
        .getElementById("ordersChart");

    new Chart(ctx, {

        type: "bar",

        data: {

            labels:
                Object.keys(cityCounts),

            datasets: [{

                label:
                    "Orders by City",

                data:
                    Object.values(cityCounts),

                borderWidth: 1
            }]
        }
    });
}

loadChart();