import sys
import os

from typing import Union

import pytest

from fastapi.testclient import TestClient
from pydantic import BaseModel

sys.path.append(os.path.abspath(os.path.join(__file__, "..", "..", "..", "..")))

import main

from domain.page.router import page_create, page_detail


def test_page_create():
    client = TestClient(main.app)
    json = {"subject": "new subject", "content": "new content"}
    response = client.post("api/page/create", json=json)
    assert response.status_code == 200
    assert response.json() == {"message": "Page created successfully"}


def test_page_create_invalid_type_subject(db):
    class TestPageCreate(BaseModel):
        subject: Union[int, float, complex, list, tuple, dict, set, bool]
        content: str

        class Config:
            arbitrary_types_allowed = True

    with pytest.raises(AttributeError):
        page_create(TestPageCreate, db)


def test_page_create_invalid_type_content(db):
    class TestPageCreate(BaseModel):
        subject: str
        content: Union[int, float, complex, list, tuple, dict, set, bool]

        class Config:
            arbitrary_types_allowed = True

    with pytest.raises(AttributeError):
        page_create(TestPageCreate, db)


def test_page_detail():
    client = TestClient(main.app)
    response = client.get("api/page/detail/1")
    assert response.status_code == 200

    page = response.json()
    assert page["id"] == 1


def test_page_detail_invalid_page_id(db):
    page_id_list = [1.5, "1", 1 + 2j, [1], (1,), {"id": 1}, {1}, True]

    for page_id in page_id_list:
        with pytest.raises(TypeError):
            page_detail(page_id, db)


def test_page_detail_out_of_range(db):
    page_id = 10000

    with pytest.raises(ValueError):
        page_detail(page_id, db)
