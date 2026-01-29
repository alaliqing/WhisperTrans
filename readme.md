# WhisperTrans

Simple audio transcription tool for Mac (M1+ and Intel Macs). Convert any audio file to text using OpenAI's Whisper AI model.

## Features

- Easy setup with automated installation ⚡
- Web browser interface and CLI tool 🌐
- Multiple output formats (TXT, SRT, VTT) 📝
- 100+ languages supported 🌍
- Privacy first - runs locally on your Mac 🔒
- Works on Apple Silicon and Intel Macs 💻
- GPU acceleration on Apple Silicon, CPU on Intel Macs
- Fast installation with uv package manager

## Prerequisites 📦

**If you don't have Homebrew installed**, run this all-in-one command to install it (this will also install git):

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

After installation, restart your terminal or run:
```bash
eval "$(/opt/homebrew/bin/brew shellenv)"  # For Apple Silicon
# or
eval "$(/usr/local/bin/brew shellenv)"  # For Intel Macs
```

## Getting Started 🚀

**Option 1: Git Clone (Recommended)**

First, install git if needed:

```bash
# Check if git is installed
git --version

# If not installed, install via Homebrew
brew install git
```

Then clone the repository:

```bash
git clone https://github.com/alaliqing/WhisperTrans.git
cd WhisperTrans
```

**Option 2: Download ZIP**

If you don't use git:

1. Click "Code" → "Download ZIP"
2. Extract to ZIP file
3. Open terminal in the extracted folder

### 1. Setup (One-time)

```bash
./setup.sh
```

This automatically checks dependencies, installs ffmpeg and uv, creates virtual environment, and downloads packages.

### 2. Run App

**Option 1: Global Alias (Recommended)**

After setup, reload your shell (or restart terminal):
```bash
source ~/.zshrc  # or source ~/.bash_profile
```

Start the app from anywhere:
```bash
whispertrans
```

**Option 2: Direct Launch**

Run from the project directory:
```bash
./run.sh
```

**Option 3: CLI Tool**

Interactive command-line interface:
```bash
./run_cli.sh
```

Open the displayed URL in your browser (usually http://localhost:5000, terminal shows actual port if 5000 is taken).

### 3. Transcribe

**Web:** Drag & drop audio file, select model and format, click "Transcribe"

**CLI:** The script guides you through file selection, model choice, format, and language options.

## Performance by Mac Type 💻

**Apple Silicon (M1, M2, M3, etc.):**
- GPU acceleration available (10-20x faster than Intel)
- Recommended models: base, small, medium, large
- Typical transcription time: 2-10 minutes (base model)
- All features fully supported

**Intel Macs (2010-2020 models):**
- CPU-only processing (no GPU acceleration)
- Recommended models: tiny, base only
- Typical transcription time: 20-60 minutes (base model)
- Medium/Large models: Not recommended (may take 2+ hours)

**Note:** Intel Macs will work but with significantly degraded performance. For best experience, use Apple Silicon Macs or start with smaller models (tiny/base).

## AI Models

| Model   | Speed       | Accuracy | Size   | Best For               | Intel Mac               |
|---------|-------------|----------|---------|------------------------|------------------------|
| tiny    | Fastest     | 75%      | ~75MB   | Quick drafts           | Recommended             |
| base    | Fast        | 80%      | ~150MB  | General use (default)  | Recommended             |
| small   | Moderate    | 85%      | ~470MB  | Better accuracy        | Not recommended         |
| medium  | Slower      | 90%      | ~1.5GB  | Professional           | Not recommended (2+ hours) |
| large   | Slowest     | 95%      | ~3GB    | Maximum accuracy       | Not recommended (3+ hours) |

## Output Formats

- **TXT** - Plain text for documents and notes
- **SRT** - Subtitles for video players
- **VTT** - Web captions for HTML5 video

## Requirements

- macOS 11+ (Apple Silicon M1/M2/M3 OR Intel Macs 2010-2020)
- Python 3.9+
- 100MB storage + up to 3GB for AI models
- 4GB RAM minimum (8GB+ recommended for Intel Macs, 16GB+ for Apple Silicon with large models)

## Configuration

Create a `.env` file to customize settings:

```bash
FLASK_SECRET_KEY=your-secret-key
PORT=5000
MAX_UPLOAD_SIZE=200
```

## Troubleshooting

**Setup Issues** 🛠️

- "Python 3.9+ required": Install Python from https://www.python.org/downloads/ or via Homebrew: `brew install python@3.11`
- "ffmpeg not installed": The setup script will install it automatically via Homebrew
- "uv not installed": The setup script will install uv automatically for you
- "Virtual environment already exists": Delete and reinstall: `rm -rf .venv && ./setup.sh`

**Alias Issues** 🔧

- "whispertrans command not found": Restart your terminal or run `source ~/.zshrc` (or `source ~/.bash_profile`)
- "Alias doesn't work": Check that alias was added to your shell config file (~/.zshrc or ~/.bash_profile)
- "Alias stopped working after moving folder": Update to alias path in your shell config file to point to new location
- "Need to remove alias": Edit your shell config file and remove to alias line, then run source command

**Transcription Issues** ⚠️

- "Download stalls": Check internet connection, first download is 75MB-3GB depending on model
- "Slow transcription": First run is slower (model download), use smaller model (tiny/base)
- "Poor accuracy": Specify language manually, use larger model (small/medium/large), ensure good audio quality

**Intel Mac Specific Issues** 💻

- "Transcription is very slow (30+ minutes)": This is expected on Intel Macs due to CPU-only processing. Try using 'tiny' model for faster results.
- "Memory errors on medium/large models": Intel Macs typically have less memory. Stick to 'tiny' or 'base' models.
- "Freezing during transcription": Reduce file size or use smaller model (tiny). Close other applications to free up memory.

**Web UI Issues** 🌐

- "Cannot access localhost:5000": Ensure server is running, check if port 5000 is in use, try different port in `.env`
- "File upload failed": Check file size (max 200MB), ensure supported format (MP3, WAV, M4A, FLAC, OGG)

## Advanced CLI Usage

```bash
python whisper_trans.py path/to/audio.mp3 \
  --model small \
  --format srt \
  --output meeting.srt \
  --language en
```

Options:
- `--model`: Model size (tiny, base, small, medium, large)
- `--format`: Output format (txt, srt, vtt)
- `--language`: Language code (e.g., en, zh, es) or auto-detect
- `--output`: Custom output filename
- `--verbose`: Show detailed progress

## Common Languages

- English: `en`
- Chinese: `zh`
- Spanish: `es`
- French: `fr`
- German: `de`
- Japanese: `ja`
- Korean: `ko`

[Full language list](https://github.com/openai/whisper/blob/main/whisper/tokenizer.py)

## Project Structure

```
whisper_trans.py   # Core transcription logic
web_app.py         # Flask web application
templates/         # HTML templates
static/            # CSS and assets
requirements.txt   # Python dependencies
setup.sh          # Automated setup script
run.sh            # Web app launcher
run_cli.sh        # CLI tool
```

## Tips 💡

- First transcription takes a few minutes to download the model
- Use "base" model for best balance of speed and accuracy
- Specify language manually for better results
- Models are cached after first download
- All processing happens locally on your Mac

## License

MIT License - Free to use, modify, and distribute.

## Credits

Built with [OpenAI's Whisper](https://github.com/openai/whisper), [PyTorch](https://pytorch.org/), and [Flask](https://flask.palletsprojects.com/).
