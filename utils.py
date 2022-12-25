"""

Utilitie functions for the FQL model.

"""

from uuid import uuid4
from datetime import datetime
from names import get_full_name
import json as JSON

JSON.stringify = JSON.dumps
JSON.parse = JSON.loads


from typing import Union, List, Dict
from pydantic import BaseModel

def tstamp(ts: int) -> float:
    return float(str(ts)[:10]+'.'+str(ts)[10:])

def id() -> str:
    return str(uuid4().hex)

def avatar()->str:
    return f"https://avatars.dicebear.com/api/avataaars/{id()}.svg"

def now():
    return datetime.now()

def serialize(response):
    return JSON.parse(JSON.stringify(response))

def parse(response):
    return JSON.parse(response)

