import json
from typing import Any
from uuid import UUID
from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Request, Query, status
from fastapi.responses import JSONResponse, FileResponse, PlainTextResponse, Response
from fastapi.encoders import jsonable_encoder

from .. database import get_db
from .. import logger as app_logger
from .. crud import crud_products as crud
from .. crud.odata import products_query as odata_product_query
from .. schemas import products

from sqlalchemy.orm import Session

'''
HTTP Response Envelope
The following overall HTTP status codes may be returned with the response:
- 200 OK: if the request is accepted and a response can be returned
- 400 Bad Request
- 401 Unauthorized: if the requesting client is unauthorised
- 404 Not Found
- 429 Too Many Requests: if a quota is exceeded (see section 4.1.2)
- 500 Internal Server Error
'''

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
        return FileResponse(file_path, filename = db_product.filename, media_type = 'application/octet-stream')
    except Exception as e:
        app_logger.logger.error(f"Failed get product_download: {e}")
        raise HTTPException(status_code = 500 , detail="The service is unavailable due to a connection error.")


# -------------------------------------------------------------------

"""
    AUXIP Product Query

    https://<service-root-uri>/odata/v1/Products?

    curl -X 'GET' 'http://localhost:8000/odata/v1/Products?' \ -H 'accept: application/json'


"""

@router.get("/odata/v1/Products")
# async def product_query(background_tasks: BackgroundTasks, query: str = Path(..., title = "OData query", description = "query (do not forget the question mark) ?$filter=startswith(Name,'S2')"), db: Session = Depends(get_db)):
async def product_query(background_tasks: BackgroundTasks,
                        request : Request,
                        db      : Session = Depends(get_db),
                        filter  : str = Query(alias = "$filter",    default = None), 
                        count   : str = Query(alias = "$count",     default = None),
                        top     : str = Query(alias = "$top",       default = None), 
                        skip    : str = Query(alias = "$skip",      default = None),
                        orderby : str = Query(alias = "$orderby",   default = None),
                        ):
    """
    query: OData query
    - Query for Product Entity / Attributes: https://<service-root-uri>/odata/v1/Products
    - ?$count=true&$filter=startswith(Name,'S2')
    - ?$filter=startswith(Name,'S1A_AUX_')
    - ?$skip=13&$top=1000&$filter=startswith(Name,'S2')
    - ?$orderby=PublicationDate desc
    - ?$filter=startswith(Name,'S1') and endswith(Name,'.EOF.zip')
    - ?$filter=contains(Name,'AMH_ERRMAT') or contains(Name,'AMV_ERRMAT')
    - ?$filter=Attributes/OData.CSC.StringAttribute/any(att:att/Name eq 'productType' and att/OData.CSC.StringAttribute/Value eq 'AUX_UT1UTC')
    - ?$filter=Attributes/OData.CSC.StringAttribute/any(att:att/Name eq 'processingCenter' and att/OData.CSC.StringAttribute/Value eq 'PDMC')
    - ?$filter=Attributes/OData.CSC.StringAttribute/any(att:att/Name eq 'platformShortName' and att/OData.CSC.StringAttribute/Value eq 'SENTINEL-2')
    - ?$filter=Attributes/OData.CSC.StringAttribute/any(att:att/Name eq 'platformShortName' and att/OData.CSC.StringAttribute/Value eq 'SENTINEL-2') and Attributes/OData.CSC.StringAttribute/any(att:att/Name eq 'processingCenter' and att/OData.CSC.StringAttribute/Value eq 'PDMC')
    - ?$filter=Attributes/OData.CSC.StringAttribute/any(att:att/Name eq 'platformShortName' and att/OData.CSC.StringAttribute/Value eq 'SENTINEL-2') and Attributes/OData.CSC.StringAttribute/any(att:att/Name eq 'processingCenter' and att/OData.CSC.StringAttribute/Value eq 'PDMC') Attributes/OData.CSC.StringAttribute/any(att:att/Name eq 'productType' and att/OData.CSC.StringAttribute/Value eq 'AUX_UT1UTC')
    """
    app_logger.logger.debug("request.url.path           : {}".format(request.url.path) )
    app_logger.logger.debug("request.url.query_params   : {}".format(request.url) )
    app_logger.logger.debug("request.url.scheme         : {}".format(request.url.scheme) )
    app_logger.logger.debug(f"$filter : {filter}")

    try:
        result = odata_product_query.odata_get_product(db = db, count = count, filter = filter, top = top, skip = skip, orderby = orderby)
    except Exception as error:
        headers = {"x-product-query" : str(request.url) , "x-get-product-query-error": str(error), "Content-Language": "en-UK"}
        return PlainTextResponse("", headers = headers, status_code = 400)

    # $count=true returns a string with the number of elements
    if isinstance(result, str) == True:
        json_count_product   = {}
        json_count_product["@odata.context"]    = "$metadata#Products"
        json_count_product["count"]             = result
        return JSONResponse(content = json_count_product)

    list_product        = []
    json_list_product   = {}

    if result == None:
        app_logger.logger.debug("NO ITEMS")
        return

    for item in result:
        # app_logger.logger.debug("Name : ".format(item.filename) )
        product = products.ProductBase( Id                          = str(item.uuid),
                                        Name                        = item.filename,
                                        ContentLength               = item.size,
                                        ContentDate                 = {"ContentDate" : {"Start" : item.validity_start.strftime("%Y-%m-%dT%H:%M:%S.000Z"), "End" : item.validity_stop.strftime("%Y-%m-%dT%H:%M:%S.000Z")} },
                                        PublicationDate             = item.archive_date.strftime("%Y-%m-%dT%H:%M:%S.000Z"),
                                        Checksum                    = {"Checksum" : { "Algorithm" : "MD5", "Value" : str(item.md5), "ChecksumDate" : item.archive_date.strftime("%Y-%m-%dT%H:%M:%S.000Z") } }
                                    )
        list_product.append(jsonable_encoder(product))
        
    json_list_product["@odata.context"] = "$metadata#Products"
    json_list_product["value"]          = list_product
   
    return JSONResponse(content = json_list_product)
   

# -------------------------------------------------------------------