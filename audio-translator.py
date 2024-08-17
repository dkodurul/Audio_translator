import os
import subprocess
from pydub import AudioSegment
import speech_recognition as sr
from googletrans import Translator
from transformers import AlbertTokenizer, AlbertModel
from deep_translator import GoogleTranslator
from gtts import gTTS
import torch

# Function to create output directory based on input file name
def create_output_directory(input_file):
    base_name = os.path.splitext(os.path.basename(input_file))[0]
    output_path = os.path.join('output', base_name)
    os.makedirs(output_path, exist_ok=True)
    return output_path

# Function to separate audio into vocals and accompaniment using Demucs
def separate_audio(input_file, output_path):
    # Ensure the output directory exists
    os.makedirs(output_path, exist_ok=True)

    # Get the base name of the input file (without extension)
    input_file_name = os.path.splitext(os.path.basename(input_file))[0]

    # Check if any file in the output directory matches the input file name
    matched_file = None
    for root, dirs, files in os.walk(output_path):
        for file in files:
            if input_file_name in file:
                matched_file = file
                break
        if matched_file:
            break

    # If a matching file is found, check if it contains vocals.wav
    if matched_file:
        vocal_file = os.path.join(root, 'vocals.wav')
        if os.path.isfile(vocal_file):
            print(f"Vocals already separated at: {vocal_file}")
            return vocal_file

    # Prepare the command for Demucs
    demucs_command = f"demucs -d cpu -n mdx_extra_q --out \"{output_path}\" \"{input_file}\""

    # Run Demucs to separate the audio
    result = subprocess.run(demucs_command, shell=True, capture_output=True, text=True)

    # Print output for debugging
    print("Demucs output:")
    print(result.stdout)
    print(result.stderr)

    # Search for the 'vocals.wav' file in the output directory
    vocal_file = None
    for root, dirs, files in os.walk(output_path):
        for file in files:
            if file == 'vocals.wav':
                vocal_file = os.path.join(root, file)
                break
        if vocal_file:
            break

    # Check if the file exists
    if not vocal_file or not os.path.isfile(vocal_file):
        raise FileNotFoundError(f"Expected file not found: vocals.wav")

    return vocal_file


# Function to convert audio file to text
def audio_to_text(audio_file):
    recognizer = sr.Recognizer()
    audio = AudioSegment.from_file(audio_file)

    # Split audio into chunks of 1 minute each
    chunk_length_ms = 60000  # 1 minute in milliseconds
    chunks = [audio[i:i + chunk_length_ms] for i in range(0, len(audio), chunk_length_ms)]

    transcription = []

    for i, chunk in enumerate(chunks):
        chunk_filename = f"chunk_{i}.wav"
        chunk.export(chunk_filename, format="wav")

        with sr.AudioFile(chunk_filename) as source:
            audio_content = recognizer.record(source)

        try:
            text = recognizer.recognize_google(audio_content)
            transcription.append(text)
        except sr.UnknownValueError:
            transcription.append("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            transcription.append(f"Could not request results from Google Speech Recognition service; {e}")

        os.remove(chunk_filename)  # Clean up the chunk file

    return " ".join(transcription)

# Function to split text into chunks for processing
def split_text(text, max_length=5000):
    chunks = []
    while len(text) > max_length:
        chunk = text[:max_length]
        # Ensure we split at a space character
        last_space = chunk.rfind(' ')
        if last_space != -1:
            chunks.append(chunk[:last_space])
            text = text[last_space+1:]
        else:
            chunks.append(chunk)
            text = text[max_length:]
    if text:
        chunks.append(text)
    return chunks

# Function to translate text to Telugu
def translate_to_telugu(text):
    translator = GoogleTranslator(source='auto', target='te')
    chunks = split_text(text)
    translated_chunks = []

    for chunk in chunks:
        print(f"Translating chunk of size {len(chunk)}")  # Debugging statement
        try:
            translated_chunk = translator.translate(chunk)
            translated_chunks.append(translated_chunk)
        except Exception as e:
            print(f"Error during translation: {e}")
            translated_chunks.append(chunk)  # Append original chunk if translation fails

    return ''.join(translated_chunks)

# Function to convert text to speech in Telugu
def text_to_speech(text, output_path):
    tts = gTTS(text=text, lang='te')
    audio_file_path = os.path.join(output_path, 'translated_audio_telugu.mp3')
    tts.save(audio_file_path)
    return audio_file_path

# Main processing function
def process_audio_file(input_audio_file):
    output_dir = create_output_directory(input_audio_file)

    # Step 1: Separate the audio into vocals and accompaniment
    try:
        vocal_file_path = separate_audio(input_audio_file, output_dir)
    except FileNotFoundError as e:
        print(e)
        return

    # Step 2: Convert the vocal audio to text
    try:
        transcribed_text = audio_to_text(vocal_file_path)
    except FileNotFoundError as e:
        print(e)
        return

    # Step 3: Translate the transcribed text to Telugu
    translated_text_file_path = os.path.join(output_dir, 'translated_text_telugu.txt')
    if os.path.exists(translated_text_file_path):
        with open(translated_text_file_path, 'r', encoding='utf-8') as file:
            translated_text = file.read()
    else:
        translated_text = translate_to_telugu(transcribed_text)
        with open(translated_text_file_path, 'w', encoding='utf-8') as file:
            file.write(translated_text)

    # Step 4: Convert the translated text to speech if it hasn't been done already
    translated_audio_file_path = os.path.join(output_dir, 'translated_audio_telugu.mp3')
    if not os.path.exists(translated_audio_file_path):
        translated_audio_file_path = text_to_speech(translated_text, output_dir)

    # Save the transcribed text to a file
    transcribed_text_file_path = os.path.join(output_dir, 'transcribed_text.txt')
    with open(transcribed_text_file_path, 'w', encoding='utf-8') as file:
        file.write(transcribed_text)

    print(f'Transcription complete. The text is saved in {transcribed_text_file_path}')
    print(f'Translation complete. The text is saved in {translated_text_file_path}')
    print(f'Translated audio complete. The audio is saved in {translated_audio_file_path}')

# Example usage
input_audio_file = 'C:/Users/dkodurul_stu/Downloads/2023 June 04 BBC One minute World News.mp3'  # replace with your audio file path
process_audio_file(input_audio_file)
