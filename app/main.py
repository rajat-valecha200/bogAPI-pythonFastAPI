from fastapi import FastAPI
from app import models
from app.database import engine
from app.routes import users, posts

models.Base.metadata.create_all(bind=engine)
app = FastAPI()

app.include_router(users.router)
app.include_router(posts.router)