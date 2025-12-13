from flask import Flask, request, jsonify
import whisper
import os
import uuid

app = Flask(__name__)

# Load SMALL model only (important for Render)
model = whisper.load_model("tiny")  # tiny is safest on free tier

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/transcribe", methods=["POST"])
def transcribe_audio():
    if "audio" not in request.files:
        return jsonify({"error": "No audio file provided"}), 400

    audio = request.files["audio"]
    filename = f"{uuid.uuid4()}.wav"
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    audio.save(filepath)

    result = model.transcribe(filepath)

    os.remove(filepath)

    return jsonify({
        "text": result["text"],
        "language": result["language"]
    })

@app.route("/", methods=["GET"])
def health():
    return "Whisper backend running"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
