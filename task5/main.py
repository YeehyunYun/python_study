import uvicorn

from fastapi import FastAPI

import models

from database import engine
from domain.page import router


app = FastAPI()


models.Base.metadata.create_all(bind=engine)


app.include_router(router.router)


if __name__ == "__main__":
    uvicorn.run(app)
