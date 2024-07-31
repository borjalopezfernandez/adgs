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
                
    def test_insert_empty_list_products_csv(self):
        """
        This test verifies the ingestion of the list of products in CSV format without any item
        """
        
        filename = "empty_list_products.csv"
        file_path = os.path.dirname(os.path.abspath(__file__)) + "/inputs/" + filename

        exit_status = ingestion.command_process_file("adgsboa.ingestions.ingestion_products_csv.ingestion_products_csv", file_path, "2018-01-01T00:00:00")

        assert len([item for item in exit_status if item["status"] != eboa_engine.exit_codes["OK"]["status"]]) == 0

    def test_insert_s1_1_product_from_auxip_csv(self):
        """
        This test verifies the ingestion of one S1 product in CSV format from the baseline configuration web page
        """
        
        filename = "list_one_product_S1SAR.csv"
        file_path = os.path.dirname(os.path.abspath(__file__)) + "/inputs/" + filename

        exit_status = ingestion.command_process_file("adgsboa.ingestions.ingestion_products_csv.ingestion_products_csv", file_path, "2018-01-01T00:00:00")

        assert len([item for item in exit_status if item["status"] != eboa_engine.exit_codes["OK"]["status"]]) == 0

        # Check number of sources inserted
        sources = self.query_eboa.get_sources()

        assert len(sources) == 2

        # Check sources inserted
        sources = self.query_eboa.get_sources(validity_start_filters = [{"date": "2015-10-05T22:59:43", "op": "=="}],
                                              validity_stop_filters = [{"date": "2015-10-07T00:59:43", "op": "=="}],
                                              processors = {"filter": "ingestion_products_csv.py", "op": "=="},
                                              dim_signatures = {"filter": "AUXILIARY_PRODUCTS", "op": "=="},
                                              names = {"filter": "list_one_product_S1SAR.csv", "op": "=="},
                                              ingestion_completeness = True)

        assert len(sources) == 1

        sources = self.query_eboa.get_sources(validity_start_filters = [{"date": "2015-10-05T22:59:43", "op": "=="}],
                                              validity_stop_filters = [{"date": "2015-10-07T00:59:43", "op": "=="}],
                                              processors = {"filter": "ingestion_products_csv.py_S1A_OPER_AUX_POEORB_OPOD_20151026T122329_V20151005T225943_20151007T005943.EOF.zip", "op": "=="},
                                              dim_signatures = {"filter": "AUXILIARY_PRODUCTS_BASELINE_S1A", "op": "=="},
                                              names = {"filter": "list_one_product_S1SAR.csv", "op": "=="},
                                              ingestion_completeness = True)

        assert len(sources) == 1

        # Check number of events generated
        events = self.query_eboa.get_events()

        assert len(events) == 2

        # Check AUXILIARY_PRODUCT events
        events = self.query_eboa.get_events(gauge_names = {"filter": "AUXILIARY_PRODUCT", "op": "=="})

        assert len(events) == 1

        events = self.query_eboa.get_events(gauge_names = {"filter": "AUXILIARY_PRODUCT", "op": "=="},
                                            gauge_systems = {"filter": "AUX_POE", "op": "=="},
                                                start_filters = [{"date": "2015-10-05T22:59:43", "op": "=="}],
                                                stop_filters = [{"date": "2015-10-07T00:59:43", "op": "=="}])

        assert len(events) == 1
        
        assert events[0].get_structured_values() == [
            {"name": "satellite",
             "type": "text",
             "value": "S1A"},
            {"name": "mission",
             "type": "text",
             "value": "S1_"},
            {"name": "associated_product_levels",
             "type": "text",
             "value": "L1"},
            {"name": "associated_product_types",
             "type": "text",
             "value": "L1GRD, L1SLC"},
            {"name": "processing_version",
             "type": "text",
             "value": "S1-IPF-03.31"}
        ]

        # Check AUXILIARY_PRODUCT_BASELINE events
        events = self.query_eboa.get_events(gauge_names = {"filter": "AUXILIARY_PRODUCT_BASELINE", "op": "=="})

        assert len(events) == 1

        events = self.query_eboa.get_events(gauge_names = {"filter": "AUXILIARY_PRODUCT_BASELINE", "op": "=="},
                                            gauge_systems = {"filter": "AUX_POE", "op": "=="},
                                                start_filters = [{"date": "2015-10-05T22:59:43", "op": "=="}],
                                                stop_filters = [{"date": "2015-10-07T00:59:43", "op": "=="}])

        assert len(events) == 1
        
        assert events[0].get_structured_values() == [
            {"name": "satellite",
             "type": "text",
             "value": "S1A"},
            {"name": "mission",
             "type": "text",
             "value": "S1_"},
            {"name": "associated_product_levels",
             "type": "text",
             "value": "L1"},
            {"name": "associated_product_types",
             "type": "text",
             "value": "L1GRD, L1SLC"},
            {"name": "processing_version",
             "type": "text",
             "value": "S1-IPF-03.31"}
        ]


    def test_insert_s2_1_product_from_auxip_csv(self):
        """
        This test verifies the ingestion of one S2 product in CSV format from the baseline configuration web page
        """
        
        filename = "list_one_product_S2MSI.csv"
        file_path = os.path.dirname(os.path.abspath(__file__)) + "/inputs/" + filename

        exit_status = ingestion.command_process_file("adgsboa.ingestions.ingestion_products_csv.ingestion_products_csv", file_path, "2018-01-01T00:00:00")

        assert len([item for item in exit_status if item["status"] != eboa_engine.exit_codes["OK"]["status"]]) == 0

        # Check number of sources inserted
        sources = self.query_eboa.get_sources()

        assert len(sources) == 2

        # Check sources inserted
        sources = self.query_eboa.get_sources(validity_start_filters = [{"date": "2015-08-19T13:42:39", "op": "=="}],
                                              validity_stop_filters = [{"date": "2015-09-03T11:13:13", "op": "=="}],
                                              processors = {"filter": "ingestion_products_csv.py", "op": "=="},
                                              dim_signatures = {"filter": "AUXILIARY_PRODUCTS", "op": "=="},
                                              names = {"filter": "list_one_product_S2MSI.csv", "op": "=="},
                                              ingestion_completeness = True)

        assert len(sources) == 1

        sources = self.query_eboa.get_sources(validity_start_filters = [{"date": "2015-08-19T13:42:39", "op": "=="}],
                                              validity_stop_filters = [{"date": "2015-09-03T11:13:13", "op": "=="}],
                                              processors = {"filter": "ingestion_products_csv.py_S2A_OPER_GIP_R2EQOG_MPC__20210413T000000_V20150819T134239_20150903T111313_B05.TGZ", "op": "=="},
                                              dim_signatures = {"filter": "AUXILIARY_PRODUCTS_BASELINE_S2A", "op": "=="},
                                              names = {"filter": "list_one_product_S2MSI.csv", "op": "=="},
                                              ingestion_completeness = True)

        assert len(sources) == 1

        # Check number of events generated
        events = self.query_eboa.get_events()

        assert len(events) == 2

        # Check AUXILIARY_PRODUCT events
        events = self.query_eboa.get_events(gauge_names = {"filter": "AUXILIARY_PRODUCT", "op": "=="})

        assert len(events) == 1

        events = self.query_eboa.get_events(gauge_names = {"filter": "AUXILIARY_PRODUCT", "op": "=="},
                                            gauge_systems = {"filter": "GIP_R2EQOG", "op": "=="},
                                                start_filters = [{"date": "2015-08-19T13:42:39", "op": "=="}],
                                                stop_filters = [{"date": "2015-09-03T11:13:13", "op": "=="}])

        assert len(events) == 1
        
        assert events[0].get_structured_values() == [
            {"name": "satellite",
             "type": "text",
             "value": "S2A"},
            {"name": "mission",
             "type": "text",
             "value": "S2_"},
            {"name": "associated_product_levels",
             "type": "text",
             "value": "L1"},
            {"name": "associated_product_types",
             "type": "text",
             "value": "L1A, L1B, L1C"},
            {"name": "processing_version",
             "type": "text",
             "value": "V2B-4.2.8"}
        ]

        # Check AUXILIARY_PRODUCT_BASELINE events
        events = self.query_eboa.get_events(gauge_names = {"filter": "AUXILIARY_PRODUCT_BASELINE", "op": "=="})

        assert len(events) == 1

        events = self.query_eboa.get_events(gauge_names = {"filter": "AUXILIARY_PRODUCT_BASELINE", "op": "=="},
                                            gauge_systems = {"filter": "GIP_R2EQOG", "op": "=="},
                                                start_filters = [{"date": "2015-08-19T13:42:39", "op": "=="}],
                                                stop_filters = [{"date": "2015-09-03T11:13:13", "op": "=="}])

        assert len(events) == 1
        
        assert events[0].get_structured_values() == [
            {"name": "satellite",
             "type": "text",
             "value": "S2A"},
            {"name": "mission",
             "type": "text",
             "value": "S2_"},
            {"name": "associated_product_levels",
             "type": "text",
             "value": "L1"},
            {"name": "associated_product_types",
             "type": "text",
             "value": "L1A, L1B, L1C"},
            {"name": "processing_version",
             "type": "text",
             "value": "V2B-4.2.8"}
        ]


    def test_insert_s3_1_product_from_auxip_csv(self):
        """
        This test verifies the ingestion of one S3 product in CSV format from the baseline configuration web page
        """
        
        filename = "list_one_product_S3ALL.csv"
        file_path = os.path.dirname(os.path.abspath(__file__)) + "/inputs/" + filename

        exit_status = ingestion.command_process_file("adgsboa.ingestions.ingestion_products_csv.ingestion_products_csv", file_path, "2018-01-01T00:00:00")

        assert len([item for item in exit_status if item["status"] != eboa_engine.exit_codes["OK"]["status"]]) == 0

        # Check number of sources inserted
        sources = self.query_eboa.get_sources()

        assert len(sources) == 2

        # Check sources inserted
        sources = self.query_eboa.get_sources(validity_start_filters = [{"date": "2020-05-27T15:00:00", "op": "=="}],
                                              validity_stop_filters = [{"date": "2020-05-28T03:00:00", "op": "=="}],
                                              processors = {"filter": "ingestion_products_csv.py", "op": "=="},
                                              dim_signatures = {"filter": "AUXILIARY_PRODUCTS", "op": "=="},
                                              names = {"filter": "list_one_product_S3ALL.csv", "op": "=="},
                                              ingestion_completeness = True)

        assert len(sources) == 1

        sources = self.query_eboa.get_sources(validity_start_filters = [{"date": "2020-05-27T15:00:00", "op": "=="}],
                                              validity_stop_filters = [{"date": "2020-05-28T03:00:00", "op": "=="}],
                                              processors = {"filter": "ingestion_products_csv.py_S3__AX___MA1_AX_20200527T150000_20200528T030000_20200528T053940___________________ECW_O_SN_001.SEN3.zip", "op": "=="},
                                              dim_signatures = {"filter": "AUXILIARY_PRODUCTS_BASELINE_S3_", "op": "=="},
                                              names = {"filter": "list_one_product_S3ALL.csv", "op": "=="},
                                              ingestion_completeness = True)

        assert len(sources) == 1

        # Check number of events generated
        events = self.query_eboa.get_events()

        assert len(events) == 2

        # Check AUXILIARY_PRODUCT events
        events = self.query_eboa.get_events(gauge_names = {"filter": "AUXILIARY_PRODUCT", "op": "=="})

        assert len(events) == 1

        events = self.query_eboa.get_events(gauge_names = {"filter": "AUXILIARY_PRODUCT", "op": "=="},
                                            gauge_systems = {"filter": "AX___MA1_AX", "op": "=="},
                                                start_filters = [{"date": "2020-05-27T15:00:00", "op": "=="}],
                                                stop_filters = [{"date": "2020-05-28T03:00:00", "op": "=="}])

        assert len(events) == 1
        
        assert events[0].get_structured_values() == [
            {"name": "satellite",
             "type": "text",
             "value": "S3_"},
            {"name": "mission",
             "type": "text",
             "value": "S3_"},
            {"name": "associated_product_levels",
             "type": "text",
             "value": "L2, L1"},
            {"name": "associated_product_types",
             "type": "text",
             "value": "L2, L1"},
            {"name": "processing_version",
             "type": "text",
             "value": "S3B-1.45"}
        ]

        # Check AUXILIARY_PRODUCT_BASELINE events
        events = self.query_eboa.get_events(gauge_names = {"filter": "AUXILIARY_PRODUCT_BASELINE", "op": "=="})

        assert len(events) == 1

        events = self.query_eboa.get_events(gauge_names = {"filter": "AUXILIARY_PRODUCT_BASELINE", "op": "=="},
                                            gauge_systems = {"filter": "AX___MA1_AX", "op": "=="},
                                                start_filters = [{"date": "2020-05-27T15:00:00", "op": "=="}],
                                                stop_filters = [{"date": "2020-05-28T03:00:00", "op": "=="}])

        assert len(events) == 1
        
        assert events[0].get_structured_values() == [
            {"name": "satellite",
             "type": "text",
             "value": "S3_"},
            {"name": "mission",
             "type": "text",
             "value": "S3_"},
            {"name": "associated_product_levels",
             "type": "text",
             "value": "L2, L1"},
            {"name": "associated_product_types",
             "type": "text",
             "value": "L2, L1"},
            {"name": "processing_version",
             "type": "text",
             "value": "S3B-1.45"}
        ]

    def test_insert_s1_products_from_auxip_csv(self):
        """
        This test verifies the ingestion of the list of all S1 products in CSV format from the baseline configuration web page
        """
        
        filename = "list_products_S1SAR.csv"
        file_path = os.path.dirname(os.path.abspath(__file__)) + "/inputs/" + filename

        exit_status = ingestion.command_process_file("adgsboa.ingestions.ingestion_products_csv.ingestion_products_csv", file_path, "2018-01-01T00:00:00")

        assert len([item for item in exit_status if item["status"] != eboa_engine.exit_codes["OK"]["status"]]) == 0

    def test_insert_s2_products_from_auxip_csv(self):
        """
        This test verifies the ingestion of the list of all S2 products in CSV format from the baseline configuration web page
        """
        
        filename = "list_products_S2MSI.csv"
        file_path = os.path.dirname(os.path.abspath(__file__)) + "/inputs/" + filename

        exit_status = ingestion.command_process_file("adgsboa.ingestions.ingestion_products_csv.ingestion_products_csv", file_path, "2018-01-01T00:00:00")

        assert len([item for item in exit_status if item["status"] != eboa_engine.exit_codes["OK"]["status"]]) == 0

    def test_insert_s3_products_from_auxip_csv(self):
        """
        This test verifies the ingestion of the list of all S3 products in CSV format from the baseline configuration web page
        """
        
        filename = "list_products_S3ALL.csv"
        file_path = os.path.dirname(os.path.abspath(__file__)) + "/inputs/" + filename

        exit_status = ingestion.command_process_file("adgsboa.ingestions.ingestion_products_csv.ingestion_products_csv", file_path, "2018-01-01T00:00:00")

        assert len([item for item in exit_status if item["status"] != eboa_engine.exit_codes["OK"]["status"]]) == 0

    def test_insert_s1_products_nominal_from_auxip_csv(self):
        """
        This test verifies the ingestion of the list of all S1 products in CSV format from the baseline configuration web page
        """
        
        filename = "list_products_nominal_S1SAR.csv"
        file_path = os.path.dirname(os.path.abspath(__file__)) + "/inputs/" + filename

        exit_status = ingestion.command_process_file("adgsboa.ingestions.ingestion_products_csv.ingestion_products_csv", file_path, "2018-01-01T00:00:00")

        assert len([item for item in exit_status if item["status"] != eboa_engine.exit_codes["OK"]["status"]]) == 0

    def test_insert_s2_products_nominal_from_auxip_csv(self):
        """
        This test verifies the ingestion of the list of all S2 products in CSV format from the baseline configuration web page
        """
        
        filename = "list_products_nominal_S2MSI.csv"
        file_path = os.path.dirname(os.path.abspath(__file__)) + "/inputs/" + filename

        exit_status = ingestion.command_process_file("adgsboa.ingestions.ingestion_products_csv.ingestion_products_csv", file_path, "2018-01-01T00:00:00")

        assert len([item for item in exit_status if item["status"] != eboa_engine.exit_codes["OK"]["status"]]) == 0

    def test_insert_s3_products_nominal_from_auxip_csv(self):
        """
        This test verifies the ingestion of the list of all S3 products in CSV format from the baseline configuration web page
        """
        
        filename = "list_products_nominal_S3ALL.csv"
        file_path = os.path.dirname(os.path.abspath(__file__)) + "/inputs/" + filename

        exit_status = ingestion.command_process_file("adgsboa.ingestions.ingestion_products_csv.ingestion_products_csv", file_path, "2018-01-01T00:00:00")

        assert len([item for item in exit_status if item["status"] != eboa_engine.exit_codes["OK"]["status"]]) == 0

    def test_insert_all_products_from_auxip_csv(self):
        """
        This test verifies the ingestion of the list of all products in CSV format from the baseline configuration web page
        """
        
        filename = "list_products_S1SAR.csv"
        file_path = os.path.dirname(os.path.abspath(__file__)) + "/inputs/" + filename

        exit_status = ingestion.command_process_file("adgsboa.ingestions.ingestion_products_csv.ingestion_products_csv", file_path, "2018-01-01T00:00:00")

        assert len([item for item in exit_status if item["status"] != eboa_engine.exit_codes["OK"]["status"]]) == 0

        filename = "list_products_S2MSI.csv"
        file_path = os.path.dirname(os.path.abspath(__file__)) + "/inputs/" + filename

        exit_status = ingestion.command_process_file("adgsboa.ingestions.ingestion_products_csv.ingestion_products_csv", file_path, "2018-01-01T00:00:00")

        assert len([item for item in exit_status if item["status"] != eboa_engine.exit_codes["OK"]["status"]]) == 0

        filename = "list_products_S3ALL.csv"
        file_path = os.path.dirname(os.path.abspath(__file__)) + "/inputs/" + filename

        exit_status = ingestion.command_process_file("adgsboa.ingestions.ingestion_products_csv.ingestion_products_csv", file_path, "2018-01-01T00:00:00")

        assert len([item for item in exit_status if item["status"] != eboa_engine.exit_codes["OK"]["status"]]) == 0

        filename = "list_products_S3MWR.csv"
        file_path = os.path.dirname(os.path.abspath(__file__)) + "/inputs/" + filename

        exit_status = ingestion.command_process_file("adgsboa.ingestions.ingestion_products_csv.ingestion_products_csv", file_path, "2018-01-01T00:00:00")

        assert len([item for item in exit_status if item["status"] != eboa_engine.exit_codes["OK"]["status"]]) == 0

        filename = "list_products_S3OLCI.csv"
        file_path = os.path.dirname(os.path.abspath(__file__)) + "/inputs/" + filename

        exit_status = ingestion.command_process_file("adgsboa.ingestions.ingestion_products_csv.ingestion_products_csv", file_path, "2018-01-01T00:00:00")

        assert len([item for item in exit_status if item["status"] != eboa_engine.exit_codes["OK"]["status"]]) == 0

        filename = "list_products_S3SLSTR.csv"
        file_path = os.path.dirname(os.path.abspath(__file__)) + "/inputs/" + filename

        exit_status = ingestion.command_process_file("adgsboa.ingestions.ingestion_products_csv.ingestion_products_csv", file_path, "2018-01-01T00:00:00")

        assert len([item for item in exit_status if item["status"] != eboa_engine.exit_codes["OK"]["status"]]) == 0

        filename = "list_products_S3SRAL.csv"
        file_path = os.path.dirname(os.path.abspath(__file__)) + "/inputs/" + filename

        exit_status = ingestion.command_process_file("adgsboa.ingestions.ingestion_products_csv.ingestion_products_csv", file_path, "2018-01-01T00:00:00")

        assert len([item for item in exit_status if item["status"] != eboa_engine.exit_codes["OK"]["status"]]) == 0

        filename = "list_products_S3SYN.csv"
        file_path = os.path.dirname(os.path.abspath(__file__)) + "/inputs/" + filename

        exit_status = ingestion.command_process_file("adgsboa.ingestions.ingestion_products_csv.ingestion_products_csv", file_path, "2018-01-01T00:00:00")

        assert len([item for item in exit_status if item["status"] != eboa_engine.exit_codes["OK"]["status"]]) == 0
        
        filename = "list_products_nominal_S1SAR.csv"
        file_path = os.path.dirname(os.path.abspath(__file__)) + "/inputs/" + filename

        exit_status = ingestion.command_process_file("adgsboa.ingestions.ingestion_products_csv.ingestion_products_csv", file_path, "2018-01-01T00:00:00")

        assert len([item for item in exit_status if item["status"] != eboa_engine.exit_codes["OK"]["status"]]) == 0

        filename = "list_products_nominal_S2MSI.csv"
        file_path = os.path.dirname(os.path.abspath(__file__)) + "/inputs/" + filename

        exit_status = ingestion.command_process_file("adgsboa.ingestions.ingestion_products_csv.ingestion_products_csv", file_path, "2018-01-01T00:00:00")

        assert len([item for item in exit_status if item["status"] != eboa_engine.exit_codes["OK"]["status"]]) == 0

        filename = "list_products_nominal_S3ALL.csv"
        file_path = os.path.dirname(os.path.abspath(__file__)) + "/inputs/" + filename

        exit_status = ingestion.command_process_file("adgsboa.ingestions.ingestion_products_csv.ingestion_products_csv", file_path, "2018-01-01T00:00:00")

        assert len([item for item in exit_status if item["status"] != eboa_engine.exit_codes["OK"]["status"]]) == 0
