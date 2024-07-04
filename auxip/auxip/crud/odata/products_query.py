from datetime import datetime
import re
from typing import Any, Dict, List
from sqlalchemy.orm import Session
from sqlalchemy import select
from ...models import products as models
from ...schemas import products as schemas
from ...logger import logger

# CSC OData Mapping
from ...minarc.metadata_auxip_odata import sentinels_auxip_odata_attribute_minarc_field as sentinels_auxip_odata_attribute_minarc
from ...minarc.metadata_auxip_odata import sentinels_auxip_odata_entity_product_minarc_field as sentinels_auxip_odata_entity_product_minarc
from ...minarc.metadata_auxip_odata import sentinels_auxip_odata_attribute_is_colum_substring as is_colum_substring
from ...minarc.metadata_auxip_odata import sentinels_auxip_odata_attribute_get_column_substring as get_column_substring
from ...minarc.metadata_auxip_odata import sentinels_auxip_odata_attribute_get_column as get_column
from ...minarc.metadata_auxip_odata import sentinels_auxip_odata_attribute_processing as odata_attribute_processing

odata_function_name_endswith                =   "endswith"
odata_function_name_contains                =   "contains"
odata_function_name_startswith              =   "startswith"         
odata_query_option_count                    =   "$count"
odata_attributes_copernicus                 =   "Attributes/OData.CSC"
odata_product_attribute_publicationdate     =   "PublicationDate"
odata_product_attribute_contentdate         =   "ContentDate"

FILTER_OPERATORS = {
    "in"    : "in_",
    "eq"    : "__eq__",
    "not"   : "__ne__",
    "gte"   : "__ge__",
    "lte"   : "__le__",
    "gt"    : "__gt__",
    "lt"    : "__lt__",
    "like"  : "like",
}

'''
TO-DO-PENDING
> The “or” operator allows clients to apply different filter values on the same filter function. The “or” operator shall not be used on different functions.
> The “not” operator allows clients to omit certain results from the query.
> The “in” operator allows for a shorthand way of writing multiple “eq” expressions joined by “or”.
'''


# current support for ContentDate:
# https://<service-root-uri>/odata/v1/Products?$filter=ContentDate/Start gt 2019-05-15T00:00:00.000Z and ContentDate/End lt 2019-05-16T00:00:00.000Z
# Time is in UTC in the format YYYY-MM-DDThh:mm:ss.sssZ
# "ContentDate": { "Start": "2019-02-17T09:00:00.000Z", "End": "2019-02-17T21:00:00.000Z" }

def  _query_by_content_date(db: Session, filter: str):
    logger.debug(f"_query_by_content_date : $filter={filter}")
    query = db.query(models.Product)
    current             = filter.partition("ContentDate/Start")
    column_start        = sentinels_auxip_odata_entity_product_minarc["ContentDate/Start"]
    operation_start     = current[2].split(" ")[1]
    str_date_start      = current[2].split(" ")[2]
    date_start          = datetime.strptime(str_date_start, '%Y-%m-%dT%H:%M:%S.%fZ')
    current             = filter.partition("ContentDate/End")
    column_end          = sentinels_auxip_odata_entity_product_minarc["ContentDate/End"]
    operation_end       = current[2].split(" ")[1]
    str_date_end        = current[2].split(" ")[2]
    date_end            = datetime.strptime(str_date_start, '%Y-%m-%dT%H:%M:%S.%fZ')

    if operation_start == "eq":
        logger.debug(f"ContentDate/Start {operation_start} {str_date_start}")
        query = query.filter( column_start == date_start )
    elif operation_start == "gt":
        logger.debug(f"ContentDate/Start {operation_start} {str_date_start}")
        query = query.filter( column_start > date_start )
    elif operation_start == "gte":
        logger.debug(f"ContentDate/Start {operation_start} {str_date_start}")
        query = query.filter( column_start >= date_start )
    elif operation_start == "lt":
        logger.debug(f"ContentDate/Start {operation_start} {str_date_start}")
        query = query.filter( column_start < date_start )
    elif operation_start == "lte":
        logger.debug(f"ContentDate/Start {operation_start} {str_date_start}")
        query = query.filter( column_start <= date_start )
    else:
        error_message = f"Requested ContentDate/Start operation {operation_start} is not available"
        logger.error(error_message)
        raise error_message

    if query.count() == 0:
        logger.debug("query ContentDate/Start {} {} {}".format(column_start, operation_start, date_start))
        return []

    if operation_end == "eq":
        logger.debug(f"ContentDate/End {operation_end} {str_date_end}")
        result = query.filter( column_end == date_end )
    elif operation_start == "gt":
        logger.debug(f"ContentDate/End {operation_end} {str_date_end}")
        result = query.filter( column_end > date_end )
    elif operation_start == "gte":
        logger.debug(f"ContentDate/End {operation_end} {str_date_end}")
        result = query.filter( column_end >= date_end )
    elif operation_start == "lt":
        logger.debug(f"ContentDate/End {operation_end} {str_date_end}")
        result = query.filter( column_end < date_end )
    elif operation_start == "lte":
        logger.debug(f"ContentDate/End {operation_end} {str_date_end}")
        result = query.filter( column_end <= date_end )
    else:
        error_message = f"Requested ContentDate/End operation {operation_end} is not available"
        logger.error(error_message)
        raise error_message

    if result.count() == 0:
        logger.debug("query ContentDate/Start {} {} {}".format(column_start, operation_end, date_end))
        return []

    return result.all()


