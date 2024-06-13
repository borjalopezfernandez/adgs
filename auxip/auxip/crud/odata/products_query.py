from sqlalchemy.orm import Session

from ...models import products as models
from ...schemas import products as schemas
from ...logger import logger

def odata_get_product(db: Session, query: str):
    logger.debug(f"odata_get_product: {query}")

    count   = None
    filter  = None
    top     = None
    skip    = None
    orderby = None

    if "$count=true" in query:
        count = True

    if "$count=false" in query:
        count = False    

    if "$filter=" in query:
        if "&" in query.split("$filter=")[1]:
            filter = query.split("$filter=")[1].split("&")[0]
        else:
            filter = query.split("$filter=")[1]

    if "$top=" in query:
        if "&" in query.split("$top=")[1]:
            top = int(query.split("$top=")[1].split("&")[0])
        else:
            top = int(query.split("$top=")[1])

    if "skip=" in query:
        if "&" in query.split("$skip=")[1]:
            skip = int(query.split("$skip=")[1].split("&")[0])
        else:
            skip = int(query.split("$skip=")[1])

    if "$orderby" in query:
        if "&" in query.split("$orderby=")[1]:
            orderby = query.split("$orderby=")[1].split("&")[0]
        else:
            orderby = query.split("$orderby=")[1]

    if filter != None:
        logger.debug(f"$filter={filter}")

    if orderby != None:
        logger.debug(f"$orderby={orderby}")

    if count != None:
        logger.debug(f"$count={count}")

    if top != None:
        logger.debug(f"$top={str(top)}")

    if skip != None:
        logger.debug(f"$skip={str(skip)}")

    if count == True:
        logger.debug(f"perform query count with filter {filter}")
        return "666"

    logger.debug(f"odata_get_product: END")


    return
