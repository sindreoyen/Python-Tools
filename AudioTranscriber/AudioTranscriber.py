import threading
import speech_recognition as sr
from pydub import AudioSegment
import os
from languages import Language

##################
### Attributes ###
##################
# Folder setup
cache_folder = os.path.join('.', 'AudioTranscriber', 'Cache')
result_folder = os.path.join('.', 'AudioTranscriber', 'Results')
if not os.path.exists(cache_folder):
    os.makedirs(cache_folder)
if not os.path.exists(result_folder):
    os.makedirs(result_folder)

# Convert mp3 file to wav and load the audio file
audio_folder = os.path.join('.', 'AudioTranscriber', 'Audio')
# Print the existing audio files enumerated
print("\nExisting audio files:")
for i, file in enumerate(os.listdir(audio_folder)):
    print(f"{i}: {file}")
# Ask the user to select a file
file_index = int(input("\nSelect a file (write only the number as listed above): "))
file_start_name = os.listdir(audio_folder)[file_index].split('.')[0]

sound = AudioSegment.from_mp3(os.path.join(audio_folder, f"{file_start_name}.mp3"))
print("\n[1/6] Audio file loaded")

# Export the file to the AudioTranscriber/Cache folder
file_path = os.path.join(cache_folder, 'transcript.wav')
sound.export(file_path, format="wav")
audio = AudioSegment.from_wav(file_path)
audio.export(file_path, format='wav')
print("[2/6] Audio file exported to cache folder")

# Split the audio file into parts
length_of_audio = len(audio)
part_length = length_of_audio // 5 # Change this number to change the number of parts, for short audio files, use 1
parts = [audio[i:i + part_length] for i in range(0, length_of_audio, part_length)]
print("[3/6] Audio file split into parts")

#########################
### Run transcription ###
#########################
# Function to handle transcription of one part
def transcribe_part(part, part_number, transcriptions):
    '''
    Function to handle transcription of one part
    :param part: The part to transcribe
    :param part_number: The number of the part
    :param transcriptions: The dictionary to store the transcriptions
    '''
    file_name = os.path.join(cache_folder, f"{file_start_name}_part_{part_number}.wav")
    part.export(file_name, format="wav")
    with sr.AudioFile(file_name) as source:
        audio_data = r.record(source)
        try:
            # Here you can set the language of the transcription, see the languages.py file for available languages
            # This will not translate the file, but will specify which language the audio is in
            transcription = r.recognize_google(audio_data, language=Language.Spanish_Spain.value)
            transcriptions[part_number] = transcription
        except sr.UnknownValueError:
            print(f"Could not understand part {part_number}")
        except sr.RequestError as e:
            print(f"Could not fetch results for part {e}")

# Initialize recognizer and a dictionary to hold transcriptions
r = sr.Recognizer()
transcriptions = {}

# Here I am running in threads to speed up the process
## Create and start threads
print("[4/6] Transcribing audio file in threads")
threads = []
for i, part in enumerate(parts):
    thread = threading.Thread(target=transcribe_part, args=(part, i, transcriptions))
    threads.append(thread)
    thread.start()

## Wait for all threads to complete
print("[5/6] Waiting for transcription in all threads to complete")
for thread in threads:
    thread.join()

###################
### Save result ###
###################
# Combine transcriptions
final_transcription = " ".join(transcriptions[i] for i in sorted(transcriptions))

# Write the final transcription to a text file
text_file_name = os.path.join(result_folder, f"{file_start_name}_transcribed.txt")
with open(text_file_name, "w") as text_file:
    text_file.write(final_transcription.strip())

print(f"[6/6] Transcription saved to {text_file_name}")

# Delete the cache folder
for file in os.listdir(cache_folder):
    os.remove(os.path.join(cache_folder, file))
