import os
from contextlib import contextmanager

import psycopg2
from pgvector.psycopg2 import register_vector

DATABASE_URL = os.environ["DATABASE_URL"]


@contextmanager
def get_connection():
    conn = psycopg2.connect(DATABASE_URL)
    register_vector(conn)
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def create_document(document_id):
    with get_connection() as conn, conn.cursor() as cur:
        cur.execute("INSERT INTO documents (id) VALUES (%s)", (document_id,))


def add_chunks(document_id, chunks, embeddings):
    with get_connection() as conn, conn.cursor() as cur:
        cur.executemany(
            """
            INSERT INTO chunks (document_id, chunk_index, content, embedding)
            VALUES (%s, %s, %s, %s)
            """,
            [(document_id, i, chunk, embedding) for i, (chunk, embedding) in enumerate(zip(chunks, embeddings))],
        )


def document_exists(document_id):
    with get_connection() as conn, conn.cursor() as cur:
        cur.execute("SELECT 1 FROM documents WHERE id = %s", (document_id,))
        return cur.fetchone() is not None


def get_chunks(document_id):
    with get_connection() as conn, conn.cursor() as cur:
        cur.execute(
            "SELECT content FROM chunks WHERE document_id = %s ORDER BY chunk_index",
            (document_id,),
        )
        return [row[0] for row in cur.fetchall()]


def search(document_id, query_vector, top_k):
    with get_connection() as conn, conn.cursor() as cur:
        cur.execute(
            """
            SELECT content FROM chunks
            WHERE document_id = %s
            ORDER BY embedding <-> %s
            LIMIT %s
            """,
            (document_id, query_vector, top_k),
        )
        return [row[0] for row in cur.fetchall()]
