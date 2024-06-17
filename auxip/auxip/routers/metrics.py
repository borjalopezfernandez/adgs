"""
API for querying Auxiliary Data Delivery Interface Points Metrics

module auxip
"""
# Import python utilities
from datetime import datetime
import re
import os

# Import FastAPI utilities
from fastapi import APIRouter, status, Depends, Form, Query, HTTPException
from fastapi.responses import JSONResponse, Response
from typing import Union, Any, Annotated

# Import requests
import requests

# Import AUXIP utilities
from .. logger import logger as logger
from .. schemas import metrics
from .. import errors

# Import Pydantic utilities
from pydantic import Field

router = APIRouter(
    tags = ["Metrics"]
)

"""
    AUXIP Metrics
"""

PLATFORM_SHORT_NAME_MAPPING = {
    "SENTINEL-1": "S1_",
    "SENTINEL-2": "S2_",
    "SENTINEL-3": "S3_",
    "SENTINEL-5P": "S5P"
}

adgsboa_host = None
adgsboa_port = None
if "ADGSBOA_HOST" in os.environ:
    # Get host to access ADGSBOA
    adgsboa_host = os.environ["ADGSBOA_HOST"]
else:
    raise errors.EnvironmentVariableNotDefined("The environment variable ADGSBOA_HOST is not defined")
# end if
if "ADGSBOA_PORT" in os.environ:
    # Get port to access ADGSBOA
    adgsboa_port = os.environ["ADGSBOA_PORT"]
else:
    raise errors.EnvironmentVariableNotDefined("The environment variable ADGSBOA_PORT is not defined")
# end if

