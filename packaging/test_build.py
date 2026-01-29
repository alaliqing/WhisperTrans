#!/usr/bin/env python3
"""
Test script to verify the app works correctly before building.
This runs the web app in development mode to check for issues.
"""

import sys
import time
import webbrowser
import subprocess
import socket
import os
from pathlib import Path

def check_port(port):
    """Check if a port is available."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind(("127.0.0.1", port))
            return True
        except OSError:
            return False

def main():
    print("=" * 60)
    print("WhisperTrans Pre-Build Test")
    print("=" * 60)

    # Add project root to path
    project_root = Path(__file__).parent.parent
    sys.path.insert(0, str(project_root))
    os.chdir(project_root)

    # Check dependencies
    print("\n1. Checking dependencies...")
    try:
        import flask
        print(f"   ✓ Flask {flask.__version__}")
    except ImportError:
        print("   ✗ Flask not installed")
        return False

    try:
        import whisper
        print(f"   ✓ Whisper installed")
    except ImportError:
        print("   ✗ Whisper not installed")
        return False

    try:
        import torch
        print(f"   ✓ PyTorch {torch.__version__}")
    except ImportError:
        print("   ✗ PyTorch not installed")
        return False

    # Check for ffmpeg
    print("\n2. Checking ffmpeg...")
    if subprocess.call(["which", "ffmpeg"], stdout=subprocess.DEVNULL) == 0:
        print("   ✓ ffmpeg found")
    else:
        print("   ✗ ffmpeg not found (install with: brew install ffmpeg)")
        return False

    # Check templates and static files
    print("\n3. Checking assets...")
    if (project_root / "templates" / "index.html").exists():
        print("   ✓ templates/index.html found")
    else:
        print("   ✗ templates/index.html not found")
        return False

    if (project_root / "static" / "styles.css").exists():
        print("   ✓ static/styles.css found")
    else:
        print("   ✗ static/styles.css not found")
        return False

    # Import the app
    print("\n4. Loading web app...")
    try:
        from web_app import app
        print("   ✓ Web app loaded successfully")
    except Exception as e:
        print(f"   ✗ Failed to load web app: {e}")
        return False

    # Find available port
    print("\n5. Finding available port...")
    port = 5000
    while not check_port(port) and port < 5100:
        port += 1

    if port >= 5100:
        print("   ✗ No available port found")
        return False

    print(f"   ✓ Port {port} is available")

    # Start the server
    print("\n6. Starting Flask server...")
    url = f"http://127.0.0.1:{port}"

    def open_browser():
        time.sleep(2)
        print(f"\n   ✓ Opening browser at {url}")
        webbrowser.open(url)
        print("\n" + "=" * 60)
        print("WhisperTrans is running!")
        print(f"URL: {url}")
        print("Press Ctrl+C to stop the server")
        print("=" * 60 + "\n")

    import threading
    browser_thread = threading.Thread(target=open_browser, daemon=True)
    browser_thread.start()

    try:
        app.run(host="127.0.0.1", port=port, debug=False)
    except KeyboardInterrupt:
        print("\n\nServer stopped.")
        return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
