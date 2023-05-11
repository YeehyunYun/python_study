import pytest

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

import models


@pytest.fixture()
def db():
    SQLALCHEMY_DATABASE_URL = "sqlite:///./test_task4api.db"
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
    )
    SessionLocal = sessionmaker(autocommit=False, bind=engine)

    db = SessionLocal()

    models.Base.metadata.create_all(bind=engine)

    yield db

    db.close()
