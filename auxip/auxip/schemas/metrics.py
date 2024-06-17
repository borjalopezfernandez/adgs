"""
Definition of the model for metrics

module auxip
"""
# Import python utilities
import enum
import uuid
from datetime import datetime

# Import Pydantic utilities
from pydantic import BaseModel, ConfigDict, Field
from typing import Pattern, Union, Annotated, Literal, List

'''
    Command helper to extract the pattern of the metric name:

    $ echo "<productType>.<platformShortName>.<platformSerialIdentifier>.size
<productType>.<platformShortName>.<platformSerialIdentifier>.count
<platformShortName>.<platformSerialIdentifier>.size
Download.<productType>.<platformShortName>.<platformSerialIdentifier>.<ServiceAlias>.size
Download.<productType>.<platformShortName>.<platformSerialIdentifier>.<ServiceAlias>.completed
Download.<productType>.<platformShortName>.<platformSerialIdentifier>.<ServiceAlias>.failed
OriginToPublication.Daily.min.time.<productType>.<platformShortName>.<platformSerialIdentifier>
OriginToPublication.Daily.max.time.<productType>.<platformShortName>.<platformSerialIdentifier>
OriginToPublication.Daily.avg.time.<productType>.<platformShortName>.<platformSerialIdentifier>
OriginToPublication.Monthly.min.time.<productType>.<platformShortName>.<platformSerialIdentifier>
OriginToPublication.Monthly.max.time.<productType>.<platformShortName>.<platformSerialIdentifier>
OriginToPublication.Monthly.avg.time.<productType>.<platformShortName>.<platformSerialIdentifier>
Service.<KPI>.value" | sed 's/\./\\./g' | sed 's/<[^.]\+>/\.+/g' |sed 's/^/"/' |sed 's/$/|" \\/'
'''

class MetricFilter(BaseModel):
    filter: str = Field(alias="$filter")

class GaugeMetric(BaseModel):
    '''
    Gauge metric model definition
    '''
    model_config = ConfigDict(extra="forbid")
    Name : str = Field(pattern=r"(OriginToPublication\.Daily\.min\.time\.[^.]+\.[^.]+\.[^.]+|" \
                       "OriginToPublication\.Daily\.max\.time\.[^.]+\.[^.]+\.[^.]+|" \
                       "OriginToPublication\.Daily\.avg\.time\.[^.]+\.[^.]+\.[^.]+|" \
                       "OriginToPublication\.Monthly\.min\.time\.[^.]+\.[^.]+\.[^.]+|" \
                       "OriginToPublication\.Monthly\.max\.time\.[^.]+\.[^.]+\.[^.]+|" \
                       "OriginToPublication\.Monthly\.avg\.time\.[^.]+\.[^.]+\.[^.]+|" \
                       "Service\.[^.]+\.value)")
    Timestamp: datetime
    MetricType : Literal["Gauge"]
    Gauge : str

class CounterMetric(BaseModel):
    '''
    Counter metric model definition
    '''
    model_config = ConfigDict(extra="forbid")
    Name : str = Field(pattern=r"([^.]+\.[^.]+\.[^.]+\.size|" \
                       "[^.]+\.[^.]+\.[^.]+\.count|" \
                       "[^.]+\.[^.]+\.size|" \
                       "Download\.[^.]+\.[^.]+\.[^.]+\.[^.]+\.size|" \
                       "Download\.[^.]+\.[^.]+\.[^.]+\.[^.]+\.completed|" \
                       "Download\.[^.]+\.[^.]+\.[^.]+\.[^.]+\.failed)")
    Timestamp: datetime
    MetricType : Literal["Counter"]
    Count : int

GaugeUnionCounterMetrics = Annotated[Union[GaugeMetric, CounterMetric], Field(discriminator='MetricType')]

class Metric(BaseModel):
    '''
    Metric model definition
    '''
    model_config = ConfigDict(extra="forbid")
    odata_context: Literal["auxip/$metadata#Metrics"] = Field(alias="@odata.context")
    value: List[GaugeUnionCounterMetrics]