# current support for PublicationDate:
# $filter=PublicationDate gt 2020-05-15T00:00:00.000Z
# Time is in UTC in the format YYYY-MM-DDThh:mm:ss.sssZ

def  _query_by_publication_date(db: Session, filter: str):
    logger.debug(f"_query_by_publication_date : $filter={filter}")
    current             = filter.partition("PublicationDate")
    column              = sentinels_auxip_odata_entity_product_minarc["PublicationDate"]
    operation           = current[2].split(" ")[1]
    alchemy_op          = FILTER_OPERATORS[operation]
    str_date            = current[2].split(" ")[2]
    publication_date    = datetime.strptime(str_date, '%Y-%m-%dT%H:%M:%S.%fZ')
        
    if operation == "eq":
        logger.debug(f"PublicationDate {operation} {str_date}")
        result = db.query(models.Product).filter( column == publication_date ).all()
    elif operation == "gt":
        logger.debug(f"PublicationDate {operation} {str_date}")
        result = db.query(models.Product).filter( column > publication_date ).all()
    elif operation == "gte":
        logger.debug(f"PublicationDate {operation} {str_date}")
        result = db.query(models.Product).filter( column >= publication_date ).all()
    elif operation == "lt":
        logger.debug(f"PublicationDate {operation} {str_date}")
        result = db.query(models.Product).filter( column < publication_date ).all()
    elif operation == "lte":
        logger.debug(f"PublicationDate {operation} {str_date}")
        result = db.query(models.Product).filter( column <= publication_date ).all()
    else:
        error_message = f"Requested PublicationDate operation {operation} is not available"
        logger.error(error_message)
        raise error_message
    # end if    
    return result


'''
S2__OPER_AUX_UT1UTC_PDMC_20240605T000000_V20170101T000000_21000101T000000.7z

https://<service-root-uri>/odata/v1/Products?$filter=Attributes/OData.CSC.StringAttribute/any(att:att/Name eq 'productType' 
    and att/OData.CSC.StringAttribute/Value eq 'AUX_UT1UTC') 
    and Attributes/OData.CSC.StringAttribute/any(att:att/Name eq 'platformShortName' and att/OData.CSC.StringAttribute/Value eq 'SENTINEL-2')
'''

