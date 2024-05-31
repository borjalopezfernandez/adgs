# Create SQLAlchemy models
# https://fastapi.tiangolo.com/tutorial/sql-databases/
# https://pypi.org/project/sqlalchemy-guid/
# https://www.getorchestra.io/guides/fastapi-and-datetime-types-a-comprehensive-guide

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

from .database import Base


class Product(Base):
    __tablename__ = "archived_files"
    Name = Column(String(255), primary_key=True, unique=False)
    ContentType = Column(String(63), unique=False)
    ContentLength = Column(Integer, nullable=False)


class EnumSubscriptionStatus(str, enum.Enum):
    running = 0
    paused = 1
    cancelled = 2


class Subscription(Base):
    __tablename__ = "subscriptions"
    Id                              = Column(Uuid, primary_key = True, default=uuid.uuid4)
    Status: EnumSubscriptionStatus  = Column(Enum(EnumSubscriptionStatus))
    FilterParam                     = Column(String(512), unique = False)
    NotificationEndpoint            = Column(String(255), unique = False)
    NotificationEpUsername          = Column(String(63), unique = False)
    NotificationEpPassword          = Column(String(255), unique = False)
    LastNotificationDate            = Column(DateTime, nullable = True, default=null)
    SubmissionDate                  = Column(DateTime)
