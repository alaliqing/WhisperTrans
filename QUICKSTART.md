# Quick Start Guide 🚀

Get transcribing in under 5 minutes!

## Prerequisites

- Mac M1 or newer
- Python 3.9+ (check with `python3 --version`)

## Three Simple Steps

### 1️⃣ Setup (Do This Once)

```bash
./setup.sh
```

This will install everything automatically. Takes 2-5 minutes.

### 2️⃣ Start the App

**For Web Browser (Easier):**
```bash
./run.sh
```
Then open: `http://localhost:5000`

**For Command Line:**
```bash
./run_cli.sh
```

### 3️⃣ Transcribe!

**Web:** Drag & drop your audio file, select options, click "Transcribe"

**CLI:** Follow the prompts - it will ask you for:
- Audio file path
- Model size (start with "base")
- Output format (txt, srt, or vtt)
- Language (optional)

## First Time Tips

⏱️ **First transcription takes longer** - The AI model downloads automatically (150MB-3GB depending on model)

📦 **Start with "base" model** - Good balance of speed and accuracy for most uses

🎯 **Know the language?** - Specify it for better results (e.g., "en" for English)

## Common Commands

```bash
# Check Python version
python3 --version

# Run web app
./run.sh

# Run CLI tool
./run_cli.sh

# Start fresh (delete everything and reinstall)
rm -rf .venv .env && ./setup.sh
```

## Need Help?

Check the full [README.md](README.md) for detailed instructions and troubleshooting.

---

**Pro tip:** The web interface is the easiest way to get started. Use CLI when you need more control!
