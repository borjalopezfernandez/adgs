import datetime
import enum
import uuid

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    String,
    null,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.types import Uuid
from sqlalchemy_guid import GUID

from .. database import Base

class Product(Base):
    __table_args__      = {'extend_existing': True}
    __tablename__       = "archived_files"
    id                  = Column(Integer, primary_key =True)
    uuid                = Column(Uuid)
    name                = Column("name", String(256))
    path                = Column(String(512))        
    filename            = Column(String(256))
    filetype            = Column(String(64))
    md5                 = Column(String(32))
    size                = Column(Integer,       nullable = True)
    detection_date      = Column(DateTime,      nullable = True)
    archive_date        = Column(DateTime,      nullable = True)
    last_access_date    = Column(DateTime,      nullable = True)
    validity_start      = Column(DateTime,      nullable = True)
    validity_stop       = Column(DateTime,      nullable = True)
    access_counter      = Column(Integer,       nullable = True)
    info                = Column(String)