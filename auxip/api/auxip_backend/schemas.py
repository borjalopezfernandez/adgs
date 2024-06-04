# > Pydantic models
# > Create an SubscriptionBase Pydantic models (or let's say "schemas") to have common attributes while creating or reading data
# > Create an SubcriptionCreate that inherit from them (so they will have the same attributes), plus any additional data (attributes) needed for creation

import enum
import uuid
from datetime import datetime
from typing import ClassVar, Optional, Union
from uuid import UUID, uuid4

from pydantic import BaseModel, ConfigDict, Field, SkipValidation, PrivateAttr


class EnumSubscriptionStatus(str, enum.Enum):
    running     = 0
    paused      = 1
    cancelled   = 2


class SubscriptionStatus(BaseModel):
    Id: UUID
    Status: EnumSubscriptionStatus


class SubscriptionId(BaseModel):
    Id: UUID


class SubscriptionBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    Id                      : UUID = Field(default_factory=uuid4)
    SubmissionDate          : datetime = Field(default=datetime.now())
    LastNotificationDate    : datetime = Field(default=datetime.now())
    Status                  : EnumSubscriptionStatus
    FilterParam             : str
    NotificationEndpoint    : str
    NotificationEpUsername  : str
    NotificationEpPassword  : str
    
    def __str__(self):
        return f"{self.Id} : {self.Status} => {self.NotificationEpUsername}"
    
    def __repr__(self):
        return f"{self.Id} : {self.Status}"


class SubscriptionOutput(SubscriptionBase):
    Id: UUID

    model_config = ConfigDict(  from_attributes         = True, 
                                arbitrary_types_allowed = True, 
                                use_enum_values         = True)

    
class SubscriptionCreate(SubscriptionBase):
    pass


class Subscription(SubscriptionBase):
    model_config = ConfigDict(  from_attributes         = True, 
                                arbitrary_types_allowed = True, 
                                use_enum_values         = True,
                                json_schema_extra       = {
                                    "example": {
                                    "Status": "0",
                                    "FilterParam": "contains(Name,'_AUX_ECMWFD_') and PublicationDate gt 2019-02-01T00:00:00.000Z and PublicationDate lt 2019-09-01T00:00:00.000Z",
                                    "NotificationEndpoint": "http://myserver.org",
                                    "NotificationEpUsername": "pinocchio",
                                    "NotificationEpPassword": "diLegno$",
                                    }
                                }
                            )

# -----------------------------------------------------------------------------

class SubscriptionNotification(BaseModel):
    model_config = ConfigDict(from_attributes =True ,
                              json_schema_extra       = {
                                  "example": {
                                    "SubscriptionId"    : "fb7a2da4-50d0-4c8c-ab5c-12f3279f3f4b",
                                    "ProductId"         : "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                                    "ProductName"       : "S2__OPER_AUX_UT1UTC_PDMC_20240513T000000_V20170101T000000_21000101T000000.7z",
                                    "NotificationDate"  : "2024-05-13T00:15:00.000Z",
                                    }
                              }
                            )
    SubscriptionId          : UUID
    ProductId               : UUID
    ProductName             : str
    NotificationDate        : datetime
    

class SubscriptionNotificationDB(SubscriptionNotification):
    model_config = ConfigDict(from_attributes=True)
    NotificationSuccess     : bool
    NotificationInfo        : str

# -----------------------------------------------------------------------------


class ProductBase(BaseModel):
    # name: str  = Field(alias='Name')
    Name: str
    ContentType: str
    ContentLength: int


class ProductCreate(ProductBase):
    pass


class Product(ProductBase):
    class ConfigProduct:
        from_attributes = True

        json_schema_extra = {
            "example": {
                "Name": "S2__OPER_AUX_ECMWFD_PDMC_20190216T120000_V20190217T090000_20190217T210000.TGZ",
                "ContentType": "application/octet-stream",
                "ContentLength": "8326253",
            }
        }
