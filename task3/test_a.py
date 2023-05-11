import os
import random
import asyncio

from sqlalchemy import Column, Integer, String, LargeBinary,select
from sqlalchemy.orm import declarative_base
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

engine = create_async_engine("sqlite+aiosqlite:///task.db", echo=False)
Base = declarative_base()
async_session = async_sessionmaker(engine)

inserted_cnt = 0
deleted_cnt = 0

class Task(Base):
    __tablename__ = "task3"
    id = Column(Integer, primary_key=True)
    user = Column(String(50))
    image = Column(LargeBinary)
    age = Column(Integer)
    type = Column(String(50))

def insert_random_data(session):
    global inserted_cnt
    user = f"User{random.randint(1, 10000)}"
    image = os.urandom(10)
    age = random.randint(1, 120)
    task_type = random.choice("ab")

    task = Task(user=user, image=image, age=age, type=task_type)
    session.add(task)
    inserted_cnt += 1

async def repeat_insert():
    while True:
        async with async_session() as session:
            for _ in range(9000):
                insert_random_data(session)
            await session.commit()

async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    t1 = asyncio.create_task(repeat_insert()) 

    await t1 

asyncio.run(async_main())