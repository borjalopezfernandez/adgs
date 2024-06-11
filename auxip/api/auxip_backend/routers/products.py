from typing import Any
from uuid import UUID
from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse, Response

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
    product_id      = products.ProductId(Id=UUID(id))
    db_product      = crud.get_product(db=db,   product_id = product_id)
    product         = products.ProductBase( Id                          = str(db_product.uuid),
                                            Name                        = db_product.name,
                                            ContentLength               = db_product.size,
                                            ContentDate                 = {"ContentDate" : {"Start" : db_product.validity_start.strftime("%Y-%m-%dT%H:%M:%S.000Z"), "End" : db_product.validity_stop.strftime("%Y-%m-%dT%H:%M:%S.000Z")} },
                                            PublicationDate             = db_product.archive_date.strftime("%Y-%m-%dT%H:%M:%S.000Z"),
                                            Checksum                    = {"Checksum" : { "Algorithm" : "MD5", "Value" : str(db_product.md5), "ChecksumDate" : db_product.archive_date.strftime("%Y-%m-%dT%H:%M:%S.000Z") } }
                                           )
    headers         = {"x-get-product-metadata-custom": "test-value",
                            "Content-Language": "en-UK"}
    return Response(content=product.model_dump_json(), media_type= "application/json", headers=headers)

# --------------------------------------------------------------------
