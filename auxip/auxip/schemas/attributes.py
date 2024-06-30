import typing
from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime

class Attributes(BaseModel):
    model_config       = ConfigDict(from_attributes=True)
    Name               : str
    ValueType          : str = Field(default = "String") | Field(default = "Integer") | Field(default = "DateTimeOffset") | Field(default = "DateTimeOffset") | Field(default = "Boolean") | Field(default = "Double")
    Value              : str | int | datetime | bool