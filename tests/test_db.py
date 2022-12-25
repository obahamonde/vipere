"""

Test Suites based on Pytest Framework

"""

from db import FQLModelMetaClass as QM, FQLModel as Q
from names import get_full_name
from pydantic import Field


from utils import id as get_id, now as get_now , avatar as get_avatar, get_full_name


class LambdaFunction(Q):
    sub: str = Field(...)
    name: str = Field(...)
    arn: str = Field(...)
    url: str = Field(...)


mock = LambdaFunction(
        sub=get_id(),
        name=get_full_name(),
        arn=get_id(),
        url=get_avatar()
    )

def test_type():
    assert type(Q) == type(QM)


def test_schema():
    assert type(LambdaFunction.schema()) == dict

def test_schema_json():
    assert type(LambdaFunction.schema_json()) == str

def test_create():
    sub = get_id()
    name = get_full_name()
    arn = get_id()
    url = get_avatar()
    mock = LambdaFunction(sub=sub,name=name,arn=arn,url=url).create()
    assert mock['sub'] == sub

def test_save():
    sub = get_id()
    name = get_full_name()
    arn = get_id()
    url = get_avatar()
    mock = LambdaFunction(sub=sub,name=name,arn=arn,url=url).save()
    assert mock['sub'] == sub
    
def test_update():
    sub = get_id()
    name = get_full_name()
    arn = get_id()
    url = get_avatar()
    LambdaFunction(sub=sub,name=name,arn=arn,url=url).create()
    mock = LambdaFunction.update("sub",sub, data={"name": "test"})
    assert mock['name'] == "test"
    
    
def test_delete():
    sub = get_id()
    name = get_full_name()
    arn = get_id()
    url = get_avatar()
    LambdaFunction(sub=sub,name=name,arn=arn,url=url).create()
    mock = LambdaFunction.delete("sub",sub)
    assert mock['sub'] == sub
    
def test_find_many():
    sub = get_id()
    name = get_full_name()
    arn = get_id()
    url = get_avatar()
    LambdaFunction(sub=sub,name=name,arn=arn,url=url).create()
    mock = LambdaFunction.find_many("sub",sub)
    assert mock[0]['sub'] == sub
    assert type(mock) == list
    
    