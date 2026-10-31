
import os
import json
from pathlib import Path
from dotenv import load_dotenv
from google import genai

# Load .env from the same folder
BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env", override=True)

# Read API key
API_KEY = os.getenv("GEMINI_API_KEY", "").strip()

def generate_quiz(topic, difficulty, number):

    if not API_KEY:
        raise ValueError(
            "API key missing! Check GEMINI_API_KEY in .env file."
        )

    client = genai.Client(api_key=API_KEY)

    prompt = f"""
    Generate exactly {number} multiple-choice questions
    about {topic} at {difficulty} difficulty level.

    Return only valid JSON in this format:

    {{
        "questions": [
            {{
                "question": "Question text",
                "options": [
                    "Option A",
                    "Option B",
                    "Option C",
                    "Option D"
                ],
                "answer": "Correct option",
                "explanation": "Short explanation"
            }}
        ]
    }}

    Rules:
    - Generate exactly {number} questions.
    - Every question must have exactly 4 options.
    - Answer must exactly match one of the options.
    - Keep explanations short and simple.
    """

    try:
        response = client.models.generate_content(
            model="gemini-3.8-flash",
            contents=prompt,
            config={
                "response_mime_type": "application/json"
            }
        )

        if not response.text:
            raise ValueError("Gemini returned an empty response.")

        data = json.loads(response.text)
        questions = data["questions"]

        if len(questions) != number:
            raise ValueError("Unexpected number of questions generated.")

        for q in questions:
            if (
                not q.get("question")
                or len(q.get("options", [])) != 4
                or q.get("answer") not in q.get("options", [])
                or not q.get("explanation")
            ):
                raise ValueError("Generated question format is incorrect.")

        return questions

    except Exception as e:
        raise RuntimeError(f"Gemini API Error: {e}") from e
