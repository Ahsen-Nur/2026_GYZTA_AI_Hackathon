from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.database import SessionLocal
from app.models import Order, Inventory
from app.ai_logic import generate_ai_response

app = FastAPI()

# STATIC
app.mount(
    "/static",
    StaticFiles(directory="app/static"),
    name="static"
)

# TEMPLATES
templates = Jinja2Templates(
    directory="app/templates"
)

# HOME
@app.get("/", response_class=HTMLResponse)
def home(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="index.html"
    )

# DASHBOARD
@app.get("/dashboard")
def dashboard():

    db = SessionLocal()

    orders = db.query(Order).all()
    inventory = db.query(Inventory).all()

    delayed = len(
        [o for o in orders if o.status == "Delayed"]
    )

    critical = len(
        [i for i in inventory if i.status == "Critical"]
    )

    revenue = 143500

    return {
        "total_orders": len(orders),
        "delayed_orders": delayed,
        "critical_stock": critical,
        "revenue": revenue
    }

# ORDERS
@app.get("/orders")
def get_orders():

    db = SessionLocal()

    orders = db.query(Order).all()

    return [
        {
            "id": o.id,
            "customer": o.customer,
            "product": o.product,
            "status": o.status,
            "city": o.city
        }
        for o in orders
    ]

# INVENTORY
@app.get("/inventory")
def get_inventory():

    db = SessionLocal()

    inventory = db.query(Inventory).all()

    return [
        {
            "product": i.product,
            "stock": i.stock,
            "status": i.status
        }
        for i in inventory
    ]

# ANALYTICS
@app.get("/analytics")
def analytics():

    db = SessionLocal()

    orders = db.query(Order).all()

    inventory = db.query(Inventory).all()

    top_product = {}

    for order in orders:

        if order.product not in top_product:
            top_product[order.product] = 0

        top_product[order.product] += 1

    most_sold = max(
        top_product,
        key=top_product.get
    )

    delayed = len([
        o for o in orders
        if o.status == "Delayed"
    ])

    critical = len([
        i for i in inventory
        if i.status == "Critical"
    ])

    active_customers = len(set([
        o.customer for o in orders
    ]))

    return {

        "top_product": most_sold,

        "predicted_demand":
            f"{most_sold} trending upward",

        "risk_analysis":
            f"{delayed} delayed shipments",

        "active_customers":
            f"{active_customers} active customers",

        "critical_stock":
            critical
    }

# CHAT
@app.post("/chat")
async def chat(request: Request):

    data = await request.json()

    message = data["message"]

    db = SessionLocal()

    orders = db.query(Order).all()

    response = generate_ai_response(
        message,
        orders
    )

    return {
        "response": response
    }