from typing import Any
import uvicorn
import os

from fastapi import FastAPI
from fastapi import Depends, status
from fastapi.middleware.cors import CORSMiddleware

from sqlalchemy.orm import Session

# -------------------------------------
# application specific
from .database import engine, get_db, Base
from .logger import logger
# -------------------------------------

# -------------------------------------
# api routers:
from .routers import subscriptions
from .routers import products
from .routers import metrics
from .routers import test_api
from .routers import subscription_notification_endpoint
# -------------------------------------

# Ensure the auxip table(s) model is created
from .models import subscriptions as model_subscriptions
model_subscriptions.Base.metadata.create_all(bind=engine)

logger.info("AUXIP backend init")

# -------------------------------------
# create the fastapi application

tags_metadata = [
    {
        "name": "Subscriptions",
        "description": "Operations with Subscriptions",
    },
    {
        "name": "Notifications",
        "description": "Simulator of Notification End-Points",
    },
    {
        "name": "Products",
        "description": "Products",
        "externalDocs": {
            "description": "Items external docs",
            "url": "https://fastapi.tiangolo.com/",
        },
    },
    {
        "name": "Metrics",
        "description": "Operations with metrics",
    }
]

if "AUXIP_BASE_PATH" in os.environ:
    app             = FastAPI(openapi_tags=tags_metadata, servers = [{"url": os.environ["AUXIP_BASE_PATH"]}], root_path=os.environ["AUXIP_BASE_PATH"])
else:
    app             = FastAPI(openapi_tags=tags_metadata)
# end if

app.title       = "Auxiliary Data Gathering Service"
app.summary     = "AUXIP description"
app.version     = "0.0.4"
app.description = "Here's a longer description of the custom **ADGS** service"

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Router for subscriptions management
app.include_router(subscriptions.router)

# Router for products management
app.include_router(products.router)

# Router for a simulated end-point for subscription notification
app.include_router(subscription_notification_endpoint.router)

# Router for metrics management
app.include_router(metrics.router)

# Router for some dummy test api for sanity check
app.include_router(test_api.router)

# -------------------------------------------------------------------


# -------------------------------------
if __name__ == "__main__":
    uvicorn.run("main:app", host = "0.0.0.0", port = 8000, workers = 4, reload = True, debug = True, proxy_headers = True)
# -------------------------------------
