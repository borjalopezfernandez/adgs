import re

'''
ESA-EOPG-EOPGC-SP-2 1.8 11/04/2023

SENTINEL-2 PRODUCT ATTRIBUTES MAPPING for AUX

> Mapping can be either static from some minarc inventory column
> Mapping can also be dynamic for resolution by some function at execution time 

'''

def sentinels_odata_attribute_to_minarc(attribute : str , param : str):
    if attribute == "platformShortName":
        return f"{param[0]}{param[-1]}"
    raise(f"{attribute} not supported in sentinels_odata_attribute_to_minarc")

sentinels_auxip_odata_entity_minarc = {
    "Name"          :       "filename",
    "ContentDate"   :       ["validity_start", "validity_stop"],
}


sentinels_auxip_odata_attribute_minarc_field = {
    "beginningDateTime"         : "validity_start",
    "endingDateTime"            : "validity_stop",
    "productType"               : "filetype",
    "processorVersion"          : "eval(\"TO-BE-DEFINED\")",
    "processingCenter"          : "filename[20:24]",
    "platformShortName"         : "filename[0:2]",
    "platformSerialIdentifier"  : "filename[2:3]"
}


sentinels_auxip_odata_attribute_processing = {
    "beginningDateTime"     : None,
    "endingDateTime"        : None,
    "productType"           : None,
    "processorVersion"      : None,
    "processingCenter"      : None,
    "platformShortName"     : sentinels_odata_attribute_to_minarc,
    "platformSerialIdentifier"  : None
}


def sentinels_auxip_odata_attribute_is_colum_substring(param):
    if "[" in param and ":" in param and "]" in param:
        return True
    else:
        return False


def sentinels_auxip_odata_attribute_get_column_substring(param):
    return re.search("\[.*\]$", param).group()


def sentinels_auxip_odata_attribute_get_column(param):
    return param.split("[")[0]
