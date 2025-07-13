from fastapi import FastAPI

from app.routers import auth
from .database import engine
from .routers import users, votes, posts
from app import db_tables

# db_tables.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to the SM API!"}

app.include_router(users.router)
app.include_router(votes.router)
app.include_router(posts.router)
app.include_router(auth.router)