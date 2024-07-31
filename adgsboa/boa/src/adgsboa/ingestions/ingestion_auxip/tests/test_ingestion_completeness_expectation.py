"""
Automated tests for the ingestion of the completeness expectation report for the AUXIP of the ADGS service

Written by DEIMOS Space S.L. (dibb)

module adgsboa
"""
# Import python utilities
import os
import sys
import unittest
import datetime
import re

# Import engine of the DDBB
import eboa.engine.engine as eboa_engine
from eboa.engine.engine import Engine
from eboa.engine.query import Query

# Import ingestion
import eboa.ingestion.eboa_ingestion as ingestion

# Import ADGSBOA functions helpers
import adgsboa.ingestions.functions as adgsboa_ingestion_functions

class TestCompletenessExpectationReport(unittest.TestCase):
    def setUp(self):
        # Create the engine to manage the data
        self.engine_eboa = Engine()
        self.query_eboa = Query()

        # Clear all tables before executing the test
        self.query_eboa.clear_db()

    def tearDown(self):
        # Close connections to the DDBB
        self.engine_eboa.close_session()
        self.query_eboa.close_session()
        
    def test_insert_completeness_expectation_report_one_mission_one_rule(self):
        """
        This test verifies the ingestion of the completeness expectation report for the AUXIP with one mission and one rule
        """
        
        filename = "adgs_completeness_timeliness_one_mission_one_rule.xml"
        file_path = os.path.dirname(os.path.abspath(__file__)) + "/inputs/" + filename

        exit_status = ingestion.command_process_file("adgsboa.ingestions.ingestion_auxip.ingestion_completeness_expectation_report", file_path, "2024-07-28T12:00:00")

        assert len([item for item in exit_status if item["status"] != eboa_engine.exit_codes["OK"]["status"]]) == 0

        # Check number of sources inserted
        sources = self.query_eboa.get_sources()

        assert len(sources) == 1

        # Check sources inserted
        sources = self.query_eboa.get_sources(validity_start_filters = [{"date": "2024-07-29T00:00:00", "op": "=="}],
                                              validity_stop_filters = [{"date": "2024-08-05T00:00:00", "op": "=="}],
                                              reported_validity_start_filters = [{"date": "2024-07-29T00:00:00", "op": "=="}],
                                              reported_validity_stop_filters = [{"date": "2024-08-05T00:00:00", "op": "=="}],
                                              processors = {"filter": "ingestion_completeness_expectation_report.py", "op": "=="},
                                              dim_signatures = {"filter": "PENDING_AUXILIARY_FILES", "op": "=="},
                                              names = {"filter": "adgs_completeness_timeliness_one_mission_one_rule.xml", "op": "=="},
                                              ingestion_completeness = True)

        assert len(sources) == 1
        # Check number of events generated
        events = self.query_eboa.get_events()

        assert len(events) == 1

        # Check PENDING_AUXILIARY_FILES events
        events = self.query_eboa.get_events(gauge_names = {"filter": "PENDING_AUXILIARY_FILES%", "op": "like"})

        assert len(events) == 1

        events = self.query_eboa.get_events(gauge_names = {"filter": "PENDING_AUXILIARY_FILES_AUX_WND", "op": "=="},
                                            gauge_systems = {"filter": "S1", "op": "=="},
                                                start_filters = [{"date": "2024-07-29T00:00:00", "op": "=="}],
                                                stop_filters = [{"date": "2024-07-30T00:00:00", "op": "=="}])

        assert len(events) == 1
        
        assert events[0].get_structured_values() == [
            {"name": "value",
             "type": "double",
             "value": "182.0"}
        ]
        
    def test_insert_completeness_expectation_report_complete(self):
        """
        This test verifies the ingestion of the completeness expectation report for the AUXIP complete
        """
        
        filename = "adgs_completeness_timeliness.xml"
        file_path = "/resources_path/" + filename

        exit_status = ingestion.command_process_file("adgsboa.ingestions.ingestion_auxip.ingestion_completeness_expectation_report", file_path, "2024-07-28T12:00:00")

        assert len([item for item in exit_status if item["status"] != eboa_engine.exit_codes["OK"]["status"]]) == 0

        # Check number of sources inserted
        sources = self.query_eboa.get_sources()

        assert len(sources) == 1

        # Check sources inserted
        sources = self.query_eboa.get_sources(validity_start_filters = [{"date": "2024-07-29T00:00:00", "op": "=="}],
                                              validity_stop_filters = [{"date": "2024-08-05T00:00:00", "op": "=="}],
                                              reported_validity_start_filters = [{"date": "2024-07-29T00:00:00", "op": "=="}],
                                              reported_validity_stop_filters = [{"date": "2024-08-05T00:00:00", "op": "=="}],
                                              processors = {"filter": "ingestion_completeness_expectation_report.py", "op": "=="},
                                              dim_signatures = {"filter": "PENDING_AUXILIARY_FILES", "op": "=="},
                                              names = {"filter": "adgs_completeness_timeliness.xml", "op": "=="},
                                              ingestion_completeness = True)

        assert len(sources) == 1
        # Check number of events generated
        events = self.query_eboa.get_events()

        assert len(events) == 63

        # Check PENDING_AUXILIARY_FILES events
        events = self.query_eboa.get_events(gauge_names = {"filter": "PENDING_AUXILIARY_FILES%", "op": "like"})

        assert len(events) == 63

        # Get the Copernicus constellations configuration
        completeness_timeliness_xpath = adgsboa_ingestion_functions.get_completeness_timeliness_conf()

        # Get the Copernicus constellations configuration
        copernicus_constellations_xpath = adgsboa_ingestion_functions.get_copernicus_constellations_conf()

        # Check events related to completeness
        completeness_rules = completeness_timeliness_xpath("/completeness_rules/mission/rule")
        completeness_check_events = []
        for completeness_rule in completeness_rules:
            auxiliary_type = completeness_rule.xpath("type")[0].text
            number_of_files = completeness_rule.xpath("number_of_files")[0].text
            mission = completeness_rule.xpath("../@name")[0]
            frequency = completeness_rule.xpath("frequency")[0].text
            satellites = [mission]
            if len(completeness_rule.xpath("@per_satellite")) > 0 and bool(completeness_rule.xpath("@per_satellite")[0]):
                satellites = copernicus_constellations_xpath(f"/constellations/mission[@name='{mission}']/satellites/satellite/@name")
            # end if

            for satellite in satellites:
                event_stop = "2024-07-30T00:00:00"
                if frequency == "weekly":
                    event_stop = "2024-08-05T00:00:00"
                # end if
                events = self.query_eboa.get_events(gauge_names = {"filter": f"PENDING_AUXILIARY_FILES_{auxiliary_type}", "op": "=="},
                                                    gauge_systems = {"filter": str(satellite), "op": "=="},
                                                    start_filters = [{"date": "2024-07-29T00:00:00", "op": "=="}],
                                                    stop_filters = [{"date": event_stop, "op": "=="}],
                                                    value_filters = [{"name": {"filter": "value", "op": "=="}, "type": "double", "value": {"op": "==", "filter": number_of_files}}])

                assert len(events) == 1

                completeness_check_events.append(events[0])
                
            # end for
        # end for

        assert len(completeness_check_events) == 63
