from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import io
import PyPDF2
import openai
import uuid
from collections import defaultdict


app = Flask(__name__)
CORS(app)

openai.api_key = os.getenv("'")

document_store = defaultdict(list)



def extract_text_from_file(file_storage):
    """Extracts text from PDF or TXT file."""
    filename = file_storage.filename.lower()

    if filename.endswith(".pdf"):
        pdf_reader = PyPDF2.PdfReader(file_storage)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() or ""
        return text

    elif filename.endswith(".txt"):
        return file_storage.read().decode("utf-8")

    else:
        return ""


def chunk_text(text, chunk_size=1000):
    """Splits long text into smaller chunks."""
    words = text.split()
    for i in range(0, len(words), chunk_size):
        yield " ".join(words[i:i + chunk_size])




@app.route("/upload", methods=["POST"])
def upload_documents():
    """Accepts multiple files, extracts text, stores them by session_id."""
    session_id = request.args.get("session_id") or str(uuid.uuid4())

    if "file" not in request.files:
        return jsonify({"error": "No file part"}), 400

    files = request.files.getlist("file")
    for file in files:
        text = extract_text_from_file(file)
        if text.strip():
            document_store[session_id].append(text)

    return jsonify({"message": "Files uploaded and processed", "session_id": session_id})





if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
