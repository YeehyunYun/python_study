import sys
import os

from datetime import datetime

import pytest

sys.path.append(os.path.abspath(os.path.join(__file__, "..", "..", "..", "..")))

import models
from domain.page import crud, schema


def test_create_page(db):
    page_data = schema.PageCreate(subject="Test Subject", content="Test Content")

    crud.create_page(db, page_data)

    db_page = db.query(models.Page).order_by(models.Page.id.desc()).first()

    assert db_page.subject == "Test Subject"
    assert db_page.content == "Test Content"
    assert isinstance(db_page.id, int)
    assert isinstance(db_page.create_date, datetime)


def test_get_page(db):
    page_id = 1
    page = crud.get_page(db, page_id)

    assert page.id == page_id


def test_get_page_invalid_id(db):
    page_id_list = [1.5, "1", 1 + 2j, [1], (1,), {"id": 1}, {1}, True]

    for page_id in page_id_list:
        with pytest.raises(TypeError):
            crud.get_page(db, page_id)


def test_get_page_out_of_range(db):
    page_id = 10000
    with pytest.raises(ValueError):
        crud.get_page(db, page_id)
