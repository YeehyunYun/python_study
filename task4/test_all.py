import threading
import time

from typing import List

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
        self.lock = threading.Lock()
    
    def enqueue(self):
        with self.lock:
            if (self.front == -1):
                self.front = 0
                self.rear = 0
                with Session() as session:
                    data: List[DB] = session.query(DB)[self.db_index:self.db_index+self.N] 
                self.db_index += self.N
                self.queue[self.rear] = data
            
            else:
                self.rear = (self.rear + 1) % self.size
                with Session() as session:
                    data = session.query(DB)[self.db_index:self.db_index+self.N] 
                self.db_index += self.N
                self.queue[self.rear] = data
    
    def dequeue(self):
        with self.lock:
            if (self.front == -1): 
                print ("Queue is Empty\n")
                return None
                
            else:
                data: List[DB] = self.queue[self.front]
                self.queue[self.front] = [None]
                if (self.front == self.rear):
                    self.front = -1
                    self.rear = -1
                else:
                    self.front = (self.front + 1) % self.size 
                return data


def consume(circularbuffer):
    data = circularbuffer.dequeue()
    while len(data) != 0:
        print(data[0].id)
        data.remove(data[0])


def main():
    with Session() as session:
        total_db_index = session.query(DB).count()

    cb = CircularBuffer(10)

    while True:
        t1 = threading.Thread(target=cb.enqueue)
        t2 = threading.Thread(target=consume, args=(cb,))

        t1.start()
        t2.start()

        t1.join()
        t2.join()

        if cb.db_index > total_db_index:
            break


if __name__ == "__main__":
    start = time.time()
    main() 
    print(time.time()-start)
   