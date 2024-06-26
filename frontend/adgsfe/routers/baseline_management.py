"""
Defintion of the AUXIP baseline management routers for the ADGS

module adgsfe
"""
# Import python utilities
import os

# Import flask utilities
from flask import Blueprint, flash, current_app, render_template, request, jsonify

# Import definition of errors
from . import errors

# Import logging
from .. logger import logger as logger

# Import requests
import requests

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

bp = Blueprint("baseline_management", __name__, url_prefix="/baseline-management")

@bp.route("/", methods=["GET"])
def show_services():
    """
    Baseline management panel of the ADGS
    """
    
    return render_template("panel/baseline_management.html")

@bp.route("/query-baseline", methods=["POST"])
def query_baseline():
    """
    End-point to query the baseline of the missions
    """

    logger.info("A request to query the baseline has been requested with the following parameters")
    
    # Obtain parameters
    filters = request.json
    mission = filters["mission"]
    satellite = filters["satellite"]
    product_type = filters["product_type"]
    sensing_start = filters["sensing_start"]
    sensing_stop = filters["sensing_stop"]
    limit = filters["limit"]

    logger.info(f"Mission: {mission}")
    logger.info(f"Satellite: {satellite}")
    logger.info(f"Instrument: {mission[2:]}")
    logger.info(f"Product type: {product_type}")
    logger.info(f"Sensing start: {sensing_start}")
    logger.info(f"Sensing stop: {sensing_stop}")
    logger.info(f"Limit: {limit}")

    query_satellite = f"{mission[0:2]}{satellite}".replace("X", "_")

    logger.info(f"Query mission: {query_satellite}")
    
    adgsboa_url = f"http://{adgsboa_host}:{adgsboa_port}/query/"

    # Query auxiliary data baseline
    # First by satellite and sensing period
    query_filters = {
        "events": {
            "gauge_names": {
                "filter": "AUXILIARY_PRODUCT_BASELINE",
                "op": "=="
            },
            "start_filters": [{"date": sensing_stop, "op": "<"}],
            "stop_filters": [{"date": sensing_start, "op": ">"}],
            "value_filters": [{"name": {"filter": "satellite", "op": "=="}, "type": "text", "value": {"op": "like", "filter": query_satellite}}],
            "limit": limit
        }
    }

    logger.info(f"The baseline is going to be requested to ADGSBOA ({adgsboa_url}) with the following filters:")
    logger.info(f"{query_filters}")
    response = requests.get(url=adgsboa_url, json=query_filters)

    # Second filter by product type
    response_json = response.json()
    query_filters = {
        "events": {
            "event_uuids": {
                "filter": response_json["data"]["event_groups"]["events"],
                "op": "in"
            },
            "start_filters": [{"date": sensing_stop, "op": "<"}],
            "stop_filters": [{"date": sensing_start, "op": ">"}],
            "value_filters": [{"name": {"filter": "associated_product_types", "op": "=="}, "type": "text", "value": {"op": "like", "filter": f"%{product_type}%"}}],
            "limit": limit
        }
    }

    logger.info(f"The baseline is going to be filtered by product type sending a request to ADGSBOA ({adgsboa_url}) with the following filters:")
    logger.info(f"{query_filters}")
    response = requests.get(url=adgsboa_url, json=query_filters)


    # Query result
    query_result = {
        "status": "OK",
        "auxiliary_baseline": []
    }
    
    if response.status_code != 200:
        error_message = f"There was a failure requesting the baseline to ADGSBOA. Response code was {response.status_code}"
        logger.error(error_message)
        query_result = {
            "status": "NOK",
            "error_message": error_message
        }

        return jsonify(query_result), 500
    else:
        response_json = response.json()
        if "data" in  response_json and "events" in response_json["data"] and len(response_json["data"]["events"].keys()) > 0:
            for event_uuid in response_json["data"]["event_groups"]["events"]:
                event = response_json["data"]["events"][event_uuid]
                mission = event["indexed_values"]["mission"][0]["value"]
                satellite = event["indexed_values"]["satellite"][0]["value"]
                associated_product_levels = event["indexed_values"]["associated_product_levels"][0]["value"]
                associated_product_types = event["indexed_values"]["associated_product_types"][0]["value"]
                processing_version = event["indexed_values"]["processing_version"][0]["value"]
                auxiliary_type = event["gauge"]["system"]
                auxiliary_file = event["explicit_reference"]["name"]

                query_result["auxiliary_baseline"].append({
                    "id": event["event_uuid"],
                    "mission": mission,
                    "satellite": satellite,
                    "associated_product_levels": associated_product_levels,
                    "associated_product_types": associated_product_types,
                    "processing_version": processing_version,
                    "auxiliary_type": auxiliary_type,
                    "auxiliary_file": auxiliary_file,
                    "validity_start": event["start"],
                    "validity_stop": event["stop"]
                })
                
            # end for
            status_message = f"The were {len(response_json['data']['events'].keys())} auxiliary products retrieved"
        else:
            status_message = "The query result is empty with the provided filters"
        # end if
    # end if
    
    return jsonify(query_result)
