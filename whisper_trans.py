#!/usr/bin/env python3
"""
Audio to Text Converter using OpenAI's Whisper Model

This script converts audio files to text using the Whisper speech recognition model.
It supports various audio formats and provides multiple output options.
"""

import argparse
import os
import sys
import whisper
from typing import Optional


def load_whisper_model(model_size: str = "base") -> whisper.Whisper:
    """
    Load the Whisper model.
    
    Args:
        model_size: Size of the model to load. Options are:
                    'tiny', 'base', 'small', 'medium', 'large'
    
    Returns:
        Loaded Whisper model
    """
    print(f"Loading Whisper {model_size} model...")
    model = whisper.load_model(model_size)
    print("Model loaded successfully!")
    return model


def transcribe_audio(
    model: whisper.Whisper, 
    audio_file: str, 
    language: Optional[str] = None,
    verbose: bool = False
) -> dict:
    """
    Transcribe an audio file using Whisper model.
    
    Args:
        model: Loaded Whisper model
        audio_file: Path to the audio file
        language: Language of the audio (optional)
        verbose: Whether to print verbose output
    
    Returns:
        Transcription result as a dictionary
    """
    if not os.path.exists(audio_file):
        raise FileNotFoundError(f"Audio file not found: {audio_file}")
    
    print(f"Transcribing audio file: {audio_file}")
    
    # Options for transcription
    options = {
        "verbose": verbose,
    }
    
    if language:
        options["language"] = language
    
    # Transcribe the audio
    result = model.transcribe(audio_file, **options)
    
    return result


def save_transcription(result: dict, output_file: str, format: str = "txt") -> None:
    """
    Save transcription result to a file.
    
    Args:
        result: Transcription result from Whisper
        output_file: Path to the output file
        format: Output format ('txt', 'srt', 'vtt')
    """
    if format == "txt":
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(result["text"].strip())
    elif format == "srt":
        with open(output_file, "w", encoding="utf-8") as f:
            for i, segment in enumerate(result["segments"], start=1):
                start = format_timestamp(segment["start"])
                end = format_timestamp(segment["end"])
                text = segment["text"].strip()
                f.write(f"{i}\n{start} --> {end}\n{text}\n\n")
    elif format == "vtt":
        with open(output_file, "w", encoding="utf-8") as f:
            f.write("WEBVTT\n\n")
            for segment in result["segments"]:
                start = format_timestamp(segment["start"], always_include_hours=True)
                end = format_timestamp(segment["end"], always_include_hours=True)
                text = segment["text"].strip()
                f.write(f"{start} --> {end}\n{text}\n\n")


def format_timestamp(seconds: float, always_include_hours: bool = False) -> str:
    """
    Format timestamp in SRT/VTT format.
    
    Args:
        seconds: Timestamp in seconds
        always_include_hours: Whether to always include hours
    
    Returns:
        Formatted timestamp string
    """
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds_remainder = seconds % 60
    
    if always_include_hours or hours > 0:
        return f"{hours:02d}:{minutes:02d}:{seconds_remainder:06.3f}"
    else:
        return f"{minutes:02d}:{seconds_remainder:06.3f}"


def main():
    parser = argparse.ArgumentParser(description="Convert audio to text using Whisper")
    parser.add_argument("audio_file", help="Path to the audio file")
    parser.add_argument("-o", "--output", help="Output file path")
    parser.add_argument("-m", "--model", default="base", 
                        choices=["tiny", "base", "small", "medium", "large"],
                        help="Model size (default: base)")
    parser.add_argument("-l", "--language", help="Language of the audio")
    parser.add_argument("-f", "--format", default="txt", 
                        choices=["txt", "srt", "vtt"],
                        help="Output format (default: txt)")
    parser.add_argument("-v", "--verbose", action="store_true",
                        help="Verbose output")
    
    args = parser.parse_args()
    
    try:
        # Load the model
        model = load_whisper_model(args.model)
        
        # Transcribe the audio
        result = transcribe_audio(model, args.audio_file, args.language, args.verbose)
        
        # Print result to console
        print("\nTranscription:")
        print(result["text"])
        
        # Save to file if output path provided
        if args.output:
            save_transcription(result, args.output, args.format)
            print(f"\nTranscription saved to {args.output}")
        else:
            # Generate output filename based on input
            base_name = os.path.splitext(args.audio_file)[0]
            output_file = f"{base_name}.{args.format}"
            save_transcription(result, output_file, args.format)
            print(f"\nTranscription saved to {output_file}")
            
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()