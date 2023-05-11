import os
import time
import threading
import random

from sqlalchemy import create_engine, Column, Integer, String, LargeBinary, insert
from sqlalchemy.orm import sessionmaker, declarative_base

engine = create_engine("sqlite:///task.db", echo=False)
Base = declarative_base()
Session = sessionmaker(bind=engine)

inserted_cnt = 0
deleted_cnt = 0

class Task(Base):
    __tablename__ = "task3"
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
    inserted_cnt += 1

def repeat_insert():
    while True:
        with Session() as session:
            for _ in range(10000):
                insert_random_data(session)
            session.commit()

def select_data(session):
    tasks = session.query(Task).all()
    return tasks

def delete_data(session, tasks):
    global deleted_cnt
    for task in tasks:
        session.delete(task)
        deleted_cnt += 1

def repeat_select_delete():
    while True:
        with Session() as session:
            tasks = select_data(session)
            delete_data(session, tasks)
            session.commit()

def print_cnt():
    global inserted_cnt, deleted_cnt
    while True:
        time.sleep(1)
        print(f"insert thread : {inserted_cnt} rows per sec\n")
        print(f"select_delete thread : {deleted_cnt} rows per sec\n")
        inserted_cnt = 0
        deleted_cnt = 0

def main():

    t1 = threading.Thread(target=repeat_insert, args=())
    t2 = threading.Thread(target=repeat_select_delete, args=())
    t3 = threading.Thread(target=print_cnt, args=())

    t1.start()
    t2.start()
    t3.start()

if __name__ == "__main__":
    main()