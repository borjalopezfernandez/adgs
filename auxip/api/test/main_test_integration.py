import sys
import pytest
import datetime
import requests
import logging as logger
import json
from uuid import UUID

from starlette.testclient import TestClient

from auxip_backend.models import subscriptions
import auxip_backend.schemas.subscriptions as schemas
import auxip_backend.crud.crud_subscriptions as crud
from auxip_backend.config import Settings

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session

from auxip_backend.main import app

subscription_id             = None
notification_end_point      = "http://localhost:8000/test/EP/Notification/ProductAvailability"
notification_end_point_unav = "http://cannotreachme:1234/test/EP/Notification/ProductAvailability"


SQLALCHEMY_DATABASE_URL = Settings.database_url
engine                  = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal            = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db                      = SessionLocal()
   

@pytest.fixture(scope = "function", autouse = False)
def init_db():
    print()
    print('init_db() start')
    subscriptions.Base.metadata.drop_all(bind=engine)
    subscriptions.Base.metadata.create_all(bind=engine)
    print('init_db() end')
   


@pytest.fixture
def client():
    return TestClient(app)



@pytest.fixture
def print_separator():
    print("\n=========================================================================")



def test_subscription_cycle(client, init_db, print_separator):
    """
    GIVEN some subscription input
    WHEN posting the subscription input
    THEN response with status 200
    """
    print(f"START : {sys._getframe().f_code.co_name}")
    
    print("POST /odata/v1/Subscription")
    
    subs = {
        "FilterParam": "contains(Name,'AUX_UT1UTC')",
        "NotificationEndpoint": notification_end_point,
        "NotificationEpUsername": "",
        "NotificationEpPassword": "",
        "Status": "0"
    }

    response = client.post("/odata/v1/Subscription", json=subs)
    assert response.status_code == 201
    json_data = response.json()
    print(json_data)

    id              = json_data['Id']
    subscription_id = id
    subs_id         = {'Id' : id}
    json_subs_id    = json.dumps(subs_id)
    print(json_subs_id)

    url = f"/odata/v1/Subscription/{id}"
    print(f"GET {url}")

    response = client.get(url)
    assert response.status_code == 200
    print(response.headers)

    subs_update      = {'Id' : id, 'Status' : '0' }
    print(subs_update)

    print("PUT /odata/v1/Subscription/Status")
    response = client.put("/odata/v1/Subscription/Status", json=subs_update)
    print(response)
    assert response.status_code == 200

    subs_update      = {'Id' : id, 'Status' : '0' }
    print()
    print(subs_update)

    print(f"END : {sys._getframe().f_code.co_name}")



def test_subscription_notification(client, print_separator):
    """
    GIVEN some subscription input
    WHEN posting the subscription input
    THEN response with status 200
    """
    print(f"START : {sys._getframe().f_code.co_name}")
    
    print("GET /odata/v1/Subscriptions/Id")
    
    response = client.get("/odata/v1/Subscriptions/Id")
    assert response.status_code == 200
    json_data = response.json()

    subscription_id = json_data[0]['Id']
    print(subscription_id)
    
    now     = datetime.datetime.utcnow()
    str_now = now.strftime("%Y-%m-%dT%H:%M:%S.000Z")


    subscription_product_notification = {
        "NotificationDate": str_now,
        "ProductId": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "ProductName": "S2__OPER_AUX_UT1UTC_PDMC_20240513T000000_V20170101T000000_21000101T000000.7z",
        "SubscriptionId": subscription_id
    }

    print(f"POST {notification_end_point}")
    response = client.post(notification_end_point, json=subscription_product_notification)
    assert response.status_code == 200
    json_data = response.json()
    print(json_data)

    notification_success  = schemas.SubscriptionNotificationDB(NotificationSuccess = True,
                                                                NotificationInfo   = str(json_data),
                                                                ProductId           = UUID("3fa85f64-5717-4562-b3fc-2c963f66afa6"),
                                                                ProductName         = "S2__OPER_AUX_UT1UTC_PDMC_20240513T000000_V20170101T000000_21000101T000000.7z",
                                                                Success             = False,
                                                                SubscriptionId      = UUID(subscription_id),
                                                                NotificationDate    = now
                                                                )
    print("after pydantic")
    crud.create_subscription_notification_product(db = db, notification = notification_success)

    print(f"END : {sys._getframe().f_code.co_name}")



def failure_test_subscription_notification(client, print_separator):
    """
    GIVEN some subscription product notification
    WHEN posting to some unavailable / unreachable EP
    THEN response with status != 200
    """
    print(f"START : {sys._getframe().f_code.co_name}")
    
    print("GET /odata/v1/Subscriptions/Id")
    
    response = client.get("/odata/v1/Subscriptions/Id")
    assert response.status_code == 200
    json_data = response.json()
    print(json_data)

    subscription_id = json_data[0]['Id']
    print(subscription_id)
    
    now     = datetime.datetime.utcnow()
    str_now = now.strftime("%Y-%m-%dT%H:%M:%S.000Z")

    subscription_product_notification = {
        "NotificationDate": str_now,
        "ProductId": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "ProductName": "S2__OPER_AUX_UT1UTC_PDMC_20240513T000000_V20170101T000000_21000101T000000.7z",
        "SubscriptionId": subscription_id
    }

    print(subscription_product_notification)

    print(f"POST {notification_end_point_unav}")

    try:
        post_response = requests.post(notification_end_point_unav, json = subscription_product_notification)
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")
        print("before pydantic")
        notification_error  = schemas.SubscriptionNotificationDB(NotificationSuccess = False,
                                                                NotificationInfo   = str(err),
                                                                ProductId           = UUID("3fa85f64-5717-4562-b3fc-2c963f66afa6"),
                                                                ProductName         = "S2__OPER_AUX_UT1UTC_PDMC_20240513T000000_V20170101T000000_21000101T000000.7z",
                                                                SubscriptionId      = UUID(subscription_id),
                                                                NotificationDate    = now
                                                                )
        print("after pydantic")
        crud.create_subscription_notification_product(db = db, notification = notification_error)


    print(f"END : {sys._getframe().f_code.co_name}")