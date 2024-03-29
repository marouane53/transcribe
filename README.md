# Audio and Video Transcription Tool

This Python script allows you to transcribe audio and video files using the Wit.ai API. It supports transcription of YouTube videos, local audio files (WAV and MP3), and local video files (MP4, MKV, AVI).

## Features

- Transcribe YouTube videos by providing the video link
- Transcribe local audio files in WAV or MP3 format
- Transcribe local video files in MP4, MKV, or AVI format
- Automatically convert MP3 files to WAV format for transcription
- Automatically extract audio from video files for transcription
- Support for multiple languages (requires Wit.ai API key for each language)
- Generate transcriptions in TXT and SRT formats

## Requirements

- Python 3.x
- ffmpeg
- yt-dlp
- tafrigh library (pip install "tafrigh[wit])
- ffmpeg-python library
- Wit.ai API key for each language you want to transcribe
- pydub (install this if you get an error)

## Installation

1. Clone the repository:
   git clone https://github.com/marouane53/transcribe.git

2. Install the required Python packages:
   3. Install ffmpeg:

- For Windows:
  - Download the ffmpeg build from the official website: [ffmpeg.org](https://ffmpeg.org/download.html)
  - Extract the downloaded archive and add the `bin` directory to your system's PATH environment variable.

- For macOS (using Homebrew):
  ```
  brew install ffmpeg
  ```

- For Linux (using apt):
  ```
  sudo apt update
  sudo apt install ffmpeg
  ```

4. Install yt-dlp:

- For Windows:
  ```
  pip install yt-dlp
  ```

- For macOS and Linux:
  ```
  sudo pip install yt-dlp
  ```

5. Set up Wit.ai API keys:

- Sign up for a Wit.ai account at [wit.ai](https://wit.ai/) if you don't have one.
- Create a new app for each language you want to transcribe.
- Obtain the API key for each language and replace the placeholders in the `LANGUAGE_API_KEYS` dictionary in the script with your actual API keys.

## Windows Release

For Windows users, a pre-packaged release is available that includes the necessary executable files (ffmpeg and yt-dlp) along with the Python script. You can download the release from [here](https://github.com/marouane53/transcribe/releases/download/windows_py/Transcribe.zip).

The release version eliminates the need for installing ffmpeg and yt-dlp separately, as the executable files are included in the package. Simply extract the ZIP file and run the script directly.


## Usage

1. Run the script:
   python transcribe.py
2. Choose whether you want to transcribe a YouTube video or a local file.

3. Follow the prompts to provide the necessary information (YouTube link or file path, language sign).

4. The script will download the audio (for YouTube videos), convert the file to WAV format (if necessary), and start the transcription process.

5. Once the transcription is completed, the generated files (TXT and SRT) will be saved in the same directory as the input file.

## Acknowledgments

This project was inspired by and adapted from the [Tafrigh](https://github.com/ieasybooks/tafrigh) project.

## License

This project is licensed under the [MIT License](LICENSE).
