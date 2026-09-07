from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.services import llm, quiz_generator, vector_store

router = APIRouter()


class QuizRequest(BaseModel):
    document_id: str
    num_questions: int = 3


@router.post("/quiz/generate")
def generate_quiz(body: QuizRequest):
    if not vector_store.document_exists(body.document_id):
        raise HTTPException(status_code=404, detail="Document not found")

    chunks = vector_store.get_chunks(body.document_id)
    client = llm.get_client()
    quiz = quiz_generator.generate_quiz(chunks, client, body.num_questions)

    return {"quiz": quiz}
