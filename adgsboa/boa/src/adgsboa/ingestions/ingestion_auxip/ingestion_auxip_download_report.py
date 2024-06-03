"""
Ingestion module for the download report from AUXIP of the ADGS service

Written by DEIMOS Space S.L. (dibb)

module adgsboa
"""
# Import python utilities
import json
import os
from jsonschema import validate
from dateutil import parser
import datetime
from dateutil import relativedelta

# Import query
from eboa.engine.query import Query

# Import ingestion_functions.helpers
import eboa.ingestion.functions as eboa_ingestion_functions

version = "1.0"

def process_file(file_path, engine, query, reception_time):
    """Function to process the file and insert its relevant information
    into the DDBB of the eboa
    
    :param file_path: path to the file to be processed
    :type file_path: str
    :param engine: Engine instance
    :type engine: Engine
    :param query: Query instance
    :type query: Query
    :param reception_time: time of the reception of the file by the triggering
    :type reception_time: str
    """

    # Get file name
    file_name = os.path.basename(file_path)

    # Get the general source entry (processor = None, version = None, DIM signature = PENDING_SOURCES)
    # This is for registrering the ingestion progress
    query_general_source = Query()
    session_progress = query_general_source.session
    general_source_progress = query_general_source.get_sources(names = {"filter": file_name, "op": "=="},
                                                               dim_signatures = {"filter": "PENDING_SOURCES", "op": "=="},
                                                               processors = {"filter": "", "op": "=="},
                                                               processor_version_filters = [{"filter": "", "op": "=="}])

    if len(general_source_progress) > 0:
        general_source_progress = general_source_progress[0]
    # end if

    eboa_ingestion_functions.insert_ingestion_progress(session_progress, general_source_progress, 10)

    schema_path = "/schemas/auxip_download_report.json"
    with open(schema_path) as schema_file:
        schema = json.load(schema_file)
    # end if

    eboa_ingestion_functions.insert_ingestion_progress(session_progress, general_source_progress, 15)

    with open(file_path) as input_file:
        auxip_download_report_data = json.load(input_file)
    # end with
    
    eboa_ingestion_functions.insert_ingestion_progress(session_progress, general_source_progress, 17)

    validate(instance=auxip_download_report_data, schema=schema)
    
    eboa_ingestion_functions.insert_ingestion_progress(session_progress, general_source_progress, 20)

    # Get generation date of the file from the file name
    # Validity is adjusted to this date
    generation_time = parser.parse(file_name.split("_")[3]).isoformat()
    reported_validity_start = generation_time
    validity_start = generation_time
    reported_validity_stop = generation_time
    validity_stop = generation_time

    eboa_ingestion_functions.insert_ingestion_progress(session_progress, general_source_progress, 30)

    source = {
        "name": file_name,
        "reception_time": reception_time,
        "generation_time": generation_time,
        "validity_start": validity_start,
        "validity_stop": validity_stop,
        "reported_validity_start": reported_validity_start,
        "reported_validity_stop": reported_validity_stop
    }
    
    eboa_ingestion_functions.insert_ingestion_progress(session_progress, general_source_progress, 40)

    # Get data
    # TODO: Username needs to be associated with an alias
    client = auxip_download_report_data["username"]
    client_ip = auxip_download_report_data["ip"]
    downloaded_file_name = auxip_download_report_data["filename"]
    file_uuid = auxip_download_report_data["uuid"]
    file_size = auxip_download_report_data["content_length"]
    download_stop_date = auxip_download_report_data["download_date"].replace("Z", "")
    download_elapsed_time = auxip_download_report_data["download_elapsed_time"]
    download_start_date = (parser.parse(download_stop_date) - datetime.timedelta(seconds=float(download_elapsed_time))).isoformat()
    product_type = downloaded_file_name[9:19]
    mission = downloaded_file_name[0:3]
    download_speed = float(file_size) / float(download_elapsed_time)
    
    # AUXIP download
    auxip_download_events = []
    auxip_download_events.append({
        "gauge": {
            "insertion_type": "SIMPLE_UPDATE",
            "name": "AUXIP_DOWNLOAD",
            "system": product_type
        },
        "start": download_start_date,
        "stop": download_stop_date,
        "values": [{"name": "satellite",
                    "type": "text",
                    "value": mission},
                   {"name": "mission",
                    "type": "text",
                    "value": mission},
                   {"name": "client",
                    "type": "text",
                    "value": client},
                   {"name": "client_ip",
                    "type": "text",
                    "value": client_ip},
                   {"name": "volume",
                    "type": "double",
                    "value": file_size},
                   {"name": "download_speed",
                    "type": "double",
                    "value": download_speed}]
    })

    # AUXIP download counters
    auxip_download_counters = []
    coverage_dates = []
    # Day
    start_date = parser.parse(auxip_download_report_data["download_date"][0:10]).isoformat()
    stop_date = (parser.parse(auxip_download_report_data["download_date"][0:10]) + datetime.timedelta(days=1)).isoformat()
    coverage_dates.append([start_date, stop_date, "PER_DAY"])
    # Month
    start_date = parser.parse(auxip_download_report_data["download_date"][0:7] + "-01").isoformat()
    stop_date = (parser.parse(auxip_download_report_data["download_date"][0:7] + "-01") + relativedelta.relativedelta(months=1)).isoformat()
    coverage_dates.append([start_date, stop_date, "PER_MONTH"])
    # Year
    start_date = parser.parse(auxip_download_report_data["download_date"][0:4] + "-01-01").isoformat()
    stop_date = (parser.parse(auxip_download_report_data["download_date"][0:4] + "-01-01") + relativedelta.relativedelta(years=1)).isoformat()
    coverage_dates.append([start_date, stop_date, "PER_YEAR"])

    downloaded_volume_gauges = [
        ["CUMULATIVE_DOWNLOADED_VOLUME_BY_MISSION_CLIENT", f"{mission}#{client}"],
        ["CUMULATIVE_DOWNLOADED_VOLUME_BY_CLIENT", client],
        ["CUMULATIVE_DOWNLOADED_VOLUME_BY_MISSION", mission],
        ["CUMULATIVE_DOWNLOADED_VOLUME_BY_MISSION_PRODUCT_TYPE", f"{mission}#{product_type}"],
        ["CUMULATIVE_DOWNLOADED_VOLUME_BY_PRODUCT_TYPE", product_type],
        ["CUMULATIVE_DOWNLOADED_VOLUME", "GLOBAL"],

    ]

    for gauge in downloaded_volume_gauges:
        gauge_name = gauge[0]
        gauge_system = gauge[1]

        for dates in coverage_dates:
            start_date = dates[0]
            stop_date = dates[1]
            suffix = dates[2]

            auxip_download_counters.append({
                "gauge": {
                    "insertion_type": "UPDATE_COUNTER",
                    "name": f"{gauge_name}_{suffix}_{start_date}_{stop_date}",
                    "system": gauge_system
                },
                "start": download_start_date,
                "stop": download_stop_date,
                "values": [{"name": "value",
                            "type": "double",
                            "value": file_size}]
            })
        # end for
        # Total: per mission and client
        auxip_download_counters.append({
            "gauge": {
                "insertion_type": "UPDATE_COUNTER",
                "name": gauge_name,
                "system": gauge_system
            },
            "start": download_start_date,
            "stop": download_stop_date,
            "values": [{"name": "value",
                        "type": "double",
                        "value": file_size}]
        })
    # end for

    eboa_ingestion_functions.insert_ingestion_progress(session_progress, general_source_progress, 60)

    downloaded_number_gauges = [
        ["CUMULATIVE_DOWNLOADED_NUMBER_BY_MISSION_CLIENT", f"{mission}#{client}"],
        ["CUMULATIVE_DOWNLOADED_NUMBER_BY_CLIENT", client],
        ["CUMULATIVE_DOWNLOADED_NUMBER_BY_MISSION", mission],
        ["CUMULATIVE_DOWNLOADED_NUMBER_BY_MISSION_PRODUCT_TYPE", f"{mission}#{product_type}"],
        ["CUMULATIVE_DOWNLOADED_NUMBER_BY_PRODUCT_TYPE", product_type],
        ["CUMULATIVE_DOWNLOADED_NUMBER", "GLOBAL"],

    ]

    for gauge in downloaded_number_gauges:
        gauge_name = gauge[0]
        gauge_system = gauge[1]

        for dates in coverage_dates:
            start_date = dates[0]
            stop_date = dates[1]
            suffix = dates[2]

            auxip_download_counters.append({
                "gauge": {
                    "insertion_type": "UPDATE_COUNTER",
                    "name": f"{gauge_name}_{suffix}_{start_date}_{stop_date}",
                    "system": gauge_system
                },
                "start": download_start_date,
                "stop": download_stop_date,
                "values": [{"name": "value",
                            "type": "double",
                            "value": 1}]
            })
        # end for
        # Total: per mission and client
        auxip_download_counters.append({
            "gauge": {
                "insertion_type": "UPDATE_COUNTER",
                "name": gauge_name,
                "system": gauge_system
            },
            "start": download_start_date,
            "stop": download_stop_date,
            "values": [{"name": "value",
                        "type": "double",
                        "value": 1}]
        })
    # end for

    eboa_ingestion_functions.insert_ingestion_progress(session_progress, general_source_progress, 80)
    
    # Build the xml
    operations = []
    data = {"operations": operations}

    operations.append({
        "mode": "insert",
        "dim_signature": {
            "name": "AUXIP_DOWNLOAD",
            "exec": os.path.basename(__file__),
            "version": version
        },
        "source": {
            "name": file_name,
            "reception_time": reception_time,
            "generation_time": generation_time,
            "validity_start": download_start_date,
            "validity_stop": download_stop_date,
            "reported_validity_start": reported_validity_start,
            "reported_validity_stop": reported_validity_stop,
        },
        "events": auxip_download_events + auxip_download_counters
    })

    return data
