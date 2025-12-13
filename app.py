from flask import Flask, request, jsonify
from gemini_client import analyze_transcript

app = Flask(__name__)

@app.route("/", methods=["GET"])
def health():
    return "Gemini service running"

@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.json
    transcript = data.get("transcript")

    if not transcript:
        return jsonify({"error": "Transcript required"}), 400

    result = analyze_transcript(transcript)
    return jsonify(result)

app.run(host="0.0.0.0", port=10000)
