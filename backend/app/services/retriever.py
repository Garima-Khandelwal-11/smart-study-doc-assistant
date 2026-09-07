from app.services import embeddings, vector_store

TOP_K = 3


def retrieve_chunks(document_id, question, top_k=TOP_K):
    question_vector = embeddings.embed_texts([question])[0]
    return vector_store.search(document_id, question_vector, top_k)
