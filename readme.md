# Whisper Audio Transcription Tools

This repository contains Python scripts to convert audio files to text using OpenAI's Whisper model.

## Files

1. [whisper_trans.py](file:///Users/qinjing/Documents/codeData/private-program/whisper-trans/whisper_trans.py) - Command-line tool for audio transcription
2. [launch.py](file:///Users/qinjing/Documents/codeData/private-program/whisper-trans/launch.py) - Interactive launcher with user-friendly interface

## Installation

Install the required dependencies:

```bash
pip install openai-whisper
```

On some systems, you might also need to install `ffmpeg`:

- macOS: `brew install ffmpeg`
- Ubuntu: `sudo apt install ffmpeg`
- Windows: Download from https://ffmpeg.org/ or use `conda install ffmpeg`

For GPU acceleration (optional but recommended):

```bash
pip install torch torchvision torchaudio
```

## Usage

### Method 1: Command-line Interface

Use [whisper_trans.py](file:///Users/qinjing/Documents/codeData/private-program/whisper-trans/whisper_trans.py) directly with command-line arguments:

```bash
# Basic usage
python whisper_trans.py audio.mp3

# With options
python whisper_trans.py audio.mp3 --model large --language English --format srt
```

#### Command-line Options

- `audio_file` - Path to the input audio file (required)
- `-m, --model` - Model size: tiny, base, small, medium, large (default: base)
- `-l, --language` - Language of the audio (default: auto-detect)
- `-f, --format` - Output format: txt, srt, vtt (default: txt)
- `-o, --output` - Output file path (default: same name as input with appropriate extension)
- `-v, --verbose` - Enable verbose output

### Method 2: Interactive Launcher

Use [launch.py](file:///Users/qinjing/Documents/codeData/private-program/whisper-trans/launch.py) for a guided experience:

```bash
python launch.py
```

The interactive launcher will guide you through:
1. Selecting your audio file
2. Choosing the model size
3. Specifying the language (optional)
4. Selecting the output format
5. Setting the output file name

Follow the on-screen prompts to configure your transcription.

## Model Sizes

Different models offer trade-offs between speed, accuracy, and resource usage:

| Model  | Disk Space | Relative Speed | Required VRAM |
|--------|------------|----------------|---------------|
| tiny   | 75 MB      | ~32x           | ~1 GB         |
| base   | 145 MB     | ~16x           | ~1 GB         |
| small  | 485 MB     | ~6x            | ~2 GB         |
| medium | 1.5 GB     | ~2x            | ~5 GB         |
| large  | 3 GB       | 1x             | ~10 GB        |

Notes:
- Models are automatically downloaded on first use and cached locally
- Larger models are more accurate but slower
- GPU recommended for larger models
- For quick transcriptions of clear audio, use "base" or "small"
- For high-quality transcriptions of noisy audio, use "large"

## Supported Formats

Input formats (depends on ffmpeg):
- MP3
- WAV
- M4A
- FLAC
- AAC
- OGG
- And more

Output formats:
- TXT (plain text)
- SRT (SubRip subtitle)
- VTT (Web Video Text Tracks)

## Examples

### Command-line Examples

```bash
# Quick transcription of a podcast
python whisper_trans.py podcast.mp3 --model base

# High quality transcription of an interview
python whisper_trans.py interview.wav --model large --language English

# Create subtitles for a video
python whisper_trans.py video_audio.mp3 --format srt --output subtitles.srt

# Transcribe a multilingual meeting
python whisper_trans.py meeting.mp3 --model large
```

### Interactive Examples

Simply run the launcher and follow the prompts:

```bash
python launch.py
```

## Troubleshooting

1. **Installation Issues**
   - Make sure you have Python 3.8 or higher
   - If you encounter CUDA errors, try: `pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118`

2. **Performance**
   - For faster processing, use a GPU if available
   - Smaller models are significantly faster
   - For long audio files, consider breaking them into smaller segments

3. **Accuracy**
   - Specify the language if known
   - Use a larger model for better accuracy
   - Ensure good audio quality for best results

## License

This project is licensed under the MIT License - see the LICENSE file for details.