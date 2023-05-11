import threading
import time

from typing import List
from collections import deque

from sqlalchemy import create_engine, Column, Integer, String, LargeBinary
from sqlalchemy.orm import sessionmaker, declarative_base

engine = create_engine("sqlite:///task4.db", echo=False)
Base = declarative_base()
Session = sessionmaker(bind=engine)


class DB(Base):
    __tablename__ = 'task4'
    id = Column(Integer, primary_key=True)
    user = Column(String(50))
    image = Column(LargeBinary)
    age = Column(Integer)
    type = Column(String(50))


class QueueBuffer():
    db_index = 0
    N = 2000

    def __init__(self):
        self.queue = deque()
        self.lock = threading.Lock()

    def enqueue(self):
        with self.lock:
            if len(self.queue) == 0:
                with Session() as session:
                    data = session.query(DB)[self.db_index:self.db_index+self.N]
                self.db_index += self.N
                self.queue.extend([data])
            else:
                with Session() as session:
                    data = session.query(DB)[self.db_index:self.db_index+self.N]
                self.db_index += self.N
                self.queue.extend([data])

    def dequeue(self):
        with self.lock:
            if len(self.queue) == 0:
                print("Queue is Empty\n")
                return None
            else:
                data = self.queue.popleft()
                return data


def consume(buffer):
    data = buffer.dequeue()
    while len(data) != 0:
        print(data[0].id)
        data.remove(data[0])

def main():
    with Session() as session:
        total_db_index = session.query(DB).count()

    qb = QueueBuffer()

    while True:
        t1 = threading.Thread(target=qb.enqueue)
        t2 = threading.Thread(target=consume, args=(qb,))

        t1.start()
        t2.start()

        t1.join()
        t2.join()

        if qb.db_index > total_db_index:
            break


if __name__ == "__main__":
    start = time.time()
    main() 
    print(time.time()-start)

