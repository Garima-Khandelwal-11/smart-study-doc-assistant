from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.services import llm, retriever, vector_store

router = APIRouter()


class AskRequest(BaseModel):
    document_id: str
    question: str


@router.post("/ask")
def ask_question(body: AskRequest):
    if not vector_store.document_exists(body.document_id):
        raise HTTPException(status_code=404, detail="Document not found")

    retrieved_chunks = retriever.retrieve_chunks(body.document_id, body.question)
    context = "\n\n".join(retrieved_chunks)
    answer = llm.ask_question(context, body.question)

    return {"answer": answer}
