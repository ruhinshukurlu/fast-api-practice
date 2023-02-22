from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.exceptions import HTTPException
from fastapi.responses import PlainTextResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.websockets import WebSocket

import time
from client import html

from fastapi import FastAPI
from router import (
    blog_post, blog_get, user, article, product, file, dependencies
)
from templates_folder import templates
from auth import authentication

from db.database import engine
from db import models
from exceptions import StoryException

app = FastAPI()

app.include_router(dependencies.router)
app.include_router(templates.router)
app.include_router(authentication.router)
app.include_router(file.router)
app.include_router(user.router)
app.include_router(article.router)
app.include_router(product.router)
app.include_router(blog_get.router)
app.include_router(blog_post.router)


@app.exception_handler(StoryException)
def story_exception_handler(request: Request, exc: StoryException):
    return JSONResponse(
        status_code=418,
        content=exc.name
    )


@app.get('/')
async def get():
    return HTMLResponse(html)

clients = []

@app.websocket('/chat')
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    clients.append(websocket)
    while True:
        data = await websocket.receive_text()
        for client in clients:
            await client.send_text(data)


# @app.exception_handler(HTTPException)
# def custom_handler(request: Request, exc: StoryException):
#     return PlainTextResponse(str(exc), status_code=400)

models.Base.metadata.create_all(engine)


@app.middleware('http')
async def add_middleware(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    duration = time.time() - start_time
    response.headers['duration'] = str(duration)
    return response


origins = [
    "http://127.0.0.1:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials = True,
    allow_headers = ["*"],
    allow_methods = ["*"]
)

app.mount('/files', StaticFiles(directory='files'), name='files')
app.mount("/templates_folder/static", StaticFiles(directory="templates_folder/static"), name="static")