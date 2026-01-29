# WhisperTrans 🎙️

A simple, easy-to-use audio transcription tool for Mac (M1+). Convert any audio file to text in seconds using OpenAI's Whisper AI model.

Perfect for transcribing meetings, lectures, podcasts, interviews, and voice notes.

## ✨ Features

- **Easy to Install** - One-command setup with automatic dependency management
- **Two Ways to Use** - Web browser interface or command-line tool
- **Multiple Formats** - Export as plain text (TXT), subtitles (SRT), or web captions (VTT)
- **100+ Languages** - Supports automatic language detection
- **Privacy First** - Everything runs locally on your Mac, no data sent to the cloud
- **Mac M1+ Optimized** - Uses Apple Silicon GPU acceleration for faster transcription

## 🚀 Quick Start (3 Steps)

### 1. Download & Setup

Open Terminal, navigate to the project folder, and run:

```bash
./setup.sh
```

This will automatically:
- Check if you have Python 3.9+ installed
- Install any missing dependencies (including ffmpeg)
- Set up a virtual environment
- Download and install all required packages

*⚠️ First-time setup takes 2-5 minutes depending on your internet speed.*

### 2. Choose Your Interface

**Option A: Web Browser (Recommended for Beginners)**

```bash
./run.sh
```

Then open your browser to: `http://localhost:5000`

Just drag and drop your audio file and click "Transcribe"!

**Option B: Command Line (For Advanced Users)**

```bash
./run_cli.sh
```

Follow the prompts to transcribe your audio file.

### 3. Transcribe Your First File

- **Web UI**: Upload any audio file, select your preferred model and format, then click "Transcribe"
- **CLI**: The script will guide you through each step with simple prompts

*⏱️ First transcription may take a few minutes while the AI model downloads. Subsequent transcriptions are much faster.*

## 📚 How It Works

### AI Models (Choose Based on Your Needs)

| Model | Speed | Accuracy | Download Size | Best For |
|-------|-------|----------|---------------|----------|
| **tiny** | ⚡ Fastest | 75% | ~75MB | Quick drafts, rough notes |
| **base** | ⚡ Fast | 80% | ~150MB | General use (default) |
| **small** | Moderate | 85% | ~470MB | Better accuracy |
| **medium** | Slower | 90% | ~1.5GB | Professional transcription |
| **large** | Slowest | 95% | ~3GB | Maximum accuracy |

### Output Formats

- **TXT** - Plain text for documents, notes, or copying
- **SRT** - Subtitles compatible with most video players and editors
- **VTT** - Web captions for HTML5 videos

## 🖥️ Web Interface

The web browser interface provides:

- **Drag & Drop Upload** - Just drop your audio file into the browser
- **Model Selection** - Choose the AI model that fits your needs
- **Format Selection** - Export as TXT, SRT, or VTT
- **Language Support** - Auto-detect or select from 100+ languages
- **Instant Results** - View transcription in browser with copy & download buttons

### Using the Web UI

1. Run `./run.sh`
2. Open `http://localhost:5000` in your browser
3. Drag & drop your audio file (or click to browse)
4. Select model size and output format
5. Optionally specify the language if you know it
6. Click "Transcribe"
7. Copy or download your transcription

## 💻 Command Line Interface

For users comfortable with Terminal, the CLI provides more control:

```bash
# Basic usage
./run_cli.sh

# Direct Python usage (advanced)
python whisper_trans.py path/to/audio.mp3 \
  --model small \
  --format srt \
  --output meeting.srt
```

### CLI Options

- `--model`: Choose model size (tiny, base, small, medium, large)
- `--format`: Output format (txt, srt, vtt)
- `--language`: Specify language (e.g., en, zh, es) or leave blank for auto-detect
- `--output`: Custom output filename
- `--verbose`: Show detailed progress

## 🔧 Advanced Configuration

### Environment Variables

Create a `.env` file to customize settings (automatically created by setup):

```bash
FLASK_SECRET_KEY=your-secret-key
PORT=5000                    # Change web server port
MAX_UPLOAD_SIZE=200          # Max file size in MB
```

### Language Codes

Common languages:
- English: `en`
- Chinese: `zh`
- Spanish: `es`
- French: `fr`
- German: `de`
- Japanese: `ja`
- Korean: `ko`

[Full list of supported languages](https://github.com/openai/whisper/blob/main/whisper/tokenizer.py)

## 📋 Requirements

- **MacOS**: M1 (Apple Silicon) or newer
- **Python**: 3.9 or higher (automatically checked by setup)
- **Storage**: 100MB for the app + up to 3GB for AI models (downloaded on first use)
- **Memory**: 4GB RAM recommended (8GB+ for large models)

### Checking Your Mac

To check if you have an M1 Mac:
1. Click Apple menu → About This Mac
2. Look for "Apple M1", "M2", "M3", etc. in the chip name

To check Python version:
```bash
python3 --version
```

## ❓ Troubleshooting

### Setup Issues

**"Python 3.9+ is required"**
- Download Python 3.9+ from [python.org](https://www.python.org/downloads/)
- Or install via Homebrew: `brew install python@3.11`

**"ffmpeg is not installed"**
- The setup script will try to install it automatically via Homebrew
- If that fails, install manually: `brew install ffmpeg`

**"Virtual environment already exists"**
- Delete it and run setup again: `rm -rf .venv && ./setup.sh`

### Transcription Issues

**"Model download stalls"**
- Check your internet connection
- The models are large (75MB-3GB) and may take time
- Models are cached after first download

**"Transcription is slow"**
- First transcription is always slower (model download)
- Use a smaller model (tiny or base) for faster results
- Make sure you're on an M1 Mac for GPU acceleration

**"Poor accuracy"**
- Specify the language manually
- Use a larger model (small, medium, or large)
- Ensure audio quality is good (clear speech, minimal background noise)

### Web UI Issues

**"Cannot access localhost:5000"**
- Make sure the server is running (check Terminal)
- Check if another app is using port 5000
- Try a different port by setting `PORT=5001` in `.env`

**"File upload failed"**
- Check file size (default max is 200MB)
- Ensure file format is supported (MP3, WAV, M4A, FLAC, OGG, etc.)
- Check file permissions

## 🛠️ For Developers

Want to customize or extend WhisperTrans?

### Project Structure

```
whisper_trans.py   # Core transcription logic
web_app.py         # Flask web application
templates/         # HTML templates for web UI
static/            # CSS and static assets
requirements.txt    # Python dependencies
setup.sh          # Automated setup script
run.sh            # Web app launcher
run_cli.sh        # CLI tool
```

### Running Tests

```bash
source .venv/bin/activate
pytest  # If tests are available
```

### Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

MIT License - Free to use, modify, and distribute.

## 🙏 Credits

- Built with [OpenAI's Whisper](https://github.com/openai/whisper) model
- Powered by [PyTorch](https://pytorch.org/)
- Web interface with [Flask](https://flask.palletsprojects.com/)

## 📞 Support

- **Issues**: Report bugs on GitHub
- **Documentation**: See this README and comments in source files
- **Community**: Join discussions on GitHub

---

**Happy Transcribing!** 🎉

Made with ❤️ for Mac users who need simple, fast, and accurate audio transcription.
