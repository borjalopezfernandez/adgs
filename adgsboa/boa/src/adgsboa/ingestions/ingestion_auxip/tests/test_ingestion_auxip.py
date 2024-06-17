"""
Automated tests for the ingestion of the download report from AUXIP of the ADGS service

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

class TestAuxipDownloadReport(unittest.TestCase):
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
        
    def test_insert_empty_auxip_download_report(self):
        """
        This test verifies that the ingestion is able to manage empty files
        """
        
        filename = "auxip_download_report_20240524T104634.466_888.json"
        file_path = os.path.dirname(os.path.abspath(__file__)) + "/inputs/" + filename

        exit_status = ingestion.command_process_file("adgsboa.ingestions.ingestion_auxip.ingestion_auxip_download_report", file_path, "2018-01-01T00:00:00")
        
        assert len([item for item in exit_status if item["status"] == eboa_engine.exit_codes["PROCESSING_ENDED_UNEXPECTEDLY"]["status"]]) == 1

        filename = "auxip_download_report_20240524T104634.466_777.json"
        file_path = os.path.dirname(os.path.abspath(__file__)) + "/inputs/" + filename

        exit_status = ingestion.command_process_file("adgsboa.ingestions.ingestion_auxip.ingestion_auxip_download_report", file_path, "2018-01-01T00:00:00")
        
        assert len([item for item in exit_status if item["status"] == eboa_engine.exit_codes["PROCESSING_ENDED_UNEXPECTEDLY"]["status"]]) == 1

        filename = "auxip_download_report_20240524T104634.466_666.json"
        file_path = os.path.dirname(os.path.abspath(__file__)) + "/inputs/" + filename

        exit_status = ingestion.command_process_file("adgsboa.ingestions.ingestion_auxip.ingestion_auxip_download_report", file_path, "2018-01-01T00:00:00")
        
        assert len([item for item in exit_status if item["status"] == eboa_engine.exit_codes["PROCESSING_ENDED_UNEXPECTEDLY"]["status"]]) == 1
        
    def test_insert_auxip_download_report(self):
        """
        This test verifies the ingestion of the download report from the AUXIP 
        """
        
        filename = "auxip_download_report_20240524T104634.466_999.json"
        file_path = os.path.dirname(os.path.abspath(__file__)) + "/inputs/" + filename

        exit_status = ingestion.command_process_file("adgsboa.ingestions.ingestion_auxip.ingestion_auxip_download_report", file_path, "2018-01-01T00:00:00")

        assert len([item for item in exit_status if item["status"] != eboa_engine.exit_codes["OK"]["status"]]) == 0

        # Check number of sources inserted
        sources = self.query_eboa.get_sources()

        assert len(sources) == 1

        # Check sources inserted
        sources = self.query_eboa.get_sources(validity_start_filters = [{"date": "2024-05-24T08:46:34.438128", "op": "=="}],
                                              validity_stop_filters = [{"date": "2024-05-24T08:46:34.454000", "op": "=="}],
                                              reported_validity_start_filters = [{"date": "2024-05-24T10:46:34.466000", "op": "=="}],
                                              reported_validity_stop_filters = [{"date": "2024-05-24T10:46:34.466000", "op": "=="}],
                                              processors = {"filter": "ingestion_auxip_download_report.py", "op": "=="},
                                              dim_signatures = {"filter": "AUXIP_DOWNLOAD", "op": "=="},
                                              names = {"filter": "auxip_download_report_20240524T104634.466_999.json", "op": "=="},
                                              ingestion_completeness = True)

        assert len(sources) == 1


        # Check number of events generated
        events = self.query_eboa.get_events()

        assert len(events) == 59

        # Check AUXIP_DOWNLOAD events
        events = self.query_eboa.get_events(gauge_names = {"filter": "AUXIP_DOWNLOAD", "op": "=="})

        assert len(events) == 1

        events = self.query_eboa.get_events(gauge_names = {"filter": "AUXIP_DOWNLOAD", "op": "=="},
                                            gauge_systems = {"filter": "AUX_UT1UTC", "op": "=="},
                                                start_filters = [{"date": "2024-05-24T08:46:34.438128", "op": "=="}],
                                                stop_filters = [{"date": "2024-05-24T08:46:34.454000", "op": "=="}])

        assert len(events) == 1
        
        assert events[0].get_structured_values() == [
            {"name": "satellite",
             "type": "text",
             "value": "S2_"},
            {"name": "mission",
             "type": "text",
             "value": "S2_"},
            {"name": "client",
             "type": "text",
             "value": "test"},
            {"name": "client_ip",
             "type": "text",
             "value": "127.0.0.1"},
            {"name": "volume",
             "type": "double",
             "value": "1048576000.0"},
            {"name": "download_speed",
             "type": "double",
             "value": "66066214403.6969"}
        ]

        # Check volume counter events
        gauges = [
            ["CUMULATIVE_DOWNLOADED_VOLUME_BY_MISSION_CLIENT_PER_DAY_2024-05-24T00:00:00_2024-05-25T00:00:00", "S2_#test"],
            ["CUMULATIVE_DOWNLOADED_VOLUME_BY_MISSION_CLIENT_PER_MONTH_2024-05-01T00:00:00_2024-06-01T00:00:00", "S2_#test"],
            ["CUMULATIVE_DOWNLOADED_VOLUME_BY_MISSION_CLIENT_PER_YEAR_2024-01-01T00:00:00_2025-01-01T00:00:00", "S2_#test"],
            ["CUMULATIVE_DOWNLOADED_VOLUME_BY_MISSION_CLIENT", "S2_#test"],
            ["CUMULATIVE_DOWNLOADED_VOLUME_BY_CLIENT_PER_DAY_2024-05-24T00:00:00_2024-05-25T00:00:00", "test"],
            ["CUMULATIVE_DOWNLOADED_VOLUME_BY_CLIENT_PER_MONTH_2024-05-01T00:00:00_2024-06-01T00:00:00", "test"],
            ["CUMULATIVE_DOWNLOADED_VOLUME_BY_CLIENT_PER_YEAR_2024-01-01T00:00:00_2025-01-01T00:00:00", "test"],
            ["CUMULATIVE_DOWNLOADED_VOLUME_BY_CLIENT", "test"],
            ["CUMULATIVE_DOWNLOADED_VOLUME_BY_MISSION_PER_DAY_2024-05-24T00:00:00_2024-05-25T00:00:00", "S2_"],
            ["CUMULATIVE_DOWNLOADED_VOLUME_BY_MISSION_PER_MONTH_2024-05-01T00:00:00_2024-06-01T00:00:00", "S2_"],
            ["CUMULATIVE_DOWNLOADED_VOLUME_BY_MISSION_PER_YEAR_2024-01-01T00:00:00_2025-01-01T00:00:00", "S2_"],
            ["CUMULATIVE_DOWNLOADED_VOLUME_BY_MISSION", "S2_"],
            ["CUMULATIVE_DOWNLOADED_VOLUME_BY_MISSION_PRODUCT_TYPE_PER_DAY_2024-05-24T00:00:00_2024-05-25T00:00:00", "S2_#AUX_UT1UTC"],
            ["CUMULATIVE_DOWNLOADED_VOLUME_BY_MISSION_PRODUCT_TYPE_PER_MONTH_2024-05-01T00:00:00_2024-06-01T00:00:00", "S2_#AUX_UT1UTC"],
            ["CUMULATIVE_DOWNLOADED_VOLUME_BY_MISSION_PRODUCT_TYPE_PER_YEAR_2024-01-01T00:00:00_2025-01-01T00:00:00", "S2_#AUX_UT1UTC"],
            ["CUMULATIVE_DOWNLOADED_VOLUME_BY_MISSION_PRODUCT_TYPE", "S2_#AUX_UT1UTC"],
            ["CUMULATIVE_DOWNLOADED_VOLUME_BY_PRODUCT_TYPE_PER_DAY_2024-05-24T00:00:00_2024-05-25T00:00:00", "AUX_UT1UTC"],
            ["CUMULATIVE_DOWNLOADED_VOLUME_BY_PRODUCT_TYPE_PER_MONTH_2024-05-01T00:00:00_2024-06-01T00:00:00", "AUX_UT1UTC"],
            ["CUMULATIVE_DOWNLOADED_VOLUME_BY_PRODUCT_TYPE_PER_YEAR_2024-01-01T00:00:00_2025-01-01T00:00:00", "AUX_UT1UTC"],
            ["CUMULATIVE_DOWNLOADED_VOLUME_BY_PRODUCT_TYPE", "AUX_UT1UTC"],
            ["CUMULATIVE_DOWNLOADED_VOLUME_PER_DAY_2024-05-24T00:00:00_2024-05-25T00:00:00", "GLOBAL"],
            ["CUMULATIVE_DOWNLOADED_VOLUME_PER_MONTH_2024-05-01T00:00:00_2024-06-01T00:00:00", "GLOBAL"],
            ["CUMULATIVE_DOWNLOADED_VOLUME_PER_YEAR_2024-01-01T00:00:00_2025-01-01T00:00:00", "GLOBAL"],
            ["CUMULATIVE_DOWNLOADED_VOLUME", "GLOBAL"],
            ["CUMULATIVE_DOWNLOADED_VOLUME_BY_MISSION_PRODUCT_TYPE_CLIENT", "S2_#AUX_UT1UTC#test"]
        ]

        assert len(gauges) == 25

        registered_events = {}
        
        for gauge in gauges:
            gauge_name = gauge[0]
            gauge_system = gauge[1]

            events = self.query_eboa.get_events(gauge_names = {"filter": gauge_name, "op": "=="},
                                                gauge_systems = {"filter": gauge_system, "op": "=="},
                                                start_filters = [{"date": "2024-05-24T08:46:34.438128", "op": "=="}],
                                                stop_filters = [{"date": "2024-05-24T08:46:34.454000", "op": "=="}])

            assert len(events) == 1
        
            assert events[0].get_structured_values() == [
                {"name": "value",
                 "type": "double",
                 "value": "1048576000.0"}
            ]

            assert events[0].event_uuid not in registered_events

            registered_events[events[0].event_uuid] = None
        # end for

        # Check number counter events
        gauges = [
            ["CUMULATIVE_DOWNLOADED_NUMBER_BY_MISSION_CLIENT_PER_DAY_2024-05-24T00:00:00_2024-05-25T00:00:00", "S2_#test"],
            ["CUMULATIVE_DOWNLOADED_NUMBER_BY_MISSION_CLIENT_PER_MONTH_2024-05-01T00:00:00_2024-06-01T00:00:00", "S2_#test"],
            ["CUMULATIVE_DOWNLOADED_NUMBER_BY_MISSION_CLIENT_PER_YEAR_2024-01-01T00:00:00_2025-01-01T00:00:00", "S2_#test"],
            ["CUMULATIVE_DOWNLOADED_NUMBER_BY_MISSION_CLIENT", "S2_#test"],
            ["CUMULATIVE_DOWNLOADED_NUMBER_BY_CLIENT_PER_DAY_2024-05-24T00:00:00_2024-05-25T00:00:00", "test"],
            ["CUMULATIVE_DOWNLOADED_NUMBER_BY_CLIENT_PER_MONTH_2024-05-01T00:00:00_2024-06-01T00:00:00", "test"],
            ["CUMULATIVE_DOWNLOADED_NUMBER_BY_CLIENT_PER_YEAR_2024-01-01T00:00:00_2025-01-01T00:00:00", "test"],
            ["CUMULATIVE_DOWNLOADED_NUMBER_BY_CLIENT", "test"],
            ["CUMULATIVE_DOWNLOADED_NUMBER_BY_MISSION_PER_DAY_2024-05-24T00:00:00_2024-05-25T00:00:00", "S2_"],
            ["CUMULATIVE_DOWNLOADED_NUMBER_BY_MISSION_PER_MONTH_2024-05-01T00:00:00_2024-06-01T00:00:00", "S2_"],
            ["CUMULATIVE_DOWNLOADED_NUMBER_BY_MISSION_PER_YEAR_2024-01-01T00:00:00_2025-01-01T00:00:00", "S2_"],
            ["CUMULATIVE_DOWNLOADED_NUMBER_BY_MISSION", "S2_"],
            ["CUMULATIVE_DOWNLOADED_NUMBER_BY_MISSION_PRODUCT_TYPE_PER_DAY_2024-05-24T00:00:00_2024-05-25T00:00:00", "S2_#AUX_UT1UTC"],
            ["CUMULATIVE_DOWNLOADED_NUMBER_BY_MISSION_PRODUCT_TYPE_PER_MONTH_2024-05-01T00:00:00_2024-06-01T00:00:00", "S2_#AUX_UT1UTC"],
            ["CUMULATIVE_DOWNLOADED_NUMBER_BY_MISSION_PRODUCT_TYPE_PER_YEAR_2024-01-01T00:00:00_2025-01-01T00:00:00", "S2_#AUX_UT1UTC"],
            ["CUMULATIVE_DOWNLOADED_NUMBER_BY_MISSION_PRODUCT_TYPE", "S2_#AUX_UT1UTC"],
            ["CUMULATIVE_DOWNLOADED_NUMBER_BY_PRODUCT_TYPE_PER_DAY_2024-05-24T00:00:00_2024-05-25T00:00:00", "AUX_UT1UTC"],
            ["CUMULATIVE_DOWNLOADED_NUMBER_BY_PRODUCT_TYPE_PER_MONTH_2024-05-01T00:00:00_2024-06-01T00:00:00", "AUX_UT1UTC"],
            ["CUMULATIVE_DOWNLOADED_NUMBER_BY_PRODUCT_TYPE_PER_YEAR_2024-01-01T00:00:00_2025-01-01T00:00:00", "AUX_UT1UTC"],
            ["CUMULATIVE_DOWNLOADED_NUMBER_BY_PRODUCT_TYPE", "AUX_UT1UTC"],
            ["CUMULATIVE_DOWNLOADED_NUMBER_PER_DAY_2024-05-24T00:00:00_2024-05-25T00:00:00", "GLOBAL"],
            ["CUMULATIVE_DOWNLOADED_NUMBER_PER_MONTH_2024-05-01T00:00:00_2024-06-01T00:00:00", "GLOBAL"],
            ["CUMULATIVE_DOWNLOADED_NUMBER_PER_YEAR_2024-01-01T00:00:00_2025-01-01T00:00:00", "GLOBAL"],
            ["CUMULATIVE_DOWNLOADED_NUMBER", "GLOBAL"],
            ["CUMULATIVE_DOWNLOADED_NUMBER_BY_MISSION_PRODUCT_TYPE_CLIENT", "S2_#AUX_UT1UTC#test"]
        ]

        assert len(gauges) == 25

        registered_events = {}
        
        for gauge in gauges:
            gauge_name = gauge[0]
            gauge_system = gauge[1]

            events = self.query_eboa.get_events(gauge_names = {"filter": gauge_name, "op": "=="},
                                                gauge_systems = {"filter": gauge_system, "op": "=="},
                                                start_filters = [{"date": "2024-05-24T08:46:34.438128", "op": "=="}],
                                                stop_filters = [{"date": "2024-05-24T08:46:34.454000", "op": "=="}])

            assert len(events) == 1
        
            assert events[0].get_structured_values() == [
                {"name": "value",
                 "type": "double",
                 "value": "1.0"}
            ]

            assert events[0].event_uuid not in registered_events

            registered_events[events[0].event_uuid] = None
        # end for

        events = self.query_eboa.get_events(gauge_names = {"filter": "CUMULATIVE_DOWNLOAD_TIME", "op": "=="},
                                            gauge_systems = {"filter": "GLOBAL", "op": "=="},
                                            start_filters = [{"date": "2024-05-24T08:46:34.438128", "op": "=="}],
                                            stop_filters = [{"date": "2024-05-24T08:46:34.454000", "op": "=="}])

        assert len(events) == 1

        assert events[0].get_structured_values() == [
            {"name": "value",
             "type": "double",
             "value": "0.015871592"}
        ]

        events = self.query_eboa.get_events(gauge_names = {"filter": "CUMULATIVE_DOWNLOAD_SPEED", "op": "=="},
                                            gauge_systems = {"filter": "GLOBAL", "op": "=="},
                                            start_filters = [{"date": "2024-05-24T08:46:34.438128", "op": "=="}],
                                            stop_filters = [{"date": "2024-05-24T08:46:34.454000", "op": "=="}])

        assert len(events) == 1

        assert events[0].get_structured_values() == [
            {"name": "value",
             "type": "double",
             "value": "66066214403.6969"}
        ]
        
    def test_insert_two_auxip_download_reports(self):
        """
        This test verifies the ingestion of the download report from the AUXIP 
        """
        
        filename = "auxip_download_report_20240524T104634.466_999.json"
        file_path = os.path.dirname(os.path.abspath(__file__)) + "/inputs/" + filename

        exit_status = ingestion.command_process_file("adgsboa.ingestions.ingestion_auxip.ingestion_auxip_download_report", file_path, "2018-01-01T00:00:00")

        assert len([item for item in exit_status if item["status"] != eboa_engine.exit_codes["OK"]["status"]]) == 0
        
        filename = "auxip_download_report_20240525T104634.466_999.json"
        file_path = os.path.dirname(os.path.abspath(__file__)) + "/inputs/" + filename

        exit_status = ingestion.command_process_file("adgsboa.ingestions.ingestion_auxip.ingestion_auxip_download_report", file_path, "2018-01-01T00:00:00")

        assert len([item for item in exit_status if item["status"] != eboa_engine.exit_codes["OK"]["status"]]) == 0

        # Check number of sources inserted
        sources = self.query_eboa.get_sources()

        assert len(sources) == 2

        # Check sources inserted
        sources = self.query_eboa.get_sources(validity_start_filters = [{"date": "2024-05-24T08:46:34.438128", "op": "=="}],
                                              validity_stop_filters = [{"date": "2024-05-24T08:46:34.454000", "op": "=="}],
                                              reported_validity_start_filters = [{"date": "2024-05-24T10:46:34.466000", "op": "=="}],
                                              reported_validity_stop_filters = [{"date": "2024-05-24T10:46:34.466000", "op": "=="}],
                                              processors = {"filter": "ingestion_auxip_download_report.py", "op": "=="},
                                              dim_signatures = {"filter": "AUXIP_DOWNLOAD", "op": "=="},
                                              names = {"filter": "auxip_download_report_20240524T104634.466_999.json", "op": "=="},
                                              ingestion_completeness = True)

        assert len(sources) == 1

        # Check sources inserted
        sources = self.query_eboa.get_sources(validity_start_filters = [{"date": "2024-05-25T08:46:34.438128", "op": "=="}],
                                              validity_stop_filters = [{"date": "2024-05-25T08:46:34.454000", "op": "=="}],
                                              reported_validity_start_filters = [{"date": "2024-05-25T10:46:34.466000", "op": "=="}],
                                              reported_validity_stop_filters = [{"date": "2024-05-25T10:46:34.466000", "op": "=="}],
                                              processors = {"filter": "ingestion_auxip_download_report.py", "op": "=="},
                                              dim_signatures = {"filter": "AUXIP_DOWNLOAD", "op": "=="},
                                              names = {"filter": "auxip_download_report_20240525T104634.466_999.json", "op": "=="},
                                              ingestion_completeness = True)

        assert len(sources) == 1


        # Check number of events generated
        events = self.query_eboa.get_events()

        assert len(events) == 74

        # Check AUXIP_DOWNLOAD events
        events = self.query_eboa.get_events(gauge_names = {"filter": "AUXIP_DOWNLOAD", "op": "=="})

        assert len(events) == 2

        events = self.query_eboa.get_events(gauge_names = {"filter": "AUXIP_DOWNLOAD", "op": "=="},
                                            gauge_systems = {"filter": "AUX_UT1UTC", "op": "=="},
                                                start_filters = [{"date": "2024-05-24T08:46:34.438128", "op": "=="}],
                                                stop_filters = [{"date": "2024-05-24T08:46:34.454000", "op": "=="}])

        assert len(events) == 1

        events = self.query_eboa.get_events(gauge_names = {"filter": "AUXIP_DOWNLOAD", "op": "=="},
                                            gauge_systems = {"filter": "AUX_UT1UTC", "op": "=="},
                                                start_filters = [{"date": "2024-05-25T08:46:34.438128", "op": "=="}],
                                                stop_filters = [{"date": "2024-05-25T08:46:34.454000", "op": "=="}])

        assert len(events) == 1

        # Check volume counter events
        # Check counters for day X
        gauges = [
            ["CUMULATIVE_DOWNLOADED_VOLUME_BY_MISSION_CLIENT_PER_DAY_2024-05-24T00:00:00_2024-05-25T00:00:00", "S2_#test"],
            ["CUMULATIVE_DOWNLOADED_VOLUME_BY_CLIENT_PER_DAY_2024-05-24T00:00:00_2024-05-25T00:00:00", "test"],
            ["CUMULATIVE_DOWNLOADED_VOLUME_BY_MISSION_PER_DAY_2024-05-24T00:00:00_2024-05-25T00:00:00", "S2_"],
            ["CUMULATIVE_DOWNLOADED_VOLUME_BY_MISSION_PRODUCT_TYPE_PER_DAY_2024-05-24T00:00:00_2024-05-25T00:00:00", "S2_#AUX_UT1UTC"],
            ["CUMULATIVE_DOWNLOADED_VOLUME_BY_PRODUCT_TYPE_PER_DAY_2024-05-24T00:00:00_2024-05-25T00:00:00", "AUX_UT1UTC"],
            ["CUMULATIVE_DOWNLOADED_VOLUME_PER_DAY_2024-05-24T00:00:00_2024-05-25T00:00:00", "GLOBAL"]
        ]

        assert len(gauges) == 6

        registered_events = {}
        
        for gauge in gauges:
            gauge_name = gauge[0]
            gauge_system = gauge[1]

            events = self.query_eboa.get_events(gauge_names = {"filter": gauge_name, "op": "=="},
                                                gauge_systems = {"filter": gauge_system, "op": "=="},
                                                start_filters = [{"date": "2024-05-24T08:46:34.438128", "op": "=="}],
                                                stop_filters = [{"date": "2024-05-24T08:46:34.454000", "op": "=="}])

            assert len(events) == 1
        
            assert events[0].get_structured_values() == [
                {"name": "value",
                 "type": "double",
                 "value": "1048576000.0"}
            ]

            assert events[0].event_uuid not in registered_events

            registered_events[events[0].event_uuid] = None
        # end for

        # Check counters for day Y
        gauges = [
            ["CUMULATIVE_DOWNLOADED_VOLUME_BY_MISSION_CLIENT_PER_DAY_2024-05-25T00:00:00_2024-05-26T00:00:00", "S2_#test"],
            ["CUMULATIVE_DOWNLOADED_VOLUME_BY_CLIENT_PER_DAY_2024-05-25T00:00:00_2024-05-26T00:00:00", "test"],
            ["CUMULATIVE_DOWNLOADED_VOLUME_BY_MISSION_PER_DAY_2024-05-25T00:00:00_2024-05-26T00:00:00", "S2_"],
            ["CUMULATIVE_DOWNLOADED_VOLUME_BY_MISSION_PRODUCT_TYPE_PER_DAY_2024-05-25T00:00:00_2024-05-26T00:00:00", "S2_#AUX_UT1UTC"],
            ["CUMULATIVE_DOWNLOADED_VOLUME_BY_PRODUCT_TYPE_PER_DAY_2024-05-25T00:00:00_2024-05-26T00:00:00", "AUX_UT1UTC"],
            ["CUMULATIVE_DOWNLOADED_VOLUME_PER_DAY_2024-05-25T00:00:00_2024-05-26T00:00:00", "GLOBAL"]
        ]

        assert len(gauges) == 6

        registered_events = {}
        
        for gauge in gauges:
            gauge_name = gauge[0]
            gauge_system = gauge[1]

            events = self.query_eboa.get_events(gauge_names = {"filter": gauge_name, "op": "=="},
                                                gauge_systems = {"filter": gauge_system, "op": "=="},
                                                start_filters = [{"date": "2024-05-25T08:46:34.438128", "op": "=="}],
                                                stop_filters = [{"date": "2024-05-25T08:46:34.454000", "op": "=="}])

            assert len(events) == 1
        
            assert events[0].get_structured_values() == [
                {"name": "value",
                 "type": "double",
                 "value": "1048576000.0"}
            ]

            assert events[0].event_uuid not in registered_events

            registered_events[events[0].event_uuid] = None
        # end for

        # Check global counters
        gauges = [
            ["CUMULATIVE_DOWNLOADED_VOLUME_BY_MISSION_CLIENT_PER_MONTH_2024-05-01T00:00:00_2024-06-01T00:00:00", "S2_#test"],
            ["CUMULATIVE_DOWNLOADED_VOLUME_BY_MISSION_CLIENT_PER_YEAR_2024-01-01T00:00:00_2025-01-01T00:00:00", "S2_#test"],
            ["CUMULATIVE_DOWNLOADED_VOLUME_BY_MISSION_CLIENT", "S2_#test"],
            ["CUMULATIVE_DOWNLOADED_VOLUME_BY_CLIENT_PER_MONTH_2024-05-01T00:00:00_2024-06-01T00:00:00", "test"],
            ["CUMULATIVE_DOWNLOADED_VOLUME_BY_CLIENT_PER_YEAR_2024-01-01T00:00:00_2025-01-01T00:00:00", "test"],
            ["CUMULATIVE_DOWNLOADED_VOLUME_BY_CLIENT", "test"],
            ["CUMULATIVE_DOWNLOADED_VOLUME_BY_MISSION_PER_MONTH_2024-05-01T00:00:00_2024-06-01T00:00:00", "S2_"],
            ["CUMULATIVE_DOWNLOADED_VOLUME_BY_MISSION_PER_YEAR_2024-01-01T00:00:00_2025-01-01T00:00:00", "S2_"],
            ["CUMULATIVE_DOWNLOADED_VOLUME_BY_MISSION", "S2_"],
            ["CUMULATIVE_DOWNLOADED_VOLUME_BY_MISSION_PRODUCT_TYPE_PER_MONTH_2024-05-01T00:00:00_2024-06-01T00:00:00", "S2_#AUX_UT1UTC"],
            ["CUMULATIVE_DOWNLOADED_VOLUME_BY_MISSION_PRODUCT_TYPE_PER_YEAR_2024-01-01T00:00:00_2025-01-01T00:00:00", "S2_#AUX_UT1UTC"],
            ["CUMULATIVE_DOWNLOADED_VOLUME_BY_MISSION_PRODUCT_TYPE", "S2_#AUX_UT1UTC"],
            ["CUMULATIVE_DOWNLOADED_VOLUME_BY_PRODUCT_TYPE_PER_MONTH_2024-05-01T00:00:00_2024-06-01T00:00:00", "AUX_UT1UTC"],
            ["CUMULATIVE_DOWNLOADED_VOLUME_BY_PRODUCT_TYPE_PER_YEAR_2024-01-01T00:00:00_2025-01-01T00:00:00", "AUX_UT1UTC"],
            ["CUMULATIVE_DOWNLOADED_VOLUME_BY_PRODUCT_TYPE", "AUX_UT1UTC"],
            ["CUMULATIVE_DOWNLOADED_VOLUME_PER_MONTH_2024-05-01T00:00:00_2024-06-01T00:00:00", "GLOBAL"],
            ["CUMULATIVE_DOWNLOADED_VOLUME_PER_YEAR_2024-01-01T00:00:00_2025-01-01T00:00:00", "GLOBAL"],
            ["CUMULATIVE_DOWNLOADED_VOLUME", "GLOBAL"],
            ["CUMULATIVE_DOWNLOADED_VOLUME_BY_MISSION_PRODUCT_TYPE_CLIENT", "S2_#AUX_UT1UTC#test"]
        ]

        assert len(gauges) == 19

        registered_events = {}
        
        for gauge in gauges:
            gauge_name = gauge[0]
            gauge_system = gauge[1]

            events = self.query_eboa.get_events(gauge_names = {"filter": gauge_name, "op": "=="},
                                                gauge_systems = {"filter": gauge_system, "op": "=="},
                                                start_filters = [{"date": "2024-05-24T08:46:34.438128", "op": "=="}],
                                                stop_filters = [{"date": "2024-05-25T08:46:34.454000", "op": "=="}])

            assert len(events) == 1
        
            assert events[0].get_structured_values() == [
                {"name": "value",
                 "type": "double",
                 "value": "2097152000.0"}
            ]

            assert events[0].event_uuid not in registered_events

            registered_events[events[0].event_uuid] = None
        # end for

        # Check number counter events
        # Check counters for day X
        gauges = [
            ["CUMULATIVE_DOWNLOADED_NUMBER_BY_MISSION_CLIENT_PER_DAY_2024-05-24T00:00:00_2024-05-25T00:00:00", "S2_#test"],
            ["CUMULATIVE_DOWNLOADED_NUMBER_BY_CLIENT_PER_DAY_2024-05-24T00:00:00_2024-05-25T00:00:00", "test"],
            ["CUMULATIVE_DOWNLOADED_NUMBER_BY_MISSION_PER_DAY_2024-05-24T00:00:00_2024-05-25T00:00:00", "S2_"],
            ["CUMULATIVE_DOWNLOADED_NUMBER_BY_MISSION_PRODUCT_TYPE_PER_DAY_2024-05-24T00:00:00_2024-05-25T00:00:00", "S2_#AUX_UT1UTC"],
            ["CUMULATIVE_DOWNLOADED_NUMBER_BY_PRODUCT_TYPE_PER_DAY_2024-05-24T00:00:00_2024-05-25T00:00:00", "AUX_UT1UTC"],
            ["CUMULATIVE_DOWNLOADED_NUMBER_PER_DAY_2024-05-24T00:00:00_2024-05-25T00:00:00", "GLOBAL"]
        ]

        assert len(gauges) == 6

        registered_events = {}
        
        for gauge in gauges:
            gauge_name = gauge[0]
            gauge_system = gauge[1]

            events = self.query_eboa.get_events(gauge_names = {"filter": gauge_name, "op": "=="},
                                                gauge_systems = {"filter": gauge_system, "op": "=="},
                                                start_filters = [{"date": "2024-05-24T08:46:34.438128", "op": "=="}],
                                                stop_filters = [{"date": "2024-05-24T08:46:34.454000", "op": "=="}])

            assert len(events) == 1
        
            assert events[0].get_structured_values() == [
                {"name": "value",
                 "type": "double",
                 "value": "1.0"}
            ]

            assert events[0].event_uuid not in registered_events

            registered_events[events[0].event_uuid] = None
        # end for

        # Check counters for day Y
        gauges = [
            ["CUMULATIVE_DOWNLOADED_NUMBER_BY_MISSION_CLIENT_PER_DAY_2024-05-25T00:00:00_2024-05-26T00:00:00", "S2_#test"],
            ["CUMULATIVE_DOWNLOADED_NUMBER_BY_CLIENT_PER_DAY_2024-05-25T00:00:00_2024-05-26T00:00:00", "test"],
            ["CUMULATIVE_DOWNLOADED_NUMBER_BY_MISSION_PER_DAY_2024-05-25T00:00:00_2024-05-26T00:00:00", "S2_"],
            ["CUMULATIVE_DOWNLOADED_NUMBER_BY_MISSION_PRODUCT_TYPE_PER_DAY_2024-05-25T00:00:00_2024-05-26T00:00:00", "S2_#AUX_UT1UTC"],
            ["CUMULATIVE_DOWNLOADED_NUMBER_BY_PRODUCT_TYPE_PER_DAY_2024-05-25T00:00:00_2024-05-26T00:00:00", "AUX_UT1UTC"],
            ["CUMULATIVE_DOWNLOADED_NUMBER_PER_DAY_2024-05-25T00:00:00_2024-05-26T00:00:00", "GLOBAL"]
        ]

        assert len(gauges) == 6

        registered_events = {}
        
        for gauge in gauges:
            gauge_name = gauge[0]
            gauge_system = gauge[1]

            events = self.query_eboa.get_events(gauge_names = {"filter": gauge_name, "op": "=="},
                                                gauge_systems = {"filter": gauge_system, "op": "=="},
                                                start_filters = [{"date": "2024-05-25T08:46:34.438128", "op": "=="}],
                                                stop_filters = [{"date": "2024-05-25T08:46:34.454000", "op": "=="}])

            assert len(events) == 1
        
            assert events[0].get_structured_values() == [
                {"name": "value",
                 "type": "double",
                 "value": "1.0"}
            ]

            assert events[0].event_uuid not in registered_events

            registered_events[events[0].event_uuid] = None
        # end for

        # Check global counters
        gauges = [
            ["CUMULATIVE_DOWNLOADED_NUMBER_BY_MISSION_CLIENT_PER_MONTH_2024-05-01T00:00:00_2024-06-01T00:00:00", "S2_#test"],
            ["CUMULATIVE_DOWNLOADED_NUMBER_BY_MISSION_CLIENT_PER_YEAR_2024-01-01T00:00:00_2025-01-01T00:00:00", "S2_#test"],
            ["CUMULATIVE_DOWNLOADED_NUMBER_BY_MISSION_CLIENT", "S2_#test"],
            ["CUMULATIVE_DOWNLOADED_NUMBER_BY_CLIENT_PER_MONTH_2024-05-01T00:00:00_2024-06-01T00:00:00", "test"],
            ["CUMULATIVE_DOWNLOADED_NUMBER_BY_CLIENT_PER_YEAR_2024-01-01T00:00:00_2025-01-01T00:00:00", "test"],
            ["CUMULATIVE_DOWNLOADED_NUMBER_BY_CLIENT", "test"],
            ["CUMULATIVE_DOWNLOADED_NUMBER_BY_MISSION_PER_MONTH_2024-05-01T00:00:00_2024-06-01T00:00:00", "S2_"],
            ["CUMULATIVE_DOWNLOADED_NUMBER_BY_MISSION_PER_YEAR_2024-01-01T00:00:00_2025-01-01T00:00:00", "S2_"],
            ["CUMULATIVE_DOWNLOADED_NUMBER_BY_MISSION", "S2_"],
            ["CUMULATIVE_DOWNLOADED_NUMBER_BY_MISSION_PRODUCT_TYPE_PER_MONTH_2024-05-01T00:00:00_2024-06-01T00:00:00", "S2_#AUX_UT1UTC"],
            ["CUMULATIVE_DOWNLOADED_NUMBER_BY_MISSION_PRODUCT_TYPE_PER_YEAR_2024-01-01T00:00:00_2025-01-01T00:00:00", "S2_#AUX_UT1UTC"],
            ["CUMULATIVE_DOWNLOADED_NUMBER_BY_MISSION_PRODUCT_TYPE", "S2_#AUX_UT1UTC"],
            ["CUMULATIVE_DOWNLOADED_NUMBER_BY_PRODUCT_TYPE_PER_MONTH_2024-05-01T00:00:00_2024-06-01T00:00:00", "AUX_UT1UTC"],
            ["CUMULATIVE_DOWNLOADED_NUMBER_BY_PRODUCT_TYPE_PER_YEAR_2024-01-01T00:00:00_2025-01-01T00:00:00", "AUX_UT1UTC"],
            ["CUMULATIVE_DOWNLOADED_NUMBER_BY_PRODUCT_TYPE", "AUX_UT1UTC"],
            ["CUMULATIVE_DOWNLOADED_NUMBER_PER_MONTH_2024-05-01T00:00:00_2024-06-01T00:00:00", "GLOBAL"],
            ["CUMULATIVE_DOWNLOADED_NUMBER_PER_YEAR_2024-01-01T00:00:00_2025-01-01T00:00:00", "GLOBAL"],
            ["CUMULATIVE_DOWNLOADED_NUMBER", "GLOBAL"],
            ["CUMULATIVE_DOWNLOADED_NUMBER_BY_MISSION_PRODUCT_TYPE_CLIENT", "S2_#AUX_UT1UTC#test"]
        ]

        assert len(gauges) == 19

        registered_events = {}
        
        for gauge in gauges:
            gauge_name = gauge[0]
            gauge_system = gauge[1]

            events = self.query_eboa.get_events(gauge_names = {"filter": gauge_name, "op": "=="},
                                                gauge_systems = {"filter": gauge_system, "op": "=="},
                                                start_filters = [{"date": "2024-05-24T08:46:34.438128", "op": "=="}],
                                                stop_filters = [{"date": "2024-05-25T08:46:34.454000", "op": "=="}])

            assert len(events) == 1
        
            assert events[0].get_structured_values() == [
                {"name": "value",
                 "type": "double",
                 "value": "2.0"}
            ]

            assert events[0].event_uuid not in registered_events

            registered_events[events[0].event_uuid] = None
        # end for

        events = self.query_eboa.get_events(gauge_names = {"filter": "CUMULATIVE_DOWNLOAD_TIME", "op": "=="},
                                            gauge_systems = {"filter": "GLOBAL", "op": "=="},
                                            start_filters = [{"date": "2024-05-24T08:46:34.438128", "op": "=="}],
                                            stop_filters = [{"date": "2024-05-25T08:46:34.454000", "op": "=="}])

        assert len(events) == 1

        assert events[0].get_structured_values() == [
            {"name": "value",
             "type": "double",
             "value": "0.031743184"}
        ]

        events = self.query_eboa.get_events(gauge_names = {"filter": "CUMULATIVE_DOWNLOAD_SPEED", "op": "=="},
                                            gauge_systems = {"filter": "GLOBAL", "op": "=="},
                                            start_filters = [{"date": "2024-05-24T08:46:34.438128", "op": "=="}],
                                            stop_filters = [{"date": "2024-05-25T08:46:34.454000", "op": "=="}])

        assert len(events) == 1

        assert events[0].get_structured_values() == [
            {"name": "value",
             "type": "double",
             "value": "132132428807.394"}
        ]
