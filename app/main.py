from loguru import logger

from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

# from .middlewares import request_handler
from .routers import setup_routes
from .events import lifespan
from .settings import api_docs_settings, stripe_settings


#########################
# app lifespan processes

app = FastAPI(
    title=api_docs_settings.title,
    description=api_docs_settings.description,
    version=api_docs_settings.version,
    contact={
        "name": api_docs_settings.contact_name,
        "email": api_docs_settings.contact_email,
    },
    docs_url="/docs",
    openapi_url="/openapi.json",
    redoc_url="/redoc",
    lifespan=lifespan
)

# add jinja templates
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# add middlewares
# app.middleware("http")(request_handler)

# add routes
setup_routes(app)

@app.get('/')
def root(request: Request):
    return templates.TemplateResponse("index.html", 
        {
            "request": request,
            "STRIPE_PUBLIC_KEY": stripe_settings.public_key,
            "STRIPE_PREMIUM_PRICE_ID": stripe_settings.premium_price_id,
            "STRIPE_BASIC_PRICE_ID": stripe_settings.basic_price_id
        }
    )


@app.get('/success')
def success(request: Request):
    return templates.TemplateResponse("success.html", {"request": request})

@app.get('/cancel')
def cancel(request: Request):
    return templates.TemplateResponse("cancel.html", {"request": request})

#########################