import sys
import os
import datetime

from typing import Dict, Type

from jsonschema import validate, exceptions

sys.path.append(os.path.abspath(os.path.join(__file__, "..", "..", "..", "..")))

from domain.page.schema import PageCreate, Page, BaseModel


# pydantic_model is defiened at domain.page.schema
def schema_validation(pydantic_model: Type[BaseModel], data: Dict) -> bool:
    json_schema = pydantic_model.schema()
    data = data

    try:
        validate(data, json_schema)
        return True
    except exceptions.ValidationError as e:
        print(e)
        return False


def test_page_create_schema():
    data = {"subject": 8, "content": "Test Content"}
    result = schema_validation(PageCreate, data)

    assert result == False


def test_page_schema():
    data = {
        "id": 1,
        "subject": "Test Subject",
        "content": "Test Content",
        "create_date": str(datetime.datetime.now()),
    }
    result = schema_validation(Page, data)

    assert result == True
