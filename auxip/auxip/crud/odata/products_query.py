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
    

def _query_tokenizer(query: str):
    query_token = {"count" : None, "filter" : None, "top" : None, "skip" : None, "orderby" : None}

    if "$count=true" in query:
        query_token["count"] = True

    if "$count=false" in query:
        query_token["count"] = False
  
    if "$filter=" in query:
        if "&" in query.split("$filter=")[1]:
            query_token["filter"] = query.split("$filter=")[1].split("&")[0]
        else:
            query_token["filter"] = query.split("$filter=")[1]
        
    if "$top=" in query:
        if "&" in query.split("$top=")[1]:
            query_token["top"] = int(query.split("$top=")[1].split("&")[0])
        else:
            query_token["top"] = int(query.split("$top=")[1])

    if "skip=" in query:
        if "&" in query.split("$skip=")[1]:
            query_token["skip"] = int(query.split("$skip=")[1].split("&")[0])
        else:
            query_token["skip"] = int(query.split("$skip=")[1])

    if "$orderby" in query:
        if "&" in query.split("$orderby=")[1]:
            query_token["orderby"] = query.split("$orderby=")[1].split("&")[0]
        else:
            query_token["orderby"] = query.split("$orderby=")[1]

    if query_token["orderby"] != None:
        logger.debug("$orderby={}".format(query_token["orderby"]) )

    if query_token["count"] != None:
        logger.debug("$count={}".format(query_token["count"]) )

    if query_token["top"] != None:
        logger.debug("$top={}".format(query_token["top"]) )

    if query_token["skip"] != None:
        logger.debug("$skip={}".format(query_token["skip"]) )

    return query_token


'''
> The “or” operator allows clients to apply different filter values on the same filter function. The “or” operator shall not be used on different functions.
> The “not” operator allows clients to omit certain results from the query.
> The “in” operator allows for a shorthand way of writing multiple “eq” expressions joined by “or”.
'''

def _query(db: Session, query_token: Dict):
    if query_token["filter"] == None and query_token["count"] == None and query_token["orderby"] == None:
        logger.error(f"query not supported / OData parameters not found in {query_token}")
        raise ValueError("bad raquest: query not supported / OData parameters not found")

    # simple $count without $filter
    if query_token["count"] == True and query_token["filter"] == None:
        return _query_count(db = db, query_token = query_token)

    #if "and" not in query_token["filter"] and not "or" in query_token["filter"] and "not" not in query_token["filter"] and "in" not in query_token["filter"]:
    logger.debug("filter query")
    result = _query_filter(db = db, query_token = query_token)
    logger.debug("$filter query")
    return result



def _query_count(db: Session, query_token: Dict):
    logger.debug("_query_count()")

    if query_token["filter"] == None and query_token["count"] == True:
        logger.debug("perform query $count no $filter")
        result = db.query(models.Product).all()
        count  = len(result)
        logger.debug("$count is equal to {}".format(str(count)))
        return str(count)

    if query_token["filter"] != None and query_token["count"] == True:
        logger.debug("perform query $count with $filter : {}".format(query_token["filter"]))
        return
    
    raise ValueError(f"Internal error of _query_count : {query_token}")


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

def _query_filter(db: Session, query_token: Dict):
    list_operator_or = []
    list_filter_name = []

    if "contains" not in query_token["filter"] and "endswith" not in query_token["filter"] and "startswith" not in query_token["filter"] and "PublicationDate" not in query_token["filter"] and "ContentDate" not in query_token["filter"]:
        logger.error("query not compliant with ICD / OData $filter function / parameters not found")
        raise ValueError("query not compliant with ICD / OData $filter function / parameters not found")

    if "contains" in query_token["filter"] or "endswith" in query_token["filter"] or "startswith" in query_token["filter"]:
        filter = query_token["filter"]

        if odata_function_name_startswith in query_token["filter"]:
            value = _extract_filter_function_name_param(query_token["filter"], odata_function_name_startswith)
            list_filter_name.append(value)
            
        if odata_function_name_endswith in query_token["filter"]:
            value = _extract_filter_function_name_param(query_token["filter"], odata_function_name_endswith)
            list_filter_name.append(value)

        if odata_function_name_contains in query_token["filter"]:
            value = _extract_filter_function_name_param(query_token["filter"], odata_function_name_contains)
            list_filter_name.append(value)
        
        logger.debug("filter by function name : {}".format(list_filter_name) )
        
        # filter for just one condition 
        result = db.query(models.Product).filter(models.Product.filename.like( str(list_filter_name[0]) ) ).all()

        if query_token["count"] == True:
            logger.debug("$count is equal to {} / $filter : {}".format(len(result), query_token["filter"]))
            return str(len(result))
        else:
            logger.debug("{} items found / $filter : {}".format(len(result), query_token["filter"]))
            return result
        
    else:
        logger.error("NOT IMPLEMENTED")


def odata_get_product(db: Session, query: str):
    logger.debug(f"odata_get_product: {query}")
    query_token = {}
    query_token = _query_tokenizer(query = query)
    logger.debug(f"{query_token}")
    return _query(db = db, query_token = query_token)
