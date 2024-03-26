import json
import logging
import os
import subprocess
import sys
from collections import deque
from pathlib import Path

from tafrigh import Config, TranscriptType, Writer, farrigh
from tafrigh.recognizers.wit_recognizer import WitRecognizer

# Define Wit.ai API keys for languages
LANGUAGE_API_KEYS = {
    'EN': 'YOUR_WIT_API_KEY_FOR_ENGLISH',
    'AR': 'YOUR_WIT_API_KEY_FOR_ARABIC',
    'FR': 'YOUR_WIT_API_KEY_FOR_FRENCH',
    'JA': 'YOUR_WIT_API_KEY_FOR_JAPANESE',
    # Add more languages and API keys as needed
}

# Set up logging
#logging.basicConfig(filename='transcription.log', level=logging.DEBUG)

def download_youtube_audio(youtube_url):
    output_path = Path(__file__).parent / 'downloads' / '%(id)s.%(ext)s'
    command = ['yt-dlp', '-x', '--audio-format', 'wav', '-o', str(output_path), youtube_url]
    subprocess.run(command, check=True)
    audio_file = next(Path(__file__).parent.glob('downloads/*.wav'))
    return audio_file

def convert_video_to_audio(video_path):
    audio_output_path = video_path.with_suffix('.wav')  # Ensure output is WAV
    command = ['ffmpeg', '-i', str(video_path), '-vn', '-acodec', 'pcm_s16le', '-ar', '44100', '-ac', '2', str(audio_output_path)]
    subprocess.run(command, check=True)
    print(f"Video converted to audio: {audio_output_path}")
    return audio_output_path

def convert_mp3_to_wav(mp3_path):
    wav_output_path = mp3_path.with_suffix('.wav')
    command = ['ffmpeg', '-i', str(mp3_path), str(wav_output_path)]
    subprocess.run(command, check=True)
    print(f"MP3 converted to WAV: {wav_output_path}")
    return wav_output_path

def is_wav_file(file_path):
    try:
        with open(file_path, 'rb') as file:
            return file.read(4) == b'RIFF'
    except IOError:
        return False

def transcribe_file(file_path, language_sign):
    if not is_wav_file(file_path):
        print(f"Skipping file {file_path} as it is not in WAV format.")
        return

    wit_api_key = LANGUAGE_API_KEYS.get(language_sign.upper())
    if not wit_api_key:
        print(f"API key not found for language: {language_sign}")
        return

    config = Config(
        urls_or_paths=[str(file_path)],
        skip_if_output_exist=False,
        playlist_items="",
        verbose=False,
        model_name_or_path="",
        task="",
        language="",
        use_faster_whisper=False,
        beam_size=0,
        ct2_compute_type="",
        wit_client_access_tokens=[wit_api_key],
        max_cutting_duration=5,
        min_words_per_segment=1,
        save_files_before_compact=False,
        save_yt_dlp_responses=False,
        output_sample=0,
        output_formats=[TranscriptType.TXT, TranscriptType.SRT],
        output_dir=str(file_path.parent),
    )

    print(f"Transcribing file: {file_path}")
    progress = deque(farrigh(config), maxlen=0)
    print(f"Transcription completed. Check the output directory for the generated files.")

def main():
    choice = input("Do you want to transcribe a YouTube video (Y) or a local file (L)? [Y/L]: ").strip().upper()

    if choice == 'Y':
        youtube_url = input("Enter the YouTube video link: ")
        language_sign = input("Enter the language sign (e.g., EN, AR, FR, JA): ")
        audio_file = download_youtube_audio(youtube_url)
        transcribe_file(audio_file, language_sign)
    elif choice == 'L':
        file_path = input("Enter the path to the local file or directory: ")
        file_path = Path(file_path)

        if file_path.is_dir():
            # Process all audio/video files in the directory
            for file in file_path.glob('*'):
                if file.suffix.lower() in ['.wav']:
                    language_sign = input(f"Enter the language sign for {file.name} (e.g., EN, AR, FR, JA): ")
                    transcribe_file(file, language_sign)
                elif file.suffix.lower() in ['.mp3']:
                    wav_file = convert_mp3_to_wav(file)
                    language_sign = input(f"Enter the language sign for {file.name} (e.g., EN, AR, FR, JA): ")
                    transcribe_file(wav_file, language_sign)
                elif file.suffix.lower() in ['.mp4', '.mkv', '.avi']:
                    audio_file = convert_video_to_audio(file)
                    language_sign = input(f"Enter the language sign for {file.name} (e.g., EN, AR, FR, JA): ")
                    transcribe_file(audio_file, language_sign)
        else:
            if file_path.suffix.lower() in ['.mp3']:
                file_path = convert_mp3_to_wav(file_path)
            elif file_path.suffix.lower() in ['.mp4', '.mkv', '.avi']:
                file_path = convert_video_to_audio(file_path)
            language_sign = input("Enter the language sign (e.g., EN, AR, FR): ")
            transcribe_file(file_path, language_sign)
    else:
        print("Invalid choice. Exiting.")
        sys.exit(1)

if __name__ == "__main__":
    main()
