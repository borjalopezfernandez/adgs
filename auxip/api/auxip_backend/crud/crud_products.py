import json
from sqlalchemy.orm import Session
from uuid import UUID

from .. models import products as models
from .. schemas import products as schemas
from .. logger import logger

# -----------------------------------------------------------------------------

def get_product_list_id(db: Session):
   logger.debug("get_product_list_id")
   return db.query(models.Product.uuid).all()

# -----------------------------------------------------------------------------

def get_product(db: Session, product_id: schemas.ProductId):
   logger.debug("get_product: Id (input)            => {}".format(product_id.Id))
   result   = db.query(models.Product).filter(models.Product.uuid == product_id.Id).first()
   logger.debug(f"get_product: uuid                  => {result.uuid}")
   logger.debug(f"get_product: name                  => {result.name}")
   logger.debug(f"get_product: filename              => {result.name}")
   logger.debug(f"get_product: path                  => {result.path}")
   logger.debug("get_product: archive_date          => {}".format(result.archive_date.strftime("%Y-%m-%dT%H:%M:%S.000Z") ) )
   if result.detection_date != None:
      logger.debug("get_product: detection_date          => {}".format(result.detection_date.strftime("%Y-%m-%dT%H:%M:%S.000Z") ) )
   logger.debug(f"get_product: size                  => {result.size}")
   logger.debug(f"get_product: md5                   => {result.md5}")
   logger.debug("get_product: validity_start        => {}".format(result.validity_start.strftime("%Y-%m-%dT%H:%M:%S.000Z") ) )
   logger.debug("get_product: validity_stop         => {}".format(result.validity_stop.strftime("%Y-%m-%dT%H:%M:%S.000Z") ) )
   logger.debug(f"get_product: access_counter        => {result.access_counter}")
   logger.debug(f"get_product: info                  => {result.info}")
   return result

# -----------------------------------------------------------------------------    
