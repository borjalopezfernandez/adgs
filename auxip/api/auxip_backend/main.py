from typing import Any
import uvicorn


from fastapi import FastAPI
from fastapi import Depends, status

from fastapi.encoders import jsonable_encoder

from sqlalchemy.orm import Session

# -------------------------------------
# application specific

from .database import engine, get_db
from . import crud, models, schemas
from .logger import logger
# -------------------------------------

# -------------------------------------
# api routers:
from .routers import subscriptions
from .routers import test_api
from .routers import subscription_notification_endpoint
# -------------------------------------

# Ensure the tables model is created
models.Base.metadata.create_all(bind=engine)

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
]

app             = FastAPI(openapi_tags=tags_metadata)
app.title       = "Auxiliary Data Gathering Service"
app.summary     = "AUXIP description"
app.version     = "0.0.4"
app.description = "Here's a longer description of the custom **ADGS** service"


# Router for subscriptions management
app.include_router(subscriptions.router)

# Router for a simulated end-point for subscription notification
app.include_router(subscription_notification_endpoint.router)

# Router for some dummy test api for sanity check
app.include_router(test_api.router)

# -------------------------------------------------------------------


# -------------------------------------
if __name__ == "__main__":
    uvicorn.run("main:app", host = "0.0.0.0", port = 8000, reload = True, debug = True, proxy_headers = True)
# -------------------------------------
