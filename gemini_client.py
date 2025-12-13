import google.generativeai as genai
import os
import json

def get_model():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY missing")

    genai.configure(api_key=api_key)
    return genai.GenerativeModel("gemini-1.5-flash")

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
    return json.loads(response.text)
