#!/bin/bash

# WhisperTrans Web App Launcher for macOS (M1+)
# This script starts the Flask web application

set -e

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Change to script directory
cd "$SCRIPT_DIR"

echo "Starting WhisperTrans Web Application..."
echo ""
echo "[INFO] Working directory: $SCRIPT_DIR"
echo ""

# Check if .venv exists
if [[ ! -d ".venv" ]]; then
    echo "[ERROR] Virtual environment not found."
    echo "   Please run ./setup.sh first"
    exit1
fi

# Activate virtual environment
source .venv/bin/activate

# Check if .env exists, if not create it
if [[ ! -f ".env" ]]; then
    echo "[WARNING] .env file not found. Creating..."
    cat > .env << EOL
FLASK_SECRET_KEY=$(openssl rand -hex 32)
PORT=5000
MAX_UPLOAD_SIZE=200
EOL
fi

# Load environment variables
export $(cat .env | grep -v '^#' | xargs)

# Start the Flask app
echo "[OK] Starting Flask server on port ${PORT:-5000}"
echo "[OK] Open your browser to: http://localhost:${PORT:-5000}"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Run the Flask app
python web_app.py
