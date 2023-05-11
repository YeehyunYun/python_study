import asyncio
from typing import List
from sqlalchemy import Column, Integer, String, LargeBinary, select, func 
from sqlalchemy.orm import declarative_base
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine


engine = create_async_engine("sqlite+aiosqlite:///task.db", echo=False)
Base = declarative_base()
async_session = async_sessionmaker(engine)


class DB(Base):
    __tablename__ = 'task4'
    id = Column(Integer, primary_key=True)
    user = Column(String(50))
    image = Column(LargeBinary)
    age = Column(Integer)
    type = Column(String(50))


class CircularBuffer():
    db_index = 0
    N = 2000

    def __init__(self, size):
        if size <= 0:
            raise ValueError("Size must be a positive integer.")
        self.size = size
        self.queue = [[None] for _ in range(size)]
        self.front = -1
        self.rear = -1
        self.lock = asyncio.Lock()

    async def enqueue(self):
        async with self.lock:
            if self.front == -1:
                self.front = 0
                self.rear = 0
                async with async_session() as session:
                    stmt = select(DB).offset(self.db_index).limit(self.N)
                    result = await session.execute(stmt)
                    data = result.scalars().all()
                    print(len(data))
                self.db_index += self.N
                self.queue[self.rear] = data

            else:
                self.rear = (self.rear + 1) % self.size
                async with async_session() as session:
                    stmt = select(DB).offset(self.db_index).limit(self.N)
                    result = await session.execute(stmt)
                    data = result.scalars().all()
                self.db_index += self.N
                self.queue[self.rear] = data

    def dequeue(self):
        if self.front == -1:
            print("Queue is Empty\n")
            return None
        else:
            data: List[DB] = self.queue[self.front]
            self.queue[self.front] = [None]
            if self.front == self.rear:
                self.front = -1
                self.rear = -1
            else:
                self.front = (self.front + 1) % self.size
            return data


async def consume(circularbuffer):
    try:
        data: List[DB] = circularbuffer.dequeue()
        while len(data) != 0:
            print(data[0].id)
            data.remove(data[0])
    except AttributeError:
        pass


async def main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with async_session() as session:
        total_db_index = await session.scalar(select(func.count()).select_from(DB))

    cb = CircularBuffer(10)

    while True:
        t1 = asyncio.create_task((cb.enqueue())) 
        t2 = asyncio.create_task(consume(cb))

        await t1
        await t2

        if cb.db_index > total_db_index:
            break


if __name__ == "__main__":
    asyncio.run(main())