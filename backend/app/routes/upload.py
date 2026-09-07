import io
import uuid

from fastapi import APIRouter, File, HTTPException, UploadFile

from app.services import chunker, document_parser, embeddings, vector_store

router = APIRouter()

EXTRACTORS = {
    "pdf": document_parser.load_pdf_text,
    "docx": document_parser.extract_text_from_docx,
    "pptx": document_parser.extract_text_from_pptx,
    "txt": document_parser.extract_text_from_txt,
}


@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    extension = (file.filename or "").rsplit(".", 1)[-1].lower()
    extractor = EXTRACTORS.get(extension)
    if extractor is None:
        supported = ", ".join(f".{ext}" for ext in EXTRACTORS)
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type '.{extension}'. Supported types: {supported}",
        )

    file_bytes = await file.read()
    text = extractor(io.BytesIO(file_bytes))
    chunks = chunker.chunk_text(text)
    chunk_vectors = embeddings.embed_texts(chunks)

    document_id = uuid.uuid4().hex
    vector_store.create_document(document_id)
    vector_store.add_chunks(document_id, chunks, chunk_vectors)

    return {"document_id": document_id, "num_chunks": len(chunks)}
