from fastapi import FastAPI
from database import engine, Base
from routes import users

Base.metadata.create_all(bind=engine)
app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

app.include_router(users.router)