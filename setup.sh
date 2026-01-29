#!/bin/bash

# WhisperTrans Setup Script for macOS (M1+)
# This script automates the installation process for non-developers

set -e  # Exit on error

echo "🎙️  WhisperTrans Setup Script for macOS (M1+)"
echo "================================================"
echo ""

# Check if running on macOS
if [[ "$OSTYPE" != "darwin"* ]]; then
    echo "❌ This script is designed for macOS only."
    echo "   Please use the manual installation instructions in README.md"
    exit 1
fi

# Check for Apple Silicon
if [[ $(uname -m) != 'arm64' ]]; then
    echo "⚠️  Warning: This project is optimized for Apple Silicon (M1+)"
    echo "   Running on Intel Mac may require additional setup"
    read -p "   Continue anyway? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed."
    echo "   Please install Python 3.9+ from https://www.python.org/downloads/"
    exit 1
fi

PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
echo "✓ Found Python $PYTHON_VERSION"

# Check Python version (need 3.9+)
PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d. -f1)
PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d. -f2)

if [[ $PYTHON_MAJOR -lt 3 ]] || [[ $PYTHON_MAJOR -eq 3 && $PYTHON_MINOR -lt 9 ]]; then
    echo "❌ Python 3.9+ is required, but you have $PYTHON_VERSION"
    exit 1
fi

# Check if ffmpeg is installed
if ! command -v ffmpeg &> /dev/null; then
    echo "⚠️  ffmpeg is not installed. Installing via Homebrew..."
    
    # Check if Homebrew is installed
    if ! command -v brew &> /dev/null; then
        echo "❌ Homebrew is not installed."
        echo "   Please install Homebrew first:"
        echo "   /bin/bash -c \"\$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\""
        exit 1
    fi
    
    brew install ffmpeg
    echo "✓ ffmpeg installed successfully"
else
    echo "✓ ffmpeg is installed"
fi

# Create virtual environment if it doesn't exist
if [[ ! -d ".venv" ]]; then
    echo ""
    echo "📦 Creating virtual environment..."
    python3 -m venv .venv
    echo "✓ Virtual environment created"
else
    echo "✓ Virtual environment already exists"
fi

# Activate virtual environment
echo ""
echo "🔧 Activating virtual environment..."
source .venv/bin/activate

# Upgrade pip
echo ""
echo "⬆️  Upgrading pip..."
pip install --upgrade pip --quiet

# Install dependencies
echo ""
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Check for Mac M1 optimized torch installation
echo ""
echo "🚀 Checking for Apple Silicon optimizations..."
python3 << 'EOF'
import torch
if hasattr(torch.backends, 'mps'):
    if torch.backends.mps.is_available():
        print("✓ Apple Silicon GPU acceleration available")
    else:
        print("ℹ️  Apple Silicon GPU acceleration not available (will use CPU)")
else:
    print("ℹ️  Running on CPU (MPS not available)")
EOF

# Create .env file if it doesn't exist
if [[ ! -f ".env" ]]; then
    echo ""
    echo "📝 Creating .env file..."
    cat > .env << EOL
# Flask configuration
FLASK_SECRET_KEY=$(openssl rand -hex 32)
PORT=5000
MAX_UPLOAD_SIZE=200
EOL
    echo "✓ .env file created"
else
    echo "✓ .env file already exists"
fi

echo ""
echo "================================================"
echo "✅ Setup completed successfully!"
echo ""
echo "Next steps:"
echo "  1. Start the web app:    ./run.sh"
echo "  2. Or use CLI:           ./run_cli.sh"
echo "  3. Read the README for more details"
echo ""
echo "First transcription may take a few minutes to download the model."
echo "================================================"
