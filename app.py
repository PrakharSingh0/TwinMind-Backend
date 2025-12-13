from flask import Flask, request, jsonify
import whisper
import os
import uuid

app = Flask(__name__)

# Load Whisper model ONCE (important)
model = whisper.load_model("base")  # tiny | base | small

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/transcribe", methods=["POST"])
def transcribe_audio():
    if "audio" not in request.files:
        return jsonify({"error": "No audio file provided"}), 400

    audio = request.files["audio"]
    filename = f"{uuid.uuid4()}.mp3"
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    audio.save(filepath)

    # Transcribe
    result = model.transcribe(filepath)

    # Cleanup
    os.remove(filepath)

    return jsonify({
        "text": result["text"],
        "language": result["language"]
    })

if __name__ == "__main__":
    app.run(debug=True)
