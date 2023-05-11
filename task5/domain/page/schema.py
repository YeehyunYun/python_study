import datetime

from pydantic import BaseModel, StrictStr


class PageCreate(BaseModel):
    subject: StrictStr
    content: StrictStr


class Page(BaseModel):
    id: int
    subject: StrictStr
    content: StrictStr
    create_date: datetime.datetime

    class Config:
        orm_mode = True
