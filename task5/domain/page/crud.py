import sys
import os

from datetime import datetime

from sqlalchemy.orm import Session

sys.path.append(os.path.abspath(os.path.join(__file__, "..", "..", "..")))

from models import Page
from domain.page import schema


def create_page(db: Session, page_new: schema.PageCreate):
    db_page = Page(
        subject=page_new.subject, content=page_new.content, create_date=datetime.now()
    )
    db.add(db_page)
    db.commit()


def get_page(db: Session, page_id: int):
    if not isinstance(page_id, int) or isinstance(page_id, bool):
        raise TypeError("page_id must be an integer")
    page = db.get(Page, page_id)
    if page is None:
        raise ValueError(f"No page found with id: {page_id}")
    return page
