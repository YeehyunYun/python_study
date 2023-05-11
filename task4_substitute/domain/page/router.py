import sys
import os

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

sys.path.append(os.path.abspath(os.path.join(__file__, "..", "..", "..")))

from database import get_db
from domain.page import crud, schema


router = APIRouter(
    prefix="/api/page",
)


@router.post("/create")
def page_create(_page_new: schema.PageCreate, db: Session = Depends(get_db)):
    crud.create_page(db=db, page_new=_page_new)
    return {"message": "Page created successfully"}


@router.get("/detail/{page_id}", response_model=schema.Page)
def page_detail(page_id: int, db: Session = Depends(get_db)):
    page = crud.get_page(db, page_id=page_id)
    return page
