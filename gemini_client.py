import google.generativeai as genai
import os
import json

def get_model():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY missing")

    genai.configure(api_key=api_key)

    # ✅ FIXED: fully-qualified supported model
    return genai.GenerativeModel("models/gemini-1.5-flash-002")

model = get_model()


def analyze_transcript(transcript: str) -> dict:
    prompt = f"""
Return STRICT JSON with keys:
- title
- summary
- action_items
- key_points

Transcript:
{transcript}
"""

    response = model.generate_content(prompt)

    try:
        return json.loads(response.text)
    except Exception:
        # Fail-safe so API never 500s
        return {
            "title": "Transcript Summary",
            "summary": response.text.strip(),
            "action_items": [],
            "key_points": []
        }
