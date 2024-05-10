from fastapi import FastAPI

from .middlewares import request_handler
from .routers import setup_routes
from .events import lifespan
from .settings import api_docs_settings


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
# app.middleware("http")(request_handler)
setup_routes(app)

#########################