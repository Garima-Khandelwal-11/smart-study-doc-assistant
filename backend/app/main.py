import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes import ask, quiz, upload

app = FastAPI(title="Smart Study Doc Assistant")

allowed_origins = os.environ.get("ALLOWED_ORIGINS")
origins = (
    [origin.strip() for origin in allowed_origins.split(",")]
    if allowed_origins
    else ["http://localhost:5173"]
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(upload.router)
app.include_router(ask.router)
app.include_router(quiz.router)
