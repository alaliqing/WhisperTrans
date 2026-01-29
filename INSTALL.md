# Installation Guide

This guide provides detailed installation instructions for WhisperTrans on Mac (M1+).

## Table of Contents

1. [System Requirements](#system-requirements)
2. [Automatic Installation (Recommended)](#automatic-installation-recommended)
3. [Manual Installation](#manual-installation)
4. [Troubleshooting](#troubleshooting)
5. [Uninstallation](#uninstallation)

---

## System Requirements

### Required

- **macOS**: Big Sur (11.0) or later with Apple Silicon (M1, M2, M3, etc.)
- **Python**: 3.9 or higher
- **Storage**: At least 100MB free (plus up to 3GB for AI models)
- **RAM**: 4GB minimum (8GB+ recommended for larger models)
- **Internet**: Required for first-time setup (to download dependencies and models)

### Optional but Recommended

- **Homebrew**: Package manager (automatically installed if needed)
- **Xcode Command Line Tools**: For compiling some dependencies

### How to Check Your System

**Check macOS Version:**
```bash
sw_vers
```

**Check Chip (Apple Silicon):**
```bash
uname -m
# Should return: arm64
```

Or click Apple menu → About This Mac and look for "Apple M1/M2/M3"

**Check Python Version:**
```bash
python3 --version
```

---

## Automatic Installation (Recommended)

The easiest way to install WhisperTrans is using the automated setup script.

### Step-by-Step

1. **Open Terminal**
   - Press `Cmd + Space`, type "Terminal", and press Enter

2. **Navigate to the WhisperTrans folder**
   ```bash
   cd /path/to/WhisperTrans
   ```

3. **Run the setup script**
   ```bash
   ./setup.sh
   ```

4. **Follow the prompts**
   - The script will automatically:
     - Check your macOS version and chip
     - Verify Python version
     - Install ffmpeg (via Homebrew if needed)
     - Create a virtual environment
     - Install all dependencies
     - Set up configuration files

5. **Wait for completion**
   - Installation takes 2-5 minutes depending on internet speed
   - You'll see ✓ checkmarks as each step completes

### What the Script Does

1. **System Check**: Verifies macOS and Apple Silicon
2. **Python Check**: Ensures Python 3.9+ is installed
3. **ffmpeg Installation**: Installs audio processing tool
4. **Virtual Environment**: Creates isolated Python environment
5. **Dependencies**: Installs Flask, Whisper, and PyTorch
6. **Configuration**: Creates `.env` file with settings
7. **GPU Check**: Verifies Apple Silicon GPU acceleration

---

## Manual Installation

If the automatic script doesn't work, follow these manual steps.

### Step 1: Install Python 3.9+

**If Python is not installed:**

```bash
# Using Homebrew (recommended)
brew install python@3.11

# Or download from python.org
# Visit: https://www.python.org/downloads/
```

**Verify installation:**
```bash
python3 --version
```

### Step 2: Install Homebrew (if not installed)

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

### Step 3: Install ffmpeg

```bash
brew install ffmpeg
```

**Verify installation:**
```bash
ffmpeg -version
```

### Step 4: Create Virtual Environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Step 5: Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Step 6: Create Configuration File

```bash
cat > .env << 'EOF'
FLASK_SECRET_KEY=$(openssl rand -hex 32)
PORT=5000
MAX_UPLOAD_SIZE=200
EOF
```

### Step 7: Verify Installation

```bash
python -c "import whisper; print('Whisper installed successfully')"
python -c "import flask; print('Flask installed successfully')"
```

---

## Troubleshooting

### Common Issues

#### "Python 3.9+ is required"

**Solution:**
```bash
# Install Python 3.11 via Homebrew
brew install python@3.11

# Or download from python.org
# https://www.python.org/downloads/
```

#### "ffmpeg is not installed"

**Solution:**
```bash
# Install Homebrew if not already installed
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install ffmpeg
brew install ffmpeg
```

#### "Permission denied" when running scripts

**Solution:**
```bash
chmod +x setup.sh run.sh run_cli.sh
```

#### "Virtual environment already exists"

**Solution:**
```bash
# Remove existing virtual environment
rm -rf .venv

# Run setup again
./setup.sh
```

#### "pip install fails" or "Command not found"

**Solution:**
```bash
# Make sure virtual environment is activated
source .venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Try installing again
pip install -r requirements.txt
```

#### "ModuleNotFoundError" when running

**Solution:**
```bash
# Activate virtual environment
source .venv/bin/activate

# Verify dependencies
pip list | grep -E "whisper|flask|torch"

# Reinstall if needed
pip install -r requirements.txt
```

#### "Model download fails" or "Download stalls"

**Solutions:**
1. Check internet connection
2. Try again (downloads can timeout)
3. Use smaller model first (tiny or base)
4. Check disk space
5. Manually download model:
   ```bash
   python -c "import whisper; whisper.load_model('base')"
   ```

#### "Port 5000 already in use"

**Solution:**
```bash
# Find what's using port 5000
lsof -i :5000

# Kill the process (replace PID with actual process ID)
kill -9 PID

# Or change port in .env file
echo "PORT=5001" >> .env
```

#### "Out of memory" or "Memory error"

**Solutions:**
1. Use smaller model (tiny or base)
2. Close other applications
3. Reduce maximum upload size in `.env`
4. Use CLI instead of web interface (uses less memory)

### Performance Issues

#### Transcription is slow

**Solutions:**
1. Use smaller model (tiny → base → small → medium → large)
2. Make sure you're on Apple Silicon Mac
3. First transcription is always slower (model download)
4. Check if GPU acceleration is working:
   ```bash
   python -c "import torch; print('MPS available:', torch.backends.mps.is_available())"
   ```

#### Poor transcription accuracy

**Solutions:**
1. Specify language manually
2. Use larger model (small, medium, or large)
3. Ensure good audio quality
4. Remove background noise if possible

---

## Uninstallation

To completely remove WhisperTrans:

```bash
# Deactivate virtual environment (if active)
deactivate

# Remove virtual environment
rm -rf .venv

# Remove configuration
rm -f .env

# Remove cache (optional)
rm -rf ~/.cache/whisper

# Remove application folder (if you want to delete the project)
cd ..
rm -rf WhisperTrans
```

To keep the project but clean up:

```bash
# Keep virtual environment but remove cached models
rm -rf ~/.cache/whisper

# Or remove everything except source code
rm -rf .venv .env
```

---

## Getting Help

If you're still having issues:

1. Check the main [README.md](README.md) for more information
2. Review the [QUICKSTART.md](QUICKSTART.md) for quick reference
3. Search existing GitHub issues
4. Create a new issue with:
   - Your macOS version
   - Your Python version
   - The exact error message
   - Steps you've already tried

---

## Next Steps

After successful installation:

1. **Start transcribing**: See [QUICKSTART.md](QUICKSTART.md)
2. **Learn the features**: Read the main [README.md](README.md)
3. **Customize settings**: Edit `.env` file

---

**Happy transcribing!** 🎙️
