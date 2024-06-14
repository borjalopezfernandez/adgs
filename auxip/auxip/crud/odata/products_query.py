import re
from typing import Any, Dict
from sqlalchemy.orm import Session

from ...models import products as models
from ...schemas import products as schemas
from ...logger import logger

odata_function_name_endswith            =   "endswith"
odata_function_name_contains            =   "contains"
odata_function_name_startswith          =   "startswith"         
odata_query_option_count                =   "$count"

'''
TO-DO-PENDING
> The “or” operator allows clients to apply different filter values on the same filter function. The “or” operator shall not be used on different functions.
> The “not” operator allows clients to omit certain results from the query.
> The “in” operator allows for a shorthand way of writing multiple “eq” expressions joined by “or”.
'''

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
3.3.1.1 Query by Product Name : $filter functions are:
> contains : The contains function returns records with names containing a particular string at any position
> endswith : The endswith function returns true if the first parameter string value ends with the second parameter string value, otherwise it returns false
> startswith : The startswith function returns true if the first parameter string value starts with the second parameter string value, otherwise it returns false

3.3.1.2 Query by Product Publication Date:
> https://<service-root-uri>/odata/v1/Products?$filter=PublicationDate gt 2020-05-15T00:00:00.000Z

3.3.1.3 Query by Validity Date
> The list of products filtered by validity date criteria can be retrieved for example as follows:
https://<service-root-uri>/odata/v1/Products?$filter=ContentDate/Start gt 2019-05-15T00:00:00.000Z and ContentDate/End lt 2019-05-16T00:00:00.000Z

'''

def _query_filter(db: Session, filter: str, count: str | None):
    logger.debug(f"_query_filter : $filter={filter}")
    
    list_filter_name = []

    if odata_function_name_contains not in filter and odata_function_name_startswith not in filter and odata_function_name_endswith not in filter and "PublicationDate" not in filter and "ContentDate" not in filter:
        logger.error("query not compliant with ICD / OData $filter function / parameters not found")
        raise ValueError("query not compliant with ICD / OData $filter function / parameters not found")
    
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
    logger.debug("fodata_get_product : $orderby={orderby}")

    if filter == None and count == None and orderby == None:
        logger.error("query not supported / OData parameters not found")
        raise ValueError("bad raquest: query not supported / OData parameters not found")

    if filter != None:
        return _query_filter(db = db, filter = filter, count = count)
