#!/usr/bin/env python3
"""Simple Flask web UI for Whisper-based transcription."""

from __future__ import annotations

import os
import shutil
import tempfile
import uuid
from typing import Dict

from flask import Flask, flash, get_flashed_messages, redirect, render_template, request, url_for
from werkzeug.utils import secure_filename

from whisper_trans import (
    SUPPORTED_FORMATS,
    SUPPORTED_MODELS,
    build_transcription_output,
    load_whisper_model,
    transcribe_audio,
)

app = Flask(__name__, static_folder="static", template_folder="templates")
app.config["SECRET_KEY"] = os.environ.get("FLASK_SECRET_KEY", "change-me")

max_upload_mb = os.environ.get("MAX_UPLOAD_SIZE", "200")
try:
    max_upload_mb_int = int(float(max_upload_mb))
except ValueError:
    max_upload_mb_int = 200
app.config["MAX_CONTENT_LENGTH"] = max_upload_mb_int * 1024 * 1024

_model_cache: Dict[str, object] = {}
# Server-side cache for transcription results
_transcription_cache: Dict[str, str] = {}


def get_model(model_size: str):
    """Load and cache Whisper models to avoid repeated downloads."""
    model_size = model_size if model_size in SUPPORTED_MODELS else "base"
    if model_size not in _model_cache:
        _model_cache[model_size] = load_whisper_model(model_size)
    return _model_cache[model_size]


@app.route("/", methods=["GET", "POST"])
def index():
    transcription_text = None
    error = None

    # Retrieve flashed transcription ID from previous POST
    for message in get_flashed_messages(with_categories=True):
        category, message_text = message
        if category == "transcription":
            # Look up transcription from server-side cache
            transcription_text = _transcription_cache.get(message_text)
        elif category == "error":
            error = message_text
    if request.method == "POST":
        selected_model = request.form.get("model", "base")
        if selected_model not in SUPPORTED_MODELS:
            selected_model = "base"

        selected_format = request.form.get("format", "txt")
        if selected_format not in SUPPORTED_FORMATS:
            selected_format = "txt"
        language = request.form.get("language", "")
    else:
        selected_model = "base"
        selected_format = "txt"
        language = ""

    if request.method == "POST":
        upload = request.files.get("audio_file")
        if not upload or upload.filename == "":
            flash("Please choose an audio file before transcribing.", "error")
            return redirect(url_for("index"))

        filename = secure_filename(upload.filename)
        if not filename:
            flash("Invalid filename. Please rename your file and try again.", "error")
            return redirect(url_for("index"))

        temp_dir = tempfile.mkdtemp(prefix="whisper_trans_")
        file_path = os.path.join(temp_dir, filename)
        upload.save(file_path)

        try:
            model = get_model(selected_model)
            result = transcribe_audio(model, file_path, language=language.strip() or None)
            transcription_text = build_transcription_output(result, selected_format)
            # Generate a small ID and store the transcription server-side instead of in session
            transcription_id = str(uuid.uuid4())
            _transcription_cache[transcription_id] = transcription_text
            flash(transcription_id, "transcription")
            return redirect(url_for("index"))
        except Exception as exc:  # pragma: no cover - surfacing to UI
            error = str(exc)
        finally:
            shutil.rmtree(temp_dir, ignore_errors=True)

    return render_template(
        "index.html",
        transcription=transcription_text,
        error=error,
        selected_model=selected_model,
        selected_format=selected_format,
        language=language,
        supported_models=SUPPORTED_MODELS,
        supported_formats=SUPPORTED_FORMATS,
    )


if __name__ == "__main__":
    import socket
    
    # Get port from environment variable, default to 5000
    port = int(os.environ.get("PORT", 5000))
    
    # Check if the default port is available, if not try to find an available one
    def check_port_availability(port_num):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind(("0.0.0.0", port_num))
                return True, port_num
            except OSError:
                # Port is in use, try to find next available port
                return False, port_num

    # Try the specified port first
    is_available, _ = check_port_availability(port)
    
    if is_available:
        app.run(host="0.0.0.0", port=port)
    else:
        # Find next available port starting from the default
        print(f"Port {port} is in use, trying to find an available port...")
        for attempt_port in range(port, port + 100):  # Try next 100 ports
            is_available, _ = check_port_availability(attempt_port)
            if is_available:
                print(f"Starting server on port {attempt_port}")
                app.run(host="0.0.0.0", port=attempt_port)
                break
        else:
            print("Could not find an available port. Please free up a port in the range and try again.")
