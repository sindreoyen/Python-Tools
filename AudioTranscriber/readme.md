# How to use
This script will allow you to extract the contents of a recording into text rapidly.

## First off
1. Install the requirements in requirements.txt
2. Make sure you have ffmpeg installed. Use your desired package manager for this.

## Run the script
1. Add your .mp3 file to ./AudioTranscriber/Audio/*yourmp3file*.mp3
2. In transcriber.py set the language of the file, see languages.py for available languages. Also make sure that you adjust how many files the file should be divided into based on its length.
3. Run transcriber.py