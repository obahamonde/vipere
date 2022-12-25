from db import FQLModel as Q
from typing import *
from pydantic import *

class LambdaFunction(Q):
    sub: str = Field(...)
    name: str = Field(...)
    arn: str = Field(...)
    url: str = Field(...)
    
    
func = LambdaFunction(sub="test", name="test", arn="test", url="test")
