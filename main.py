import uvicorn
from fastapi import FastAPI
from starlette.responses import Response

from db.mongodb import close, connect
from routers import users

app = FastAPI()

app.include_router(users.user_router)


@app.on_event('startup')
async def on_app_start():
    await connect()


@app.on_event('shutdown')
async def on_app_shutdown():
    await close()


@app.get('/')
async def home():
    return Response('/')


uvicorn.run(app, host="0.0.0.0", port=8000)
