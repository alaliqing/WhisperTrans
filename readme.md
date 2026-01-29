# WhisperTrans

Simple audio transcription tool for Mac (M1+). Convert any audio file to text using OpenAI's Whisper AI model.

## Features

- Easy setup with automated installation 🎙️
- Web browser interface and CLI tool 🌐
- Multiple output formats (TXT, SRT, VTT) 📄
- 100+ languages supported 🌍
- Privacy first - runs locally on your Mac 🔒
- Optimized for Apple Silicon GPU acceleration ⚡

## Quick Start

### 1. Setup (One-time) 📦

```bash
./setup.sh
```

This automatically checks dependencies, installs ffmpeg, creates virtual environment, and downloads packages.

### 2. Run the App 🚀

**Web Interface:**
```bash
./run.sh
```
Open http://localhost:5000 in your browser.

**CLI Tool:**
```bash
./run_cli.sh
```
Follow the interactive prompts.

### 3. Transcribe ✍️

**Web:** Drag & drop audio file, select model and format, click "Transcribe"

**CLI:** The script guides you through file selection, model choice, format, and language options.

## AI Models

| Model   | Speed       | Accuracy | Size   | Best For               |
|---------|-------------|----------|---------|------------------------|
| tiny    | Fastest     | 75%      | ~75MB   | Quick drafts           |
| base    | Fast        | 80%      | ~150MB  | General use (default)  |
| small   | Moderate    | 85%      | ~470MB  | Better accuracy        |
| medium  | Slower      | 90%      | ~1.5GB  | Professional           |
| large   | Slowest     | 95%      | ~3GB    | Maximum accuracy       |

## Output Formats

- **TXT** - Plain text for documents and notes
- **SRT** - Subtitles for video players
- **VTT** - Web captions for HTML5 video

## Requirements

- macOS 11+ with Apple Silicon (M1, M2, M3, etc.)
- Python 3.9+
- 100MB storage + up to 3GB for AI models
- 4GB RAM minimum (8GB+ for larger models)

## Configuration

Create a `.env` file to customize settings:

```bash
FLASK_SECRET_KEY=your-secret-key
PORT=5000
MAX_UPLOAD_SIZE=200
```

## Troubleshooting 🔧

**Setup Issues**

- "Python 3.9+ required": Install Python from https://www.python.org/downloads/ or via Homebrew: `brew install python@3.11`
- "ffmpeg not installed": The setup script will install it automatically via Homebrew
- "Virtual environment already exists": Delete and reinstall: `rm -rf .venv && ./setup.sh`

**Transcription Issues**

- "Download stalls": Check internet connection, first download is 75MB-3GB depending on model
- "Slow transcription": First run is slower (model download), use smaller model (tiny/base), ensure on M1 Mac
- "Poor accuracy": Specify language manually, use larger model (small/medium/large), ensure good audio quality

**Web UI Issues**

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
