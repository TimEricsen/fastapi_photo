from fastapi import FastAPI

from . import models
from .database import engine
from .routers import users, photos


app = FastAPI()

app.include_router(users.router)
app.include_router(photos.router)


models.Base.metadata.create_all(bind=engine)


@app.get('/', tags=['Main'])
async def main_page():
    return "Hello, it's the main page of the cite."
