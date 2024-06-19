"""
Ingestion module for the list of products in CSV format from the baseline configuration web page

Written by DEIMOS Space S.L. (dibb)

module adgsboa
"""
# Import python utilities
import os
from dateutil import parser
import datetime
from dateutil import relativedelta
import csv

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

    # Set generation date as now
    generation_time = datetime.datetime.now().isoformat()
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
    
    # Build the xml
    operations = []
    data = {"operations": operations}

    # Get data
    auxiliary_products_events = []
    with open(file_path, newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            auxiliary_data_validity_start = row["Application From"]
            auxiliary_data_validity_stop = row["Application To"]
            associated_product_level = row["Product Level"]
            associated_product_types = row["Product Type"]
            auxiliary_product_type = row["Auxiliary Type"]
            auxiliary_product_name = row["Auxiliary File"]
            processing_version = row["IPF Version"]
            satellite = auxiliary_product_name[0:3]
            mission = auxiliary_product_name[0:2] + "_"
            auxiliary_products_events.append({
                "explicit_reference": auxiliary_product_name,
                "gauge": {
                    "insertion_type": "SIMPLE_UPDATE",
                    "name": "AUXILIARY_PRODUCT",
                    "system": auxiliary_product_type
                },
                "start": auxiliary_data_validity_start,
                "stop": auxiliary_data_validity_stop,
                "values": [{"name": "satellite",
                            "type": "text",
                            "value": satellite},
                           {"name": "mission",
                            "type": "text",
                            "value": mission},
                           {"name": "associated_product_level",
                            "type": "text",
                            "value": associated_product_level},
                           {"name": "associated_product_types",
                            "type": "text",
                            "value": associated_product_types},
                           {"name": "processing_version",
                            "type": "text",
                            "value": processing_version}
                ]
            })

            # Build operations for the baseline management associated to each auxiliiary file
            auxiliary_generation_time = auxiliary_product_name.split("_G")[1][0:15]
            operations.append({
                "mode": "insert",
                "dim_signature": {
                    "name": "AUXILIARY_PRODUCTS_BASELINE",
                    "exec": os.path.basename(__file__) + "_" + auxiliary_product_name,
                    "version": version
                },
                "source": {
                    "name": file_name,
                    "reception_time": reception_time,
                    "generation_time": auxiliary_generation_time,
                    "validity_start": auxiliary_data_validity_start,
                    "validity_stop": auxiliary_data_validity_stop,
                    "reported_validity_start": auxiliary_data_validity_start,
                    "reported_validity_stop": auxiliary_data_validity_stop
                },
                "events": [{
                    "explicit_reference": auxiliary_product_name,
                    "gauge": {
                        "insertion_type": "INSERT_and_ERASE_per_EVENT",
                        "name": "AUXILIARY_PRODUCT_BASELINE",
                        "system": auxiliary_product_type
                    },
                    "start": auxiliary_data_validity_start,
                    "stop": auxiliary_data_validity_stop,
                    "values": [{"name": "satellite",
                                "type": "text",
                                "value": satellite},
                               {"name": "mission",
                                "type": "text",
                                "value": mission},
                               {"name": "associated_product_level",
                                "type": "text",
                                "value": associated_product_level},
                               {"name": "associated_product_types",
                                "type": "text",
                                "value": associated_product_types},
                               {"name": "processing_version",
                                "type": "text",
                                "value": processing_version}
                    ]
                }]
            })

        # end for
    # end with

    eboa_ingestion_functions.insert_ingestion_progress(session_progress, general_source_progress, 84)

    if len(auxiliary_products_events) > 0:
        event_starts = [event["start"] for event in auxiliary_products_events]
        event_starts.sort()
        validity_start = event_starts[0]
        event_stops = [event["stop"] for event in auxiliary_products_events]
        event_stops.sort()
        validity_stop = event_stops[-1]
    # end if
    
    operations.append({
        "mode": "insert",
        "dim_signature": {
            "name": "AUXILIARY_PRODUCTS",
            "exec": os.path.basename(__file__),
            "version": version
        },
        "source": {
            "name": file_name,
            "reception_time": reception_time,
            "generation_time": generation_time,
            "validity_start": validity_start,
            "validity_stop": validity_stop,
            "reported_validity_start": reported_validity_start,
            "reported_validity_stop": reported_validity_stop
        },
        "events": auxiliary_products_events
    })

    return data
