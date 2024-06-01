import sys
import pytest
import logging as logger
import json
from starlette.testclient import TestClient

from auxip_backend.main import app


# https://stackoverflow.com/questions/67255653/how-to-set-up-and-tear-down-a-database-between-tests-in-fastapi
# https://github.com/tiangolo/fastapi/issues/4507


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def print_separator():
    print("\n=========================================================================")


def test_base_route(client):
    """
    GIVEN
    WHEN health check endpoint is called with GET method
    THEN response with status 200 and body OK is returned
    """
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"not": "supported"}


def test_db(client):
    """
    GIVEN
    WHEN health check endpoint is called with GET method
    THEN response with status 200 and body OK is returned
    """
    response = client.get("/test")
    assert response.status_code == 200
    assert response.json() == {"test": "database"}


def test_post_subscription(client, print_separator):
    """
    GIVEN some subscription input
    WHEN posting the subscription input
    THEN response with status 201
    """
    print(f"START : {sys._getframe().f_code.co_name}")
    
    print("POST /odata/v1/Subscription")

    subs = {
        "FilterParam": "contains(Name,'_AUX_ECMWFD_') and PublicationDate gt 2019-02-01T00:00:00.000Z and PublicationDate lt 2019-09-01T00:00:00.000Z",
        "NotificationEndpoint": "http://myserver.org",
        "NotificationEpPassword": "diLegno$",
        "NotificationEpUsername": "pinocchio",
        "Status": "0"
    }

    response = client.post("/odata/v1/Subscription", json=subs)
    assert response.status_code == 201
    json_data = response.json()
    print(json_data)
    print(f"END : {sys._getframe().f_code.co_name}")


def test_get_subscription(client, print_separator):
    """
    GIVEN some subscription input
    WHEN posting the subscription input
    THEN response with status 200
    """
    print(f"START : {sys._getframe().f_code.co_name}")
    
    print("POST /odata/v1/Subscription")
    
    subs = {
        "FilterParam": "contains(Name,'_AUX_ECMWFD_') and PublicationDate gt 2019-02-01T00:00:00.000Z and PublicationDate lt 2019-09-01T00:00:00.000Z",
        "NotificationEndpoint": "http://myserver.org",
        "NotificationEpPassword": "diLegno$",
        "NotificationEpUsername": "pinocchio",
        "Status": "0"
    }

    response = client.post("/odata/v1/Subscription", json=subs)
    assert response.status_code == 201
    json_data = response.json()
    print(json_data)

    id              = json_data['Id']
    subs_id         = {'Id' : id}
    json_subs_id    = json.dumps(subs_id)
    print(json_subs_id)

    url = f"/odata/v1/Subscription/{id}"
    print(f"GET {url}")

    response = client.get(url)
    assert response.status_code == 200
    print(response.headers)
    print(f"END : {sys._getframe().f_code.co_name}")


def test_put_subscription_status(client, print_separator):
    """
    GIVEN some subscription statut input
    WHEN PUT the subscription input
    THEN response with status 200
    """
    print(f"START : {sys._getframe().f_code.co_name}")
    
    print("POST /odata/v1/Subscription")
    # -----------------------
    # Create the subscription
    subs = {
        "FilterParam": "contains(Name,'_AUX_ECMWFD_') and PublicationDate gt 2019-02-01T00:00:00.000Z and PublicationDate lt 2019-09-01T00:00:00.000Z",
        "NotificationEndpoint": "http://myserver.org",
        "NotificationEpPassword": "diLegno$",
        "NotificationEpUsername": "perry",
        "Status": "0"
    }

    response = client.post("/odata/v1/Subscription", json=subs)
    assert response.status_code == 201
    json_data = response.json()
    print(f"Subscription {json_data['Id']} has status {json_data['Status']}")

    # -----------------------
    id = json_data['Id']
    subs_update      = {'Id' : id, 'Status' : '1' }
    print(subs_update)
    # avoid double json construction which introduces double quotes
    # json_subs_update = json.dumps(subs_update)
    # print(json_subs_update)

    print("PUT /odata/v1/Subscription/Status")
    response = client.put("/odata/v1/Subscription/Status", json=subs_update)
    print(response)
    assert response.status_code == 200

    subs_update      = {'Id' : id, 'Status' : '2' }
    print()
    print(subs_update)

    print("PUT /odata/v1/Subscription/Status")
    response = client.put("/odata/v1/Subscription/Status", json=subs_update)
    print(response)
    assert response.status_code == 200

    subs_update      = {'Id' : id, 'Status' : '0' }
    print()
    print(subs_update)

    print("PUT /odata/v1/Subscription/Status")
    response = client.put("/odata/v1/Subscription/Status", json=subs_update)
    print(response)
    assert response.status_code == 200

    print(f"END : {sys._getframe().f_code.co_name}")
   

def test_get_subscription_lisf_id(client, print_separator):
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
    print(json_data)
    print(json_data[0])
    print(json_data[0]['Id'])

    for element in json_data:
        id  = element['Id']
        url = f"/odata/v1/Subscription/{id}"
        print(f"GET {url}")
        response = client.get(url)
        assert response.status_code == 200
        print(response.headers)
        print("\n************")
