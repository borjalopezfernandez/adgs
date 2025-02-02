from typing import Any
from uuid import UUID
from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse, Response

from .. database import get_db
from .. import logger as app_logger
from .. crud import crud_subscriptions as crud
from .. schemas import subscriptions

from sqlalchemy.orm import Session

app_logger.logger.info(f"API Router start => {__name__}")

router = APIRouter(
   tags           = ["Subscriptions"], 
   dependencies   = [Depends(get_db) ]
)

# -------------------------------------------------------------------

"""
    AUXIP Create Subscription
"""


@router.post("/odata/v1/Subscription",
   status_code     = status.HTTP_201_CREATED,
   response_model  = subscriptions.SubscriptionOutput,
)
async def create_subscription(subscription: subscriptions.Subscription, db: Session = Depends(get_db)) -> Any:
    """
    Create a Subscription with the following parameters:

    - **FilterParam**: Subscription filter params (refers to the $filter= parameter of any Products? query)
    - **NotificationEndpoint**: URI used by the AUXIP for subscription notifications
    - **NotificationEpUsername**: The username associated with the EndPoint URI provided
    - **NotificationEpPassword**: The password associated with the EndPoint URI provided
    - **Status**: SubscriptionStatus value: running (0) paused (1) cancelled (2)
    """
    app_logger.logger.debug("/post create_subscription")
    app_logger.logger.debug(subscription)
    return crud.create_subscription(db = db, subscription = subscription)

# -------------------------------------------------------------------

# -------------------------------------------------------------------

"""
    AUXIP Get List of Subscription ID
"""

@router.get("/odata/v1/Subscriptions/Id", 
      status_code = status.HTTP_200_OK
)
async def get_subcription_list_id(db: Session = Depends(get_db)):
   app_logger.logger.debug("/get subcription_list_id")
   db_list_id              = crud.get_subscription_list_id(db=db)
   list_subscription_id    = []
   # list of <class 'sqlalchemy.engine.row.Row'>
   for row in db_list_id:
      list_subscription_id.append( subscriptions.SubscriptionId( Id = str(row[0]) ) )
   return(list_subscription_id)


# -------------------------------------------------------------------

# -------------------------------------------------------------------

"""
    AUXIP Get Subscription by ID
"""


@router.get("/odata/v1/Subscription/{id}",
    tags            = ["Subscriptions"],
    status_code     = status.HTTP_200_OK,
    response_model  = subscriptions.SubscriptionOutput,
)
async def get_subcription(id: str, db: Session = Depends(get_db)) -> subscriptions.Subscription:
   app_logger.logger.debug(f"/get subscription {id}") 
   subscription_id     = subscriptions.SubscriptionId(Id=UUID(id))
   db_subscription     = crud.get_subscription(db=db,   subscription_id = subscription_id)
   subscription        = subscriptions.Subscription(  Id                      = db_subscription.Id,
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

# --------------------------------------------------------------------

"""
    AUXIP Update Subscription Status
"""


@router.put("/odata/v1/Subscription/Status", tags=["Subscriptions"])
async def update_subscription_status(sub_status: subscriptions.SubscriptionStatus, db: Session = Depends(get_db)) -> Any:
   app_logger.logger.debug("/put update subscription status")
   app_logger.logger.debug(sub_status)
   return crud.update_subscription_status(db = db, subscription_status = sub_status)

# --------------------------------------------------------------------