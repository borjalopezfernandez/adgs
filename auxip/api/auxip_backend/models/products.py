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

'''

class Product(Base):
    __tablename__       = "archived_files"
    uuid                = Column(Uuid)
    name                = Column(String(255))
    filename            = Column(String(255))
    filetype            = Column(String(63))
    detection_date      = Column(DateTime,      nullable = True)
    last_access_date    = Column(DateTime,      nullable = True)
    validity_start      = Column(DateTime,      nullable = True)
    validity_stop       = Column(DateTime,      nullable = True)
    access_counter      = Column(Integer,       nullable = True)

'''