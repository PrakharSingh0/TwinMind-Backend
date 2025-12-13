import google.generativeai as genai
import os
import json

def get_model():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY missing")

    genai.configure(api_key=api_key)

    # ✅ FIXED MODEL NAME
    return genai.GenerativeModel("gemini-1.5-flash-latest")

model = get_model()


def analyze_transcript(transcript: str) -> dict:
    prompt = f"""
Return STRICT JSON with:
- title
- summary (4–6 lines)
- action_items (array)
- key_points (array)

Transcript:
{transcript}
"""

    response = model.generate_content(prompt)

    try:
        return json.loads(response.text)
    except json.JSONDecodeError:
        return {
            "title": "Transcript Summary",
            "summary": response.text.strip(),
            "action_items": [],
            "key_points": []
        }
