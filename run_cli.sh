#!/bin/bash

# WhisperTrans CLI Transcriber for macOS (M1+)
# This script provides an interactive command-line transcription tool

set -e

echo "🎙️  WhisperTrans CLI Transcriber"
echo "=================================="
echo ""

# Check if .venv exists
if [[ ! -d ".venv" ]]; then
    echo "❌ Virtual environment not found."
    echo "   Please run ./setup.sh first"
    exit 1
fi

# Activate virtual environment
source .venv/bin/activate

# Default values
MODEL="base"
FORMAT="txt"
LANGUAGE=""
VERBOSE=false

# Interactive prompts
echo "Follow the prompts to transcribe your audio file:"
echo ""

# Get audio file path
while true; do
    read -e -p "📁 Enter path to audio file: " AUDIO_FILE
    
    if [[ -z "$AUDIO_FILE" ]]; then
        echo "❌ Please enter a file path"
        continue
    fi
    
    if [[ ! -f "$AUDIO_FILE" ]]; then
        echo "❌ File not found: $AUDIO_FILE"
        continue
    fi
    
    break
done

# Get model choice
echo ""
echo "Available models:"
echo "  tiny    - Fastest, lowest accuracy (~75MB)"
echo "  base    - Balanced speed and accuracy (~150MB)"
echo "  small   - Good accuracy (~470MB)"
echo "  medium  - High accuracy (~1.5GB)"
echo "  large   - Best accuracy (~3GB)"
echo ""
read -p "🤖 Choose model [base]: " MODEL_INPUT
MODEL=${MODEL_INPUT:-base}

# Validate model
case $MODEL in
    tiny|base|small|medium|large)
        ;;
    *)
        echo "❌ Invalid model. Using 'base' instead"
        MODEL="base"
        ;;
esac

# Get format choice
echo ""
echo "Available output formats:"
echo "  txt  - Plain text transcript"
echo "  srt  - Subtitle format (SRT)"
echo "  vtt  - Web video text tracks (VTT)"
echo ""
read -p "📄 Choose format [txt]: " FORMAT_INPUT
FORMAT=${FORMAT_INPUT:-txt}

# Validate format
case $FORMAT in
    txt|srt|vtt)
        ;;
    *)
        echo "❌ Invalid format. Using 'txt' instead"
        FORMAT="txt"
        ;;
esac

# Get language (optional)
echo ""
read -p "🌐 Enter language code (optional, press Enter for auto-detect): " LANGUAGE_INPUT
LANGUAGE=$LANGUAGE_INPUT

# Ask for verbose output
echo ""
read -p "📝 Show detailed progress? (y/n) [n]: " VERBOSE_INPUT
if [[ $VERBOSE_INPUT =~ ^[Yy]$ ]]; then
    VERBOSE=true
fi

# Show summary
echo ""
echo "=================================="
echo "Transcription Summary:"
echo "  File:      $AUDIO_FILE"
echo "  Model:     $MODEL"
echo "  Format:    $FORMAT"
echo "  Language:  ${LANGUAGE:-Auto-detect}"
echo "  Verbose:   $VERBOSE"
echo "=================================="
echo ""

# Run transcription
python whisper_trans.py "$AUDIO_FILE" \
    --model "$MODEL" \
    --format "$FORMAT" \
    ${LANGUAGE:+--language "$LANGUAGE"} \
    $([[ $VERBOSE == true ]] && echo "--verbose")

echo ""
echo "✅ Transcription completed!"
