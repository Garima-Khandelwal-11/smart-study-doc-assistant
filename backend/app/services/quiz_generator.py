import json
import re


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
