# WhisperTrans

Simple audio transcription tool for Mac. Convert any audio file to text using OpenAI's Whisper AI model.

## Features

- One-click installation with DMG ⚡
- Web browser interface and CLI tool 🌐
- Multiple output formats (TXT, SRT, VTT) 📝
- 100+ languages supported 🌍
- Privacy first - runs locally on your Mac 🔒
- GPU acceleration on Apple Silicon
- No Python setup required for DMG/Homebrew installation

## Prerequisites 📦

**If you don't have Homebrew installed**, choose one of the following:

**Standard installation (recommended):**
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

**For users in China (faster mirror):**
```bash
/bin/zsh -c "$(curl -fsSL https://gitee.com/cunkai/HomebrewCN/raw/master/Homebrew.sh)"
```

After installation, restart your terminal.

## Installation 📥

### Option 1: Download DMG 🖥️

The easiest way to install WhisperTrans:

1. **Download the latest DMG** from [Releases](https://github.com/alaliqing/WhisperTrans/releases)
2. **Open DMG** and drag WhisperTrans to Applications
3. **Launch** from Applications folder

That's it! No Python setup required.



### Option 3: Git Clone 💻

For developers or users who want to modify the code:

**First, install git if needed:**

```bash
# Check if git is installed
git --version

# If not installed, install via Homebrew
brew install git
```

**Then clone the repository:**

```bash
git clone https://github.com/alaliqing/WhisperTrans.git
cd WhisperTrans
```

### Running from Source Setup 🔧

This section only applies if you installed via Git Clone or ZIP. DMG and Homebrew users can skip this.

#### 1. Setup (One-time)

```bash
./setup.sh
```

This automatically checks dependencies, installs ffmpeg and uv, creates virtual environment, and downloads packages.

#### 2. Run App

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

#### 3. Transcribe

**Web:** Drag & drop audio file, select model and format, click "Transcribe"

**CLI:** The script guides you through file selection, model choice, format, and language options.

## Performance 💻
- **Apple Silicon:** GPU acceleration available, 2-10 minutes for base model
- **Intel Macs:** CPU-only processing, 20-60 minutes for base model (Git Clone only)

Recommend using smaller models (tiny/base) on Intel Macs for best performance.

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

- macOS 11+ (Apple Silicon for DMG/Homebrew, Intel for Git Clone)
- Python 3.9+
- 100MB storage + up to 3GB for AI models
- 4GB RAM minimum (8GB+ recommended)

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
- "Transcription very slow (30+ minutes) on Intel Mac": Expected due to CPU-only processing. Use 'tiny' model for faster results.

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
