from fastembed import TextEmbedding

model = TextEmbedding(model_name="sentence-transformers/all-MiniLM-L6-v2")


def embed_texts(texts):
    return list(model.embed(texts))
