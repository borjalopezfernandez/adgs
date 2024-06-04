from typing import Any
import os
import uvicorn
import logging

from uuid import UUID
from fastapi import FastAPI
from fastapi import Depends, status
from fastapi.responses import JSONResponse, Response
from fastapi.encoders import jsonable_encoder

from sqlalchemy.orm import Session

# -------------------------------------
# application specific

from .database import engine, get_db
from . import crud, models, schemas
from .routers import subscription_notification_endpoint
# -------------------------------------


logging.basicConfig(
    level=logging.INFO, format="%(levelname)-9s %(asctime)s - %(name)s - %(message)s"
)

logger = logging.getLogger(__name__)

if os.environ.get('AUXIP_DEBUG_MODE') is not None:
    if os.environ.get("AUXIP_DEBUG_MODE").lower() == 'true':
        logger.setLevel(logging.DEBUG)
        logger.debug("AUXIP debug mode is active")
else:
    logger.info("AUXIP debug mode off")


logger.info("AUXIP backend init")

# -------------------------------------
# TO-DO:
# create the db model
# it should be done outside with alembic
# logger.debug("Creating database => models.Base.metadata.create_all(bind=engine)")
# models.Base.metadata.create_all(bind=engine)

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
app.version     = "0.0.3"
app.description = "Here's a longer description of the custom **ADGS** service"

# this is is a simulated end-point for notification
app.include_router(subscription_notification_endpoint.router)

list_subscription = []

# -------------------------------------


@app.get("/")
def read_root():
    return {"not": "supported"}


@app.get("/test")
async def test_db(db: Session = Depends(get_db)):
    return {"test": "database"}


# -------------------------------------------------------------------

"""
    AUXIP Create Subscription
"""


@app.post("/odata/v1/Subscription",
    tags            = ["Subscriptions"],
    status_code     = status.HTTP_201_CREATED,
    response_model  = schemas.SubscriptionOutput,
)
async def create_subscription(subscription: schemas.Subscription, db: Session = Depends(get_db)) -> Any:
    """
    Create a Subscription with the following parameters:

    - **FilterParam**: Subscription filter params (refers to the $filter= parameter of any Products? query)
    - **NotificationEndpoint**: URI used by the AUXIP for subscription notifications
    - **NotificationEpUsername**: The username associated with the EndPoint URI provided
    - **NotificationEpPassword**: The password associated with the EndPoint URI provided
    - **Status**: SubscriptionStatus value: running (0) paused (1) cancelled (2)
    """
    logger.debug("/post create_subscription")
    logger.debug(subscription)
    list_subscription.append(subscription)
    return crud.create_subscription(db=db, subscription=subscription)

# --------------------------------------------------------------------

"""
    AUXIP Get Subscription by ID
"""


@app.get("/odata/v1/Subscription/{id}",
    tags            = ["Subscriptions"],
    status_code     = status.HTTP_200_OK,
    response_model  = schemas.SubscriptionOutput,
)
async def get_subcription(id: str, db: Session = Depends(get_db)) -> schemas.Subscription:
    logger.debug(f"/get subscription {id}") 
    subscription_id     = schemas.SubscriptionId(Id=UUID(id))
    db_subscription     = crud.get_subscription(db=db, subscription_id=subscription_id)
    subscription        = schemas.Subscription( Id                      = db_subscription.Id,
                                                Status                  = db_subscription.Status,
                                                SubmissionDate          = db_subscription.SubmissionDate,
                                                FilterParam             = db_subscription.FilterParam, 
                                                LastNotificationDate    = db_subscription.LastNotificationDate,
                                                NotificationEndpoint    = db_subscription.NotificationEndpoint,
                                                NotificationEpUsername  = db_subscription.NotificationEpUsername,
                                                NotificationEpPassword  = db_subscription.NotificationEpPassword
                                                )
    
    headers             = {"x-get-subscription-notificationepusername": subscription.NotificationEpUsername,
                            "Content-Language": "en-UK"}
    return Response(content=subscription.model_dump_json(), media_type= "application/json", headers=headers)

# --------------------------------------------------------------------

"""
    AUXIP Get List of Subscription ID
"""


@app.get("/odata/v1/Subscriptions/Id",
    tags            = ["Subscriptions"],
    status_code     = status.HTTP_200_OK,
)
async def get_subcription_list_id(db: Session = Depends(get_db)):
    logger.debug(f"/get subcription_list_id {id}")
    db_list_id              = crud.get_subscription_list_id(db=db)
    list_subscription_id    = []
    # list of <class 'sqlalchemy.engine.row.Row'>
    for row in db_list_id:
        list_subscription_id.append( schemas.SubscriptionId( Id = str(row[0]) ) )
    return(list_subscription_id)


# --------------------------------------------------------------------

"""
    AUXIP Update Subscription Status
"""


@app.put("/odata/v1/Subscription/Status", tags=["Subscriptions"])
async def update_subscription_status(sub_status: schemas.SubscriptionStatus, db: Session = Depends(get_db)) -> Any:
    logger.debug("/put update subscription status")
    logger.debug(sub_status)
    return crud.update_subscription_status(db=db, subscription_status=sub_status)

# --------------------------------------------------------------------

# -------------------------------------
if __name__ == "__main__":
    uvicorn.run("main:app", host = "0.0.0.0", port = 8000, reload = True, debug = True, proxy_headers = True)
# -------------------------------------
