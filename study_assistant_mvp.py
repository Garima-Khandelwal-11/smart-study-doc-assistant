from dotenv import load_dotenv
load_dotenv()

import sys
import pdfplumber
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import json
import re
from groq import Groq

sys.stdout.reconfigure(encoding='utf-8')

PDF_PATH = "sample.pdf"
CHUNK_SIZE = 500
TOP_K = 3

def load_pdf_text(path):
    text = ""
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text

def chunk_text(text, size):
    return [text[i:i+size] for i in range(0, len(text), size)]

def generate_quiz(chunks, client, num_questions=3):
    quiz = []
    selected_chunks = [c for c in chunks if len(c.strip()) > 100][:num_questions]

    for chunk in selected_chunks:
        prompt = f"""Based ONLY on the following text, generate one multiple-choice question.
"options" must be a list of 4 answer strings (no letter labels or prefixes like "A)").
"correct_answer" must be an exact copy of one of the strings in "options", not a letter.

Respond ONLY with valid JSON in this exact format, no other text:
{{"question": "What color is the sky?", "options": ["Blue", "Green", "Red", "Yellow"], "correct_answer": "Blue"}}

Text:
{chunk}
"""
        question_data = None
        for attempt in range(2):
            response = client.chat.completions.create(
                model="openai/gpt-oss-120b",
                max_tokens=500,
                messages=[{"role": "user", "content": prompt}]
            )
            raw = response.choices[0].message.content.strip()
            raw = re.sub(r"^```(?:json)?\s*|\s*```$", "", raw.strip())
            try:
                candidate = json.loads(raw)
            except json.JSONDecodeError:
                if attempt == 0:
                    continue
                print("Skipped one question - model didn't return valid JSON:", raw[:100])
                break

            if (
                not isinstance(candidate, dict)
                or "question" not in candidate
                or "options" not in candidate
                or "correct_answer" not in candidate
                or not isinstance(candidate["options"], list)
                or candidate["correct_answer"] not in candidate["options"]
            ):
                if attempt == 0:
                    continue
                print("Skipped one question - malformed structure:", raw[:100])
                break

            question_data = candidate
            break

        if question_data is not None:
            quiz.append(question_data)

    return quiz


model = SentenceTransformer("all-MiniLM-L6-v2")
text = load_pdf_text(PDF_PATH)
chunks = chunk_text(text, CHUNK_SIZE)
chunk_vectors = model.encode(chunks)

dimension = chunk_vectors.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(np.array(chunk_vectors))

client = Groq()

question = input("Ask a question about the PDF: ")
question_vector = model.encode([question])

distances, indices = index.search(np.array(question_vector), TOP_K)
retrieved_chunks = [chunks[i] for i in indices[0]]

context = "\n\n".join(retrieved_chunks)

response = client.chat.completions.create(
    model="openai/gpt-oss-120b",
    max_tokens=500,
    messages=[{
        "role": "user",
        "content": f"Answer ONLY using this context. If the answer isn't in the context, say so.\n\nContext:\n{context}\n\nQuestion: {question}"
    }]
)

print("\nAnswer:\n", response.choices[0].message.content)

quiz = generate_quiz(chunks, client)
print("\n--- Quiz ---")
for i, q in enumerate(quiz, 1):
    print(f"\nQ{i}: {q['question']}")
    for opt in q['options']:
        print(f"  - {opt}")
    print(f"Correct answer: {q['correct_answer']}")