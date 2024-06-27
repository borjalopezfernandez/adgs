import enum
import uuid
from datetime import datetime
from typing import ClassVar, List, Optional, Union, Dict
from uuid import UUID, uuid4

from pydantic import BaseModel, ConfigDict, Field, SkipValidation, PrivateAttr
from pydantic import TypeAdapter


class ProductId(BaseModel):
    Id: UUID


class ProductCreate(BaseModel):
    pass


class ProductBase(BaseModel):
    model_config            = ConfigDict(from_attributes=True)
    Id                      : str
    Name                    : str
    ContentType             : str  = Field(default = "application/octet-stream")
    ContentLength           : int
    PublicationDate         : str
    # OriginDate              : str
    ContentDate             : Dict[ str, Dict[str,str] ]
    Checksum                : Dict[ str, Dict[str,str] ]

    def __str__(self):
        return f"{self.Id} : {self.Name} => {self.Checksum}"
    
    def __repr__(self):
        return f"{self.Id} : {self.Name}"
    


'''
{ "@odata.context": "$metadata#Products", "count": "2": "value": [ ] }
'''

class ODataResultProduct(BaseModel):
    json        : Dict [str, str | List[ProductBase]]

    