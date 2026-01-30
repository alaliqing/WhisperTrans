#!/usr/bin/env python3
"""Simple Flask web UI for Whisper-based transcription."""

from __future__ import annotations

import atexit
import os
import shutil
import tempfile
import uuid
from typing import Dict, Any

from flask import (
    Flask,
    flash,
    get_flashed_messages,
    redirect,
    render_template,
    request,
    url_for,
)
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

_model_cache: Dict[str, Any] = {}
# Server-side cache for transcription results
_transcription_cache: Dict[str, str] = {}

# Heartbeat tracking for auto-shutdown
_last_heartbeat: float = 0.0
_shutdown_timeout: int = 60  # seconds of inactivity before shutdown


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
        if not upload or not upload.filename:
            flash("Please choose an audio file before transcribing.", "error")
            return redirect(url_for("index"))

        filename = secure_filename(upload.filename) if upload.filename else ""
        if not filename:
            flash("Invalid filename. Please rename your file and try again.", "error")
            return redirect(url_for("index"))

        temp_dir = tempfile.mkdtemp(prefix="whisper_trans_")
        file_path = os.path.join(temp_dir, filename)
        upload.save(file_path)

        try:
            model = get_model(selected_model)
            result = transcribe_audio(
                model, file_path, language=language.strip() or None
            )
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


@app.route("/heartbeat", methods=["POST"])
def heartbeat():
    """Receive heartbeat from frontend to keep server alive."""
    global _last_heartbeat
    _last_heartbeat = time.time()
    return "OK"


@app.route("/shutdown", methods=["POST"])
def shutdown():
    """Shutdown the server and exit the application."""
    import os
    import threading

    def delayed_shutdown():
        import time

        time.sleep(1.0)
        try:
            os._exit(0)
        except:
            pass

    t = threading.Thread(target=delayed_shutdown, daemon=False)
    t.start()
    return "Server shutting down..."


def monitor_heartbeat():
    """Monitor heartbeat and shutdown if inactive for too long."""
    global _last_heartbeat
    print("Heartbeat monitor started")
    import sys

    while True:
        time.sleep(5)
        if _last_heartbeat > 0:
            elapsed = time.time() - _last_heartbeat
            print(f"Last heartbeat: {elapsed:.1f}s ago (timeout: {_shutdown_timeout}s)")
            sys.stdout.flush()
            if elapsed > _shutdown_timeout:
                print(
                    f"\nNo heartbeat received for {_shutdown_timeout} seconds, shutting down..."
                )
                sys.stdout.flush()
                os._exit(0)


if __name__ == "__main__":
    import fcntl
    import socket
    import webbrowser
    import threading
    import time
    import urllib.request
    from urllib.error import URLError

    # Single-instance lock file
    LOCK_FILE = os.path.join(tempfile.gettempdir(), "whispertrans.lock")

    def acquire_lock():
        """Acquire a file lock to ensure only one instance runs."""
        try:
            # Create lock file directory if needed
            lock_dir = os.path.dirname(LOCK_FILE)
            if not os.path.exists(lock_dir):
                os.makedirs(lock_dir)

            lock_fd = open(LOCK_FILE, "w")
            try:
                # Try to acquire exclusive, non-blocking lock
                print(f"Attempting to acquire lock: {LOCK_FILE}")
                fcntl.flock(lock_fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
                lock_fd.write(str(os.getpid()))
                lock_fd.flush()
                print(f"Lock acquired successfully, PID: {os.getpid()}")
                # Keep lock file alive while process runs
                # Lock will be automatically released when process exits and file descriptor is closed
                return True
            except (IOError, OSError) as e:
                lock_fd.close()
                # Another instance is already running
                print(f"WhisperTrans is already running! Error: {e}")
                # Also check if the process from lock file is actually alive
                try:
                    with open(LOCK_FILE, "r") as f:
                        pid = int(f.read().strip())
                        try:
                            os.kill(pid, 0)
                            print(f"Existing instance PID: {pid}")
                        except OSError:
                            print(f"Stale lock file found, removing...")
                            try:
                                os.unlink(LOCK_FILE)
                            except:
                                pass
                except:
                    pass
                return False
        except Exception as e:
            print(f"Could not acquire lock: {e}")
            return False

    def release_lock(lock_fd):
        """Release the file lock (only call on explicit shutdown)."""
        try:
            fcntl.flock(lock_fd, fcntl.LOCK_UN)
            lock_fd.close()
            if os.path.exists(LOCK_FILE):
                os.unlink(LOCK_FILE)
        except Exception:
            pass

    def wait_for_server(url, timeout=10):
        """Wait until the server is ready to accept connections."""
        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                with urllib.request.urlopen(url, timeout=1) as response:
                    if response.getcode() == 200:
                        return True
            except (URLError, socket.timeout, ConnectionRefusedError):
                time.sleep(0.1)
        return False

    def open_browser(url):
        """Open browser after server is ready."""
        if wait_for_server(url, timeout=10):
            webbrowser.open(url)
            print(f"\n✓ WhisperTrans is running at: {url}")
            print("✓ Web interface opened in your default browser")
            print("✓ Press Ctrl+C to stop the server\n")
        else:
            print(f"\n⚠ Server started but may not be ready: {url}")

    def check_port_availability(port_num):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind(("0.0.0.0", port_num))
                return True, port_num
            except OSError:
                return False, port_num

    # Try to acquire lock first - exit if another instance is running
    if not acquire_lock():
        print("Only one instance of WhisperTrans can run at a time.")
        print("If you believe this is incorrect, delete:", LOCK_FILE)
        print("Exiting now...")
        import sys

        sys.exit(1)

    # Get port from environment variable, default to 5000
    port = int(os.environ.get("PORT", 5000))

    # Try the specified port first
    is_available, _ = check_port_availability(port)

    if is_available:
        # Start server in background thread (non-daemon to prevent premature exit)
        url = f"http://127.0.0.1:{port}"

        # Start heartbeat monitor thread
        heartbeat_thread = threading.Thread(target=monitor_heartbeat, daemon=True)
        heartbeat_thread.start()

        server_thread = threading.Thread(
            target=lambda: app.run(host="0.0.0.0", port=port, use_reloader=False),
            daemon=False,
        )
        server_thread.start()

        # Open browser after server is ready
        open_browser(url)

        # Keep main thread alive until server stops
        try:
            while server_thread.is_alive():
                server_thread.join(0.5)
        except KeyboardInterrupt:
            print("\n\nShutting down WhisperTrans...")
            os._exit(0)
    else:
        # Find next available port starting from the default
        print(f"Port {port} is in use, trying to find an available port...")
        for attempt_port in range(port, port + 100):  # Try next 100 ports
            is_available, _ = check_port_availability(attempt_port)
            if is_available:
                print(f"Starting server on port {attempt_port}")
                url = f"http://127.0.0.1:{attempt_port}"

                # Start heartbeat monitor thread
                heartbeat_thread = threading.Thread(
                    target=monitor_heartbeat, daemon=True
                )
                heartbeat_thread.start()

                server_thread = threading.Thread(
                    target=lambda: app.run(
                        host="0.0.0.0", port=attempt_port, use_reloader=False
                    ),
                    daemon=False,
                )
                server_thread.start()
                open_browser(url)
                try:
                    while server_thread.is_alive():
                        server_thread.join(0.5)
                except KeyboardInterrupt:
                    print("\n\nShutting down WhisperTrans...")
                    os._exit(0)
                break
        else:
            print(
                "Could not find an available port. Please free up a port in the range and try again."
            )
