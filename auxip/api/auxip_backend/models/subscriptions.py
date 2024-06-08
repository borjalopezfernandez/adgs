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

from .. import database
from .. database import get_db
from .. database import Base

class EnumSubscriptionStatus(str, enum.Enum):
    running     = 0
    paused      = 1
    cancelled   = 2


class Subscription(Base):
    __tablename__ = "subscription"
    Id                              = Column(Uuid,          primary_key = True, default=uuid.uuid4)
    Status: EnumSubscriptionStatus  = Column(Enum(EnumSubscriptionStatus))
    FilterParam                     = Column(String(512),   unique = False)
    NotificationEndpoint            = Column(String(255),   unique = False)
    NotificationEpUsername          = Column(String(63),    unique = False)
    NotificationEpPassword          = Column(String(255),   unique = False)
    LastNotificationDate            = Column(DateTime,      nullable = True, default=null)
    SubmissionDate                  = Column(DateTime)

    def __repr__(self):
        return f"Id:{self.Id} - Status:{self.Status}"


class SubscriptionNotification(Base):
    __tablename__ = "subscription_notification"
    ProductId                       = Column(Uuid)
    SubscriptionId                  = Column(Uuid)
    ProductName                     = Column(String(255),   unique = False)
    NotificationDate                = Column(DateTime,      nullable = False)
    # extended attributes not part of ESA-EOPG-EOPGC-IF-10 Issue 1.5 Date 26/04/2023
    id                              = Column(Integer,       primary_key = True, autoincrement = True)
    NotificationSuccess             = Column(Boolean,       nullable = False)
    NotificationInfo                = Column(String(512),   unique = False)


class Product(Base):
    __tablename__   = "archived_files"
    Name            = Column(String(255), primary_key=True, unique=False)
    ContentType     = Column(String(63), unique=False)
    ContentLength   = Column(Integer, nullable=False)