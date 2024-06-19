"""
Automated tests for the ingestion of the list of products in CSV format from the baseline configuration web page

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

class TestListProductsCsv(unittest.TestCase):
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
        
    def test_insert_list_products_csv(self):
        """
        This test verifies the ingestion of the list of products in CSV format from the baseline configuration web page
        """
        
        filename = "list_products.csv"
        file_path = os.path.dirname(os.path.abspath(__file__)) + "/inputs/" + filename

        exit_status = ingestion.command_process_file("adgsboa.ingestions.ingestion_products_csv.ingestion_products_csv", file_path, "2018-01-01T00:00:00")

        assert len([item for item in exit_status if item["status"] != eboa_engine.exit_codes["OK"]["status"]]) == 0
