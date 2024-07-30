"""
Ingestion module for the completeness expectation report for the AUXIP of the ADGS service

Written by DEIMOS Space S.L. (dibb)

module adgsboa
"""
# Import python utilities
import os
from dateutil import parser
import datetime

# Import ingestion_functions.helpers
import eboa.ingestion.functions as eboa_ingestion_functions

# Import query
from eboa.engine.query import Query

# Import xml parser
from lxml import etree

# Import ADGSBOA functions helpers
import adgsboa.ingestions.functions as adgsboa_ingestion_functions

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
    
    # Parse file
    parsed_xml = etree.parse(file_path)
    xpath_xml = etree.XPathEvaluator(parsed_xml)

    eboa_ingestion_functions.insert_ingestion_progress(session_progress, general_source_progress, 15)

    # Completeness is created for the next day and week to the reception_time
    next_day_start = parser.parse(reception_time[0:10]) + datetime.timedelta(days=1)
    next_day_stop = next_day_start + datetime.timedelta(days=1)
    next_week_start = next_day_start
    next_week_stop = next_day_start + datetime.timedelta(days=7)

    # Get the Copernicus constellations configuration
    copernicus_constellations_xpath = adgsboa_ingestion_functions.get_copernicus_constellations_conf()

    completeness_events = []

    # Create completeness for daily operations
    daily_completeness_rules = xpath_xml("/completeness_rules/mission/rule[frequency='daily']")
    for daily_completeness_rule in daily_completeness_rules:
        auxiliary_type = daily_completeness_rule.xpath("type")[0].text
        number_of_files = daily_completeness_rule.xpath("number_of_files")[0].text
        mission = daily_completeness_rule.xpath("../@name")[0]
        satellites = [mission]
        if len(daily_completeness_rule.xpath("@per_satellite")) > 0 and bool(daily_completeness_rule.xpath("@per_satellite")[0]):
            satellites = copernicus_constellations_xpath(f"/constellations/mission[@name='{mission}']/satellites/satellite/@name")
        # end if
        for satellite in satellites:

            completeness_events.append({
                "gauge": {
                    "insertion_type": "SET_COUNTER",
                    "name": f"EXPECTED_AUXILIARY_FILES_{auxiliary_type}",
                    "system": f"{satellite}"
                },
                "start": next_day_start.isoformat(),
                "stop": next_day_stop.isoformat(),
                "values": [{"name": "value",
                            "type": "double",
                            "value": number_of_files}]
            })
        # end for
    # end for
    
    eboa_ingestion_functions.insert_ingestion_progress(session_progress, general_source_progress, 40)

    # If next day is monday, create completeness for weekly operations
    if next_day_start.weekday() == 0:
        weekly_completeness_rules = xpath_xml("/completeness_rules/mission/rule[frequency='weekly']")
        for weekly_completeness_rule in weekly_completeness_rules:
            auxiliary_type = weekly_completeness_rule.xpath("type")[0].text
            number_of_files = weekly_completeness_rule.xpath("number_of_files")[0].text
            mission = weekly_completeness_rule.xpath("../@name")[0]
            satellites = [mission]
            if len(weekly_completeness_rule.xpath("@per_satellite")) > 0 and bool(weekly_completeness_rule.xpath("@per_satellite")[0]):
                satellites = copernicus_constellations_xpath(f"/constellations/mission[@name='{mission}']/satellites/satellite/@name")
            # end if
            for satellite in satellites:

                completeness_events.append({
                    "gauge": {
                        "insertion_type": "SET_COUNTER",
                        "name": f"EXPECTED_AUXILIARY_FILES_{auxiliary_type}",
                        "system": f"{satellite}"
                    },
                    "start": next_week_start.isoformat(),
                    "stop": next_week_stop.isoformat(),
                    "values": [{"name": "value",
                                "type": "double",
                                "value": number_of_files}]
                })
            # end for
        # end for
    # end if
    
    eboa_ingestion_functions.insert_ingestion_progress(session_progress, general_source_progress, 70)

    source = {
        "name": file_name,
        "reception_time": reception_time,
        "generation_time": reception_time,
        "validity_start": next_week_start.isoformat(),
        "validity_stop": next_week_stop.isoformat(),
        "reported_validity_start": next_week_start.isoformat(),
        "reported_validity_stop": next_week_stop.isoformat()
    }

    eboa_ingestion_functions.insert_ingestion_progress(session_progress, general_source_progress, 80)
    
    # Build the xml
    operations = []
    data = {"operations": operations}

    operations.append({
        "mode": "insert",
        "dim_signature": {
            "name": "EXPECTED_AUXILIARY_FILES",
            "exec": os.path.basename(__file__),
            "version": version
        },
        "source": {
            "name": file_name,
            "reception_time": reception_time,
            "generation_time": reception_time,
            "validity_start": next_week_start.isoformat(),
            "validity_stop": next_week_stop.isoformat(),
            "reported_validity_start": next_week_start.isoformat(),
            "reported_validity_stop": next_week_stop.isoformat()
        },
        "events": completeness_events
    })

    return data
