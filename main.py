from fastapi import FastAPI
from database import engine, Base
from middleware.game_request import add_request_id_middleware
from routes import users
from config import STAGE

Base.metadata.create_all(bind=engine)
app = FastAPI()

if STAGE == "prod":
    # apply ssl
    pass

add_request_id_middleware(app, "/users/")

@app.get("/")
async def root():
    return {"message": "Hello World"}

app.include_router(users.router)