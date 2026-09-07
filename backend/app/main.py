from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes import ask, quiz, upload

app = FastAPI(title="Smart Study Doc Assistant")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(upload.router)
app.include_router(ask.router)
app.include_router(quiz.router)
