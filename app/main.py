from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from fastapi.templating import Jinja2Templates
from fastapi.requests import Request

from app.routers.dashboard import (
    router as dashboard_router
)

from app.routers.orders import (
    router as orders_router
)

from app.routers.inventory import (
    router as inventory_router
)

from app.routers.analytics import (
    router as analytics_router
)

from app.routers.chat import (
    router as chat_router
)


from app.routers.customer_chat import (
    router as customer_chat_router
)


app = FastAPI(
    title="AI Operations Command Center"
)

app.mount(

    "/static",

    StaticFiles(
        directory="app/static"
    ),

    name="static"
)

templates = Jinja2Templates(

    directory="app/templates"
)

app.include_router(
    dashboard_router
)

app.include_router(
    orders_router
)

app.include_router(
    inventory_router
)

app.include_router(
    analytics_router
)

app.include_router(
    chat_router
)

app.include_router(
    customer_chat_router
)


@app.get("/")
def home(request: Request):

    return templates.TemplateResponse(

        request=request,

        name="index.html"
    )