@router.get("/odata/v1/Metrics",
            status_code = status.HTTP_200_OK,
            response_model = metrics.Metric
)
async def serve_metrics(filter: str = Query(alias="$filter")) -> metrics.Metric:
    """
    Serve AUXIP metrics with the following parameters:

    - **$filter**: Metrics filter params (refers to the $filter= parameter of any Metrics? query)
    """

    logger.info(f"Serving metrics using the provided query: {filter}")
    # Parse filter
    query_pattern = re.compile(r"Name eq '([^.]+\.[^.]+\.[^.]+\.size|" \
                               "[^.]+\.[^.]+\.[^.]+\.count|" \
                               "[^.]+\.[^.]+\.size|" \
                               "Download\.[^.]+\.[^.]+\.[^.]+\.[^.]+\.size|" \
                               "Download\.[^.]+\.[^.]+\.[^.]+\.[^.]+\.completed|" \
                               "Download\.[^.]+\.[^.]+\.[^.]+\.[^.]+\.failed|" \
                               "OriginToPublication\.Daily\.min\.time\.[^.]+\.[^.]+\.[^.]+|" \
                               "OriginToPublication\.Daily\.max\.time\.[^.]+\.[^.]+\.[^.]+|" \
                               "OriginToPublication\.Daily\.avg\.time\.[^.]+\.[^.]+\.[^.]+|" \
                               "OriginToPublication\.Monthly\.min\.time\.[^.]+\.[^.]+\.[^.]+|" \
                               "OriginToPublication\.Monthly\.max\.time\.[^.]+\.[^.]+\.[^.]+|" \
                               "OriginToPublication\.Monthly\.avg\.time\.[^.]+\.[^.]+\.[^.]+|" \
                               "Service\.[^.]+\.value)'")

    # TODO create API in ADGSBOA to serve the name of a client or a platform from the aliases
    
    if not query_pattern.fullmatch(filter):
        error_message = f"The provided query filters do not match the expected values. The query filters should match the pattern: {query_pattern.pattern}"
        logger.error(error_message)
        raise HTTPException(status_code=400, detail=error_message)
    # end if
    
    metric = filter.replace("Name eq ", "").replace("'", "")

    # Set metric metadata for OData
    metric_type = "Counter"
    metric_value_label = "Count"
    
    logger.info(f"The query is going to provide the metric: {metric}")

    if re.compile(r"[^.]+\.[^.]+\.[^.]+\.size").fullmatch(metric):
        logger.info(f"Metric <productType>.<platformShortName>.<platformSerialIdentifier>.size has been requested")
        # Extract metric fields
        metric_fields = metric.split(".")
        product_type = metric_fields[0]
        platform_short_name = metric_fields[1]
        platform_serial_identifier = metric_fields[1]
    elif re.compile(r"[^.]+\.[^.]+\.[^.]+\.count").fullmatch(metric):
        logger.info(f"Metric <productType>.<platformShortName>.<platformSerialIdentifier>.count has been requested")
        # Extract metric fields
        metric_fields = metric.split(".")
        product_type = metric_fields[0]
        platform_short_name = metric_fields[1]
        platform_serial_identifier = metric_fields[1]
    elif re.compile(r"[^.]+\.[^.]+\.size").fullmatch(metric):
        logger.info(f"Metric <platformShortName>.<platformSerialIdentifier>.size has been requested")
        # Extract metric fields
        metric_fields = metric.split(".")
        platform_short_name = metric_fields[0]
        platform_serial_identifier = metric_fields[1]
    elif re.compile(r"Download\.[^.]+\.[^.]+\.[^.]+\.[^.]+\.size").fullmatch(metric):
        logger.info(f"Metric Download.<productType>.<platformShortName>.<platformSerialIdentifier>.<ServiceAlias>.size has been requested")
        # Extract metric fields
        metric_fields = metric.split(".")
        product_type = metric_fields[1]
        platform_short_name = metric_fields[2]
        platform_serial_identifier = metric_fields[3]
        service_alias = metric_fields[4]

        # Build gauge for BOA query
        mission = PLATFORM_SHORT_NAME_MAPPING[platform_short_name].replace("_", platform_serial_identifier)
        gauge_name = "CUMULATIVE_DOWNLOADED_VOLUME_BY_MISSION_PRODUCT_TYPE_CLIENT"
        gauge_system = f"{mission}#{product_type}#{service_alias}"
    elif re.compile(r"Download\.[^.]+\.[^.]+\.[^.]+\.[^.]+\.completed").fullmatch(metric):
        logger.info(f"Metric Download.<productType>.<platformShortName>.<platformSerialIdentifier>.<ServiceAlias>.completed has been requested")
        # Extract metric fields
        metric_fields = metric.split(".")
        product_type = metric_fields[1]
        platform_short_name = metric_fields[2]
        platform_serial_identifier = metric_fields[3]
        service_alias = metric_fields[4]

        # Build gauge for BOA query
        mission = PLATFORM_SHORT_NAME_MAPPING[platform_short_name].replace("_", platform_serial_identifier)
        gauge_name = "CUMULATIVE_DOWNLOADED_NUMBER_BY_MISSION_PRODUCT_TYPE_CLIENT"
        gauge_system = f"{mission}#{product_type}#{service_alias}"
    elif re.compile(r"Download\.[^.]+\.[^.]+\.[^.]+\.[^.]+\.failed").fullmatch(metric):
        logger.info(f"Metric Download.<productType>.<platformShortName>.<platformSerialIdentifier>.<ServiceAlias>.failed has been requested")
        # Extract metric fields
        metric_fields = metric.split(".")
        product_type = metric_fields[1]
        platform_short_name = metric_fields[2]
        platform_serial_identifier = metric_fields[3]
        service_alias = metric_fields[4]
    elif re.compile(r"OriginToPublication\.Daily\.min\.time\.[^.]+\.[^.]+\.[^.]+").fullmatch(metric):
        logger.info(f"Metric OriginToPublication.Daily.min.time.<productType>.<platformShortName>.<platformSerialIdentifier> has been requested")
        # Set metric metadata for OData
        metric_type = "Gauge"
        metric_value_label = "Gauge"

        # Extract metric fields
        metric_fields = metric.split(".")
        product_type = metric_fields[4]
        platform_short_name = metric_fields[5]
        platform_serial_identifier = metric_fields[6]
    elif re.compile(r"OriginToPublication\.Daily\.max\.time\.[^.]+\.[^.]+\.[^.]+").fullmatch(metric):
        logger.info(f"Metric OriginToPublication.Daily.max.time.<productType>.<platformShortName>.<platformSerialIdentifier> has been requested")
        # Set metric metadata for OData
        metric_type = "Gauge"
        metric_value_label = "Gauge"

        # Extract metric fields
        metric_fields = metric.split(".")
        product_type = metric_fields[4]
        platform_short_name = metric_fields[5]
        platform_serial_identifier = metric_fields[6]
    elif re.compile(r"OriginToPublication\.Daily\.avg\.time\.[^.]+\.[^.]+\.[^.]+").fullmatch(metric):
        logger.info(f"Metric OriginToPublication.Daily.avg.time.<productType>.<platformShortName>.<platformSerialIdentifier> has been requested")
        # Set metric metadata for OData
        metric_type = "Gauge"
        metric_value_label = "Gauge"

        # Extract metric fields
        metric_fields = metric.split(".")
        product_type = metric_fields[4]
        platform_short_name = metric_fields[5]
        platform_serial_identifier = metric_fields[6]
    elif re.compile(r"OriginToPublication\.Monthly\.min\.time\.[^.]+\.[^.]+\.[^.]+").fullmatch(metric):
        logger.info(f"Metric OriginToPublication.Monthly.min.time.<productType>.<platformShortName>.<platformSerialIdentifier> has been requested")
        # Set metric metadata for OData
        metric_type = "Gauge"
        metric_value_label = "Gauge"

        # Extract metric fields
        metric_fields = metric.split(".")
        product_type = metric_fields[4]
        platform_short_name = metric_fields[5]
        platform_serial_identifier = metric_fields[6]
    elif re.compile(r"OriginToPublication\.Monthly\.max\.time\.[^.]+\.[^.]+\.[^.]+").fullmatch(metric):
        logger.info(f"Metric OriginToPublication.Monthly.max.time.<productType>.<platformShortName>.<platformSerialIdentifier> has been requested")
        # Set metric metadata for OData
        metric_type = "Gauge"
        metric_value_label = "Gauge"

        # Extract metric fields
        metric_fields = metric.split(".")
        product_type = metric_fields[4]
        platform_short_name = metric_fields[5]
        platform_serial_identifier = metric_fields[6]
    elif re.compile(r"OriginToPublication\.Monthly\.avg\.time\.[^.]+\.[^.]+\.[^.]+").fullmatch(metric):
        logger.info(f"Metric OriginToPublication.Monthly.avg.time.<productType>.<platformShortName>.<platformSerialIdentifier> has been requested")
        # Set metric metadata for OData
        metric_type = "Gauge"
        metric_value_label = "Gauge"

        # Extract metric fields
        metric_fields = metric.split(".")
        product_type = metric_fields[4]
        platform_short_name = metric_fields[5]
        platform_serial_identifier = metric_fields[6]
    elif re.compile(r"Service\.[^.]+\.value").fullmatch(metric):
        logger.info(f"Metric Service.<KPI>.value has been requested")
        # Set metric metadata for OData
        metric_type = "Gauge"
        metric_value_label = "Gauge"

        # Extract metric fields
        metric_fields = metric.split(".")
        kpi = metric_fields[1]
    else:
        error_message = f"Requested metric {metric} is not available"
        logger.error(error_message)
        raise HTTPException(status_code=400, detail=error_message)
    # end if    
    
    # Query metrics to BOA
    query_filters = {
        "events": {
            "gauge_names": {
                "filter": gauge_name,
                "op": "=="
            },
            "gauge_systems": {
                "filter": gauge_system,
                "op": "=="
            }
        }
    }

    adgsboa_url = f"http://{adgsboa_host}:{adgsboa_port}/query/"
    logger.info(f"The metric is going to be requested to ADGSBOA ({adgsboa_url}) for the gauge with name {gauge_name} and system {gauge_system}")
    response = requests.get(url=adgsboa_url, json=query_filters)

    if response.status_code != 200:
        error_message = f"There was a failure requesting the metric {metric} to ADGSBOA. Response code was {response.status_code}"
        logger.error(error_message)
        raise HTTPException(status_code=500, detail=error_message)
    else:
        response_json = response.json()
        if "data" in  response_json and "events" in response_json["data"] and len(response_json["data"]["events"].keys()) > 0:
            event_uuid = response_json["data"]["event_groups"]["events"][0]
            event = response_json["data"]["events"][event_uuid]
            metric_value = int(float(event["indexed_values"]["value"][0]["value"]))

            logger.info(f"Metric value associated to metric {metric} successfully obtained from ADGSBOA: {metric_value}")
        else:
            error_message = f"The metric {metric} is not available from the ADGSBOA"
            logger.error(error_message)
            raise HTTPException(status_code=500, detail=error_message)            
        # end if
    # end if
    
    timestamp = datetime.now().isoformat() + "Z"
    
    result = {
        "@odata.context": "auxip/$metadata#Metrics",
        "value": [
            {
                "Name": metric,
                "Timestamp": timestamp,
                "MetricType": metric_type,
                metric_value_label: metric_value
            }
        ]
    }
    
    return result