def _query_db_list_attribute_filter(db: Session, list_attribute_filter):
    query = db.query(models.Product)
    for filter_attribute in list_attribute_filter:
        col_name        = sentinels_auxip_odata_attribute_minarc[filter_attribute["Name"]]
        col_value       = filter_attribute["Value"]
        result_substr   = None

        if is_colum_substring(sentinels_auxip_odata_attribute_minarc[filter_attribute["Name"]]):
            col_name        = get_column( sentinels_auxip_odata_attribute_minarc[filter_attribute["Name"]]  )
    
        if odata_attribute_processing[filter_attribute["Name"]] != None:
            col_value       = odata_attribute_processing[filter_attribute["Name"]](filter_attribute["Name"], filter_attribute["Value"])

        logger.debug("query OData/Attr {} = {} ; column {}".format(filter_attribute["Name"], col_value, col_name))
        query = query.filter(getattr(models.Product, col_name).like("%%%s%%" % col_value))
        
        if query.count() == 0:
            logger.debug("query OData/Attr {} = {} ; column {}".format(filter_attribute["Name"], col_value, col_name))
            return []

    results = query.all()
    return results


def _filter_results_list_attribute_filter(result, list_attribute_filter):
    new_result = []
    for filter_attribute in list_attribute_filter:
        result_substr   = None
        filter_value    = None
        
        if is_colum_substring(sentinels_auxip_odata_attribute_minarc[filter_attribute["Name"]]):
            filter_name     = get_column( sentinels_auxip_odata_attribute_minarc[filter_attribute["Name"]]  )
            result_substr   = get_column_substring( sentinels_auxip_odata_attribute_minarc[filter_attribute["Name"]] )
        
        if odata_attribute_processing[filter_attribute["Name"]] != None:
            filter_value    = odata_attribute_processing[filter_attribute["Name"]](filter_attribute["Name"], filter_attribute["Value"])

        logger.debug("schema  OData/Attr {} == {}".format(filter_attribute["Name"], filter_value, filter_name))

        for item in result:
            if is_colum_substring(sentinels_auxip_odata_attribute_minarc[filter_attribute["Name"]]): 
                substr = f"item.{filter_name}{result_substr}"
                logger.debug("filtering by {} with value {} to be equal to {}".format(substr, eval(substr), filter_name) )
                if eval(substr) == filter_value:
                    if item not in new_result:
                        new_result.append(item)
            else:
                if item not in new_result:
                    new_result.append(item)

    return new_result


# current support for OData.CSC.StringAttribute
def  _query_by_attributes(db: Session, filter: str):
    logger.debug(f"_query_by_attributes : $filter={filter}")
    list_filter_attribute = []
    current = str(filter)

    while "/Name eq " in current:
        current     = current.partition("/Name eq '")
        name        = current[2].split("'")[0]
        value       = current[2].split("/Value eq ")[1].split("'")[1]
        filter_attribute = {}
        filter_attribute["Name"]    = name
        filter_attribute["Value"]   = value
        list_filter_attribute.append(filter_attribute)
        current     = str(current[2])
        
    results         = _query_db_list_attribute_filter(db, list_filter_attribute)
    filter_results  = _filter_results_list_attribute_filter(results, list_filter_attribute)
    return filter_results

   
def _extract_filter_function_name_param(filter : str, function : str):    
    # split by the name of the function
    param_value_    = filter.split(function)[1].split(",")[1]
    # extract the value in between the single quotes
    value_          = re.findall(r'\'(.*?)\'', param_value_)[0]
    if odata_function_name_startswith in filter:
        return f"{value_}%"
    if odata_function_name_endswith in filter:
        return f"%{value_}"
    if odata_function_name_contains in filter:
        return f"%{value_}%"
    

'''

3.3 Query Products Catalogue
The Query Products Catalogue function is achieved through standard APIs according to the Entity Model described in Section 3.2. 
By default, the Products query are to be ordered by Publication Date, 
in an ascending order (e.g. any query for new products published since a previous query will find the list ordered from oldest to newest

'''


