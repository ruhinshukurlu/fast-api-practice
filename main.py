from fastapi import FastAPI

from fastapi import FastAPI
from router import blog_post, blog_get, user
from db.database import engine
from db import models

app = FastAPI()
app.include_router(user.router)
app.include_router(blog_get.router)
app.include_router(blog_post.router)


@app.get('/hello')
def index():
  return {'message': 'Hello world!'}

models.Base.metadata.create_all(engine)