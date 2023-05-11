from sqlalchemy import Column, Integer, String, Text, DateTime

from database import Base


class Page(Base):
    __tablename__ = "page"

    id = Column(Integer, primary_key=True)
    subject = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    create_date = Column(DateTime, nullable=False)