def _query_filter(db: Session, filter: str, count: str | None):
    logger.debug(f"_query_filter : $filter={filter}")
    
    list_filter_name = []

    # query sanity check
    if odata_attributes_copernicus not in filter and odata_function_name_contains not in filter and odata_function_name_startswith not in filter and odata_function_name_endswith not in filter and odata_product_attribute_publicationdate not in filter and odata_product_attribute_contentdate not in filter:
        logger.error("query not compliant with ICD / OData $filter function / parameters not found")
        raise ValueError("query not compliant with ICD / OData $filter function / parameters not found")
    

    '''
    3.3.1.4 Query by Attributes
    [AD-1], [AD-2], [AD-3], [AD-4] and [AD-5] provide the definition of the minimum metadata that shall be indexed for each product, and their origin within the product.

    https://<service-root-uri>/odata/v1/Products?$filter=Attributes/OData.CSC.StringAttribute/any(att:att/Name eq 'platformShortName' and att/OData.CSC.StringAttribute/Value eq 'SENTINEL-2') and Attributes/OData.CSC.StringAttribute/any(att:att/Name eq 'processingCenter' and att/OData.CSC.StringAttribute/Value eq 'PDMC') Attributes/OData.CSC.StringAttribute/any(att:att/Name eq 'productType' and att/OData.CSC.StringAttribute/Value eq 'AUX_UT1UTC')

    '''
    # query by OData Attributes
    if odata_attributes_copernicus in filter:
        result = _query_by_attributes(db = db, filter = filter)
        logger.debug("{} items found / $filter : {}".format(len(result), filter))
        return result


    '''
    3.3.1.2 Query by Product Publication Date:
    > https://<service-root-uri>/odata/v1/Products?$filter=PublicationDate gt 2020-05-15T00:00:00.000Z
    '''
    if odata_product_attribute_publicationdate in filter:
        result = _query_by_publication_date(db = db, filter = filter)
        logger.debug("{} items found / $filter : {}".format(len(result), filter))
        return result


    '''
    3.3.1.3 Query by Validity Date
    > The list of products filtered by validity date criteria can be retrieved for example as follows:
    https://<service-root-uri>/odata/v1/Products?$filter=ContentDate/Start gt 2019-05-15T00:00:00.000Z and ContentDate/End lt 2019-05-16T00:00:00.000Z

    '''
    if odata_product_attribute_contentdate in filter:
        result = _query_by_content_date(db = db, filter = filter)
        logger.debug("{} items found / $filter : {}".format(len(result), filter))
        return result


    '''
    3.3.1.1 Query by Product Name : $filter functions are:
    > contains : The contains function returns records with names containing a particular string at any position
    > endswith : The endswith function returns true if the first parameter string value ends with the second parameter string value, otherwise it returns false
    > startswith : The startswith function returns true if the first parameter string value starts with the second parameter string value, otherwise it returns false
    '''

    value = None
        
    if odata_function_name_contains in filter:
        value = _extract_filter_function_name_param(filter, odata_function_name_contains)

    if odata_function_name_startswith in filter:
        value = _extract_filter_function_name_param(filter, odata_function_name_startswith)
        
    if odata_function_name_endswith in filter:
        value = _extract_filter_function_name_param(filter, odata_function_name_endswith)

    list_filter_name.append(value)
     
    logger.debug("filter by function name : {}".format(list_filter_name[0]) )
    
    # filter for just one condition 
    result = db.query(models.Product).filter(models.Product.filename.like( str(list_filter_name[0]) ) ).all()

    if count != None:
        logger.debug("$count is equal to {} / $filter : {}".format(len(result), filter))
        return str(len(result))
    else:
        logger.debug("{} items found / $filter : {}".format(len(result), filter))
        return result


def odata_get_product(db: Session, count: str | None, filter: str | None, skip: str | None, top: str | None, orderby: str | None):
    logger.debug(f"odata_get_product : $count={count}")
    logger.debug(f"odata_get_product : $filter={filter}")
    logger.debug(f"odata_get_product : $top={top}")
    logger.debug(f"odata_get_product : $skip={skip}")
    logger.debug(f"odata_get_product : $orderby={orderby}")

    if filter == None and count == None and orderby == None:
        logger.error("query not supported / OData parameters not found")
        raise ValueError(f"bad raquest: query not supported / OData parameters not found in {filter}")

    if filter != None:
        return _query_filter(db = db, filter = filter, count = count)

