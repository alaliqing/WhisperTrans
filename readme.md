# Whisper Transcriber

Whisper Transcriber bundles a battle-tested command-line interface and a lightweight Flask web application for converting audio files to text using OpenAI's Whisper models. Upload a file, pick the model that fits your hardware, and download the transcript or subtitle output that best fits your workflow.

## Features
- Command-line workflow for automation-friendly batch transcriptions.
- Web UI with drag-and-drop style upload, model selection, format selection, and instant output.
- TXT, SRT, and VTT generation powered by the same core formatting logic.
- Re-usable helper functions (`whisper_trans.py`) so you can embed the transcriber elsewhere.
- MIT-licensed with a tiny dependency footprint: Flask + Whisper.

## Project Layout
```
├── whisper_trans.py   # CLI tool + reusable helpers
├── web_app.py         # Flask application for the interactive UI
├── templates/         # HTML template for the web UI
├── static/            # Basic styling for the UI
├── requirements.txt   # Minimal dependency spec
└── LICENSE            # MIT license
```

## Requirements
- Python 3.9+
- `ffmpeg` installed on your system (brew/apt/choco/etc.)
- Whisper + Torch dependencies (pulled in automatically via `pip install -r requirements.txt`, see the note below for GPU wheels)

> **Torch wheels:** Whisper pulls in PyTorch. For CUDA-enabled installs use the [official wheel index](https://pytorch.org/get-started/locally/) by running `pip install 'torch==2.2.*' 'torchaudio==2.2.*' --index-url https://download.pytorch.org/whl/cu121` before installing the rest of the dependencies.

## Setup
```bash
python3 -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt
```
The first transcription for each model downloads ~75 MB–3 GB of model weights. Subsequent runs re-use the cached weights located in `~/.cache/whisper/`.

## Command-line usage
Run the CLI against any audio/video file that `ffmpeg` can read:
```bash
python whisper_trans.py path/to/audio.mp3 \
  --model small \
  --language English \
  --format srt \
  --output meeting.srt
```
**Flags**
- `audio_file` (positional): file to transcribe.
- `-m / --model`: one of `tiny`, `base`, `small`, `medium`, `large` (`base` default).
- `-l / --language`: language hint. Leave blank for auto-detect.
- `-f / --format`: `txt`, `srt`, or `vtt` (`txt` default).
- `-o / --output`: explicit output path. Defaults to `<input>.<format>`.
- `-v / --verbose`: pass through Whisper's verbose output.

## Web application
Launch the interactive UI with:
```bash
export FLASK_SECRET_KEY="dev"   # optional but recommended
python web_app.py
```
Then open [http://localhost:5000](http://localhost:5000) and:
1. Upload an audio file (any format supported by ffmpeg).
2. Pick the Whisper model (first use downloads the weights).
3. Choose the output format and optional language hint.
4. Click **Transcribe** to view the result directly in the browser.

**Environment knobs**
- `PORT`: change the listen port (defaults to `5000`).
- `FLASK_SECRET_KEY`: secret key used for flash messages.
- `MAX_UPLOAD_SIZE`: max upload size in MB (defaults to `200`).

Use `flask --app web_app run --reload` for an auto-reloading development server.

## Output format cheat sheet
| Format | Use case |
| ------ | -------- |
| TXT    | Simple transcripts for search or documentation.
| SRT    | Drop-in subtitles for most video players/editors.
| VTT    | Web-native captions for HTML5 video.

## Troubleshooting & Tips
- **Model download stalls**: verify your network connection and retry; Whisper caches models once downloaded.
- **CUDA errors**: install the matching Torch version for your CUDA runtime or run on CPU by omitting GPU-specific installs.
- **Performance**: start with `base` or `small` unless you need top-tier accuracy; they use <2 GB VRAM and are significantly faster.
- **Accuracy**: specify `--language` or fill in the language field in the UI when you already know it—this skips auto-detection.

## License
This project is licensed under the [MIT License](LICENSE).
