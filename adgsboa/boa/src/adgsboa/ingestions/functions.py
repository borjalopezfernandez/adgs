"""
Helper module for the ingestion_functions of files of ADGSBOA

Written by DEIMOS Space S.L. (dibb)

module adgsboa
"""

# Import helpers
from eboa.engine.functions import get_resources_path, get_schemas_path

# Import xml parser
from lxml import etree

# Import errors
from adgsboa.ingestions.errors import ConfigCannotBeRead, ConfigDoesNotPassSchema

# Import logging
from eboa.logging import Log
import logging

logging_module = Log(name = __name__)
logger = logging_module.logger

###########
# Functions for managing the completeness and timeliness configuration
###########
def get_completeness_timeliness_conf():
    '''
    Function to obtain the configuration of the completeness and timeliness

    :return: xpath structure of the configuration of the completeness and timeliness
    :rtype: etree.XPathEvaluator
    '''
    schema_path = get_schemas_path() + "/adgs_completeness_timeliness_schema.xsd"
    parsed_schema = etree.parse(schema_path)
    schema = etree.XMLSchema(parsed_schema)
    # Get configuration
    try:
        completeness_timeliness_xml = etree.parse(get_resources_path() + "/adgs_completeness_timeliness.xml")
    except etree.XMLSyntaxError as e:
        logger.error("The completeness and timeliness configuration file ({}) cannot be read".format(get_resources_path() + "/adgs_completeness_timeliness.xml"))
        raise ConfigCannotBeRead("The completeness and timeliness configuration file ({}) cannot be read".format(get_resources_path() + "/adgs_completeness_timeliness.xml"))
    # end try

    valid = schema.validate(completeness_timeliness_xml)
    if not valid:
        logger.error("The completeness and timeliness configuration file ({}) does not pass the schema ({})".format(get_resources_path() + "/adgs_completeness_timeliness.xml", get_schemas_path() + "/adgs_completeness_timeliness_schema.xsd"))
        raise ConfigDoesNotPassSchema("The completeness and timeliness configuration file ({}) does not pass the schema ({})".format(get_resources_path() + "/adgs_completeness_timeliness.xml", get_schemas_path() + "/adgs_completeness_timeliness_schema.xsd"))
    # end if

    completeness_timeliness_xpath = etree.XPathEvaluator(completeness_timeliness_xml)

    return completeness_timeliness_xpath

###########
# Functions for managing the constellations configuration
###########
def get_copernicus_constellations_conf():
    '''
    Function to obtain the configuration of the Copernicus constellations

    :return: xpath structure of the configuration of the Copernicus constellations
    :rtype: etree.XPathEvaluator
    '''
    schema_path = get_schemas_path() + "/copernicus_constellations_schema.xsd"
    parsed_schema = etree.parse(schema_path)
    schema = etree.XMLSchema(parsed_schema)
    # Get configuration
    try:
        copernicus_constellations_xml = etree.parse(get_resources_path() + "/copernicus_constellations.xml")
    except etree.XMLSyntaxError as e:
        logger.error("The Copernicus constellations configuration file ({}) cannot be read".format(get_resources_path() + "/copernicus_constellations.xml"))
        raise ConfigCannotBeRead("The Copernicus constellations configuration file ({}) cannot be read".format(get_resources_path() + "/copernicus_constellations.xml"))
    # end try

    valid = schema.validate(copernicus_constellations_xml)
    if not valid:
        logger.error("The Copernicus constellations configuration file ({}) does not pass the schema ({})".format(get_resources_path() + "/copernicus_constellations.xml", get_schemas_path() + "/copernicus_constellations_schema.xsd"))
        raise ConfigDoesNotPassSchema("The Copernicus constellations configuration file ({}) does not pass the schema ({})".format(get_resources_path() + "/copernicus_constellations.xml", get_schemas_path() + "/copernicus_constellations_schema.xsd"))
    # end if

    copernicus_constellations_xpath = etree.XPathEvaluator(copernicus_constellations_xml)

    return copernicus_constellations_xpath
