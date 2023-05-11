import os
import time
import threading
import random

from sqlalchemy import create_engine, Column, Integer, String, LargeBinary, insert
from sqlalchemy.orm import sessionmaker, declarative_base

engine = create_engine("sqlite:///task4.db", echo=False)
Base = declarative_base()
Session = sessionmaker(bind=engine)

class Task(Base):
    __tablename__ = "task4"
    id = Column(Integer, primary_key=True)
    user = Column(String(50))
    image = Column(LargeBinary)
    age = Column(Integer)
    type = Column(String(50))

Base.metadata.create_all(engine)

def insert_random_data(session):
    global inserted_cnt
    user = f"User{random.randint(1, 10000)}"
    image = os.urandom(10)
    age = random.randint(1, 120)
    task_type = random.choice("ab")

    task = Task(user=user, image=image, age=age, type=task_type)
    session.add(task)

def repeat_insert():
    for _ in range(11000):
        with Session() as session:
            insert_random_data(session)
            session.commit()


repeat_insert()

