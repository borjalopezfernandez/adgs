from typing import Any
from uuid import UUID
from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, status
from fastapi.responses import JSONResponse, FileResponse, Response

from .. database import get_db
from .. import logger as app_logger
from .. crud import crud_products as crud
from .. schemas import products

from sqlalchemy.orm import Session

app_logger.logger.info(f"API Router start => {__name__}")

router = APIRouter(
   tags           = ["Products"], 
   dependencies   = [Depends(get_db) ]
)

# -------------------------------------------------------------------

def my_background_task(file : str):
    app_logger.logger.info(f"my background task executed for {file}")

# -------------------------------------------------------------------


"""
    AUXIP Get List of Products ID
"""

# TO-DO: pydantic verification of list of objects

@router.get("/odata/v1/Products/Id", 
    status_code     = status.HTTP_200_OK
    # response_model  = products.ProductId
)
async def get_product_list_id(db: Session = Depends(get_db)) -> Any:
    app_logger.logger.debug("/get product_list_id")
    db_list_id         = crud.get_product_list_id(db=db)
    list_product_id    = []
    for row in db_list_id:
        app_logger.logger.debug(str(row[0]))
        list_product_id.append( products.ProductId( Id = str(row[0]) ) )
    return(list_product_id)


# -------------------------------------------------------------------


# -------------------------------------------------------------------

"""
    AUXIP Get Product by ID
"""

@router.get("/odata/v1/Product/Id/{id}",
    tags            = ["Products"],
    status_code     = status.HTTP_200_OK,
    response_model  = products.ProductBase
)
async def get_product(id: str, db: Session = Depends(get_db)) -> Any:
    app_logger.logger.debug(f"/get product {id}") 
    product_id      = products.ProductId(Id = UUID(id))
    db_product      = crud.get_product(db = db, product_id = product_id)
    product         = products.ProductBase( Id                          = str(db_product.uuid),
                                            Name                        = db_product.name,
                                            ContentLength               = db_product.size,
                                            ContentDate                 = {"ContentDate" : {"Start" : db_product.validity_start.strftime("%Y-%m-%dT%H:%M:%S.000Z"), "End" : db_product.validity_stop.strftime("%Y-%m-%dT%H:%M:%S.000Z")} },
                                            PublicationDate             = db_product.archive_date.strftime("%Y-%m-%dT%H:%M:%S.000Z"),
                                            Checksum                    = {"Checksum" : { "Algorithm" : "MD5", "Value" : str(db_product.md5), "ChecksumDate" : db_product.archive_date.strftime("%Y-%m-%dT%H:%M:%S.000Z") } }
                                           )
    headers         = {"x-get-product-metadata-custom": "test-value",
                            "Content-Language": "en-UK"}
    return Response(content = product.model_dump_json(), media_type = "application/json", headers = headers)

# --------------------------------------------------------------------


# -------------------------------------------------------------------

"""
    AUXIP Download by Product Id

    https://<service-root-uri>/odata/v1/Products(Id)/$value

    curl -X 'GET' 'http://localhost:8000/odata/v1/Products(e5834d1b-a705-44ac-bb36-4f1715c755df)/$value' \ -H 'accept: application/json'

"""

# https://github.com/tiangolo/fastapi/discussions/8630

@router.get("/odata/v1/Products({id})/$value", 
    status_code     = status.HTTP_200_OK
)
async def product_download(id: str, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    """
    - Product download over the OData API is initiated using the ‘Id’ for each product returned in the GET Products List Response
    - The URI for the download of a single product is: https://<service-root-uri>/odata/v1/Products(Id)/$value
    - Id is the UUID assigned per product.
    - The download is considered in the OData protocol through the /$value URL
    """
    app_logger.logger.debug(f"/get product_download {id}")
    product_id = products.ProductId(Id = UUID(id))
    db_product = crud.get_product(db = db, product_id = product_id)
    file_path  = f"{db_product.path}/{db_product.filename}"
    app_logger.logger.debug(f"/get product_download {file_path}")
    background_tasks.add_task(my_background_task, file_path)
    try:
        return FileResponse(file_path, filename = db_product.filename)
    except Exception as e:
        app_logger.logger.error(f"Failed get product_download: {e}")
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="The service is unavailable due to a connection error.")


# -------------------------------------------------------------------


"""
    AUXIP Product Query

    https://<service-root-uri>/odata/v1/Products?

    curl -X 'GET' 'http://localhost:8000/odata/v1/Products?' \ -H 'accept: application/json'

"""

@router.get("/odata/v1/Products{query}")
async def product_query(background_tasks: BackgroundTasks, query: str = Path(..., title = "OData query", description = "query (do not forget the question mark) ?$filter=startswith(Name,'S2')"), db: Session = Depends(get_db)):
    """
    query: OData query
    - Query for Product Entity / Attributes: https://<service-root-uri>/odata/v1/Products
    - ?$count=true&$filter=startswith(Name,'S2')
    - ?$filter=startswith(Name,'S1A_AUX_')
    - ?$skip=13&$top=1000&$filter=startswith(Name,'S2')
    - ?$orderby=PublicationDate desc
    """
    app_logger.logger.debug(f"/get product_query: {query}")
    
    # If it is not a query raise 404
    if query[0:1] != "?":
        return Response(status_code = status.HTTP_404_NOT_FOUND)
    
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
            orderby = query.split("$filter=")[1].split("&")[0]
        else:
            orderby = query.split("$filter=")[1]

    if "$top=" in query:
        if "&" in query.split("$top=")[1]:
            top = int(query.split("$top=")[1].split("&")[0])
        else:
            top = int(query.split("$top=")[1])

    if "skip=" in query:
        if "&" in query.split("$skip=")[1]:
            top = int(query.split("$skip=")[1].split("&")[0])
        else:
            top = int(query.split("$skip=")[1])

    if "$orderby" in query:
        if "&" in query.split("$orderby=")[1]:
            orderby = query.split("$orderby=")[1].split("&")[0]
        else:
            orderby = query.split("$orderby=")[1]

    if filter != None:
        app_logger.logger.debug(f"$filter={filter}")

    if orderby != None:
        app_logger.logger.debug(f"$orderby={orderby}")

    if count != None:
        app_logger.logger.debug(f"$count={count}")

    if top != None:
        app_logger.logger.debug(f"$top={str(top)}")

    if skip != None:
        app_logger.logger.debug(f"$skip={str(skip)}")

    if count == True:
        app_logger.logger.debug(f"perform query count with filter {filter}")
        return "666"


    return {"received": query}


# -------------------------------------------------------------